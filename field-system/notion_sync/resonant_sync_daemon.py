#!/usr/bin/env python3
"""
Resonant Sync Daemon - Master Orchestrator
Coordinates file watcher, truth evaluator, and bidirectional sync
Respects Eval Cadence and scheduler settings from Notion registry
"""

import os
import sys
import time
import signal
from datetime import datetime, timedelta
from pathlib import Path
import logging
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from truth_evaluator import TruthEvaluator
from notion_to_local_sync import NotionToLocalSync
from notionscribe_reflection import run_notionscribe_dispatch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [DAEMON] %(message)s',
    handlers=[
        logging.FileHandler('/Users/jbear/FIELD-LIVING/notion_sync/resonant_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Daemon state
class DaemonState:
    def __init__(self):
        self.running = False
        self.file_watcher_pid = None
        self.last_truth_eval = None
        self.last_reflection_dispatch = None
        self.eval_cadence_minutes = 360  # Default: evaluate every 6 hours (safe, infrequent)
        
daemon_state = DaemonState()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"\n🛑 Received signal {signum}, shutting down...")
    daemon_state.running = False

def start_file_watcher():
    """Start the file watcher daemon in background"""
    try:
        # File watcher should already be running from earlier
        # Check if it's running
        pid_file = Path(__file__).parent / 'file_watcher.pid'
        
        if pid_file.exists():
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process is running
            try:
                os.kill(pid, 0)  # Sends signal 0 to check if process exists
                logger.info(f"✅ File watcher already running (PID: {pid})")
                daemon_state.file_watcher_pid = pid
                return True
            except OSError:
                logger.warning(f"File watcher PID file exists but process not running")
        
        logger.info("⚠️  File watcher not running. Please start it manually:")
        logger.info("   ./file_watcher.sh start")
        return False
        
    except Exception as e:
        logger.error(f"Error checking file watcher: {e}")
        return False

def run_truth_evaluation():
    """Run truth evaluation cycle"""
    try:
        logger.info("\n🔺 Running Truth Evaluation Cycle...")
        evaluator = TruthEvaluator()
        evaluator.run_evaluation_cycle()
        daemon_state.last_truth_eval = datetime.utcnow()
        logger.info(f"✅ Truth evaluation complete at {daemon_state.last_truth_eval.isoformat()}")
        return True
    except Exception as e:
        logger.error(f"Truth evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_notion_to_local_pull():
    """Run Notion → Local pull for sections where Notion has higher truth"""
    try:
        logger.info("\n🔻 Running Notion → Local Pull...")
        puller = NotionToLocalSync(dry_run=False)
        puller.run_pull_cycle()
        logger.info("✅ Notion → Local pull complete")
        return True
    except Exception as e:
        logger.error(f"Notion → Local pull failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def should_run_truth_eval() -> bool:
    """Check if it's time to run truth evaluation based on cadence"""
    if daemon_state.last_truth_eval is None:
        return True
    
    elapsed = datetime.utcnow() - daemon_state.last_truth_eval
    elapsed_minutes = elapsed.total_seconds() / 60
    
    return elapsed_minutes >= daemon_state.eval_cadence_minutes

def should_dispatch_reflection() -> bool:
    """Dispatch reflection cues at most every 4 hours."""
    if daemon_state.last_reflection_dispatch is None:
        return True
    elapsed = datetime.utcnow() - daemon_state.last_reflection_dispatch
    return elapsed >= timedelta(hours=4)

def daemon_loop():
    """Main daemon loop"""
    logger.info("\n" + "="*60)
    logger.info("🌟 RESONANT SYNC DAEMON STARTING")
    logger.info("="*60)
    logger.info(f"Eval Cadence: {daemon_state.eval_cadence_minutes} minutes")
    logger.info(f"File Watcher: {'Running' if daemon_state.file_watcher_pid else 'Not detected'}")
    logger.info("="*60 + "\n")
    
    daemon_state.running = True
    cycle_count = 0
    
    while daemon_state.running:
        cycle_count += 1
        logger.info(f"\n{'─'*60}")
        logger.info(f"Daemon Cycle #{cycle_count}")
        logger.info(f"{'─'*60}")
        
        try:
            # Check if truth evaluation should run
            if should_run_truth_eval():
                logger.info("⏰ Time for truth evaluation")
                
                # Step 1: Evaluate truth (compare local vs Notion)
                if run_truth_evaluation():
                    # Step 2: Pull from Notion if any sections have higher truth there
                    run_notion_to_local_pull()
            else:
                next_eval_minutes = daemon_state.eval_cadence_minutes - \
                    ((datetime.utcnow() - daemon_state.last_truth_eval).total_seconds() / 60)
                logger.info(f"⏳ Next truth eval in {next_eval_minutes:.1f} minutes")

            if should_dispatch_reflection():
                logger.info("🧭 Dispatching NotionScribe reflection cues...")
                try:
                    run_notionscribe_dispatch()
                    daemon_state.last_reflection_dispatch = datetime.utcnow()
                    logger.info("✅ Reflection cues refreshed.")
                except Exception as exc:
                    logger.error(f"NotionScribe dispatch failed: {exc}")
                    import traceback
                    traceback.print_exc()
            
            # Sleep for a short interval before next check
            # Check every minute if it's time to evaluate
            sleep_seconds = 60
            logger.info(f"💤 Sleeping for {sleep_seconds}s...")
            time.sleep(sleep_seconds)
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Keyboard interrupt received")
            break
        except Exception as e:
            logger.error(f"Error in daemon loop: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(60)  # Wait before retrying
    
    logger.info("\n" + "="*60)
    logger.info("🌟 RESONANT SYNC DAEMON STOPPED")
    logger.info("="*60 + "\n")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Resonant Sync Daemon - Master Orchestrator')
    parser.add_argument('--cadence', type=int, default=360, 
                       help='Truth evaluation cadence in minutes (default: 360 = 6 hours)')
    parser.add_argument('--eval-now', action='store_true',
                       help='Run one truth evaluation cycle and exit')
    parser.add_argument('--pull-now', action='store_true',
                       help='Run one Notion → Local pull and exit')
    
    args = parser.parse_args()
    
    # Set cadence
    daemon_state.eval_cadence_minutes = args.cadence
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # One-shot modes
    if args.eval_now:
        logger.info("Running one-time truth evaluation...")
        run_truth_evaluation()
        sys.exit(0)
    
    if args.pull_now:
        logger.info("Running one-time Notion → Local pull...")
        run_notion_to_local_pull()
        sys.exit(0)
    
    # Check file watcher status
    start_file_watcher()
    
    # Start daemon loop
    try:
        daemon_loop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
