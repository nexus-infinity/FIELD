import logging
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
import time
from datetime import datetime

# Configure logging
log_path = os.path.expanduser('~/FIELD/_MCP/mcp.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('MCP_Monitor')

class MCPMonitor:
    def __init__(self):
        self.directory_watchers = {}
        self.stream_processors = set()
        self.error_count = 0
        self.last_error_check = time.time()
        self.pipeline_status = {}
        
    def start_directory_watcher(self, path):
        """Start watching a directory for changes."""
        if path in self.directory_watchers:
            logger.warning(f"Already watching directory: {path}")
            return

        class DirHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                logger.info(f"Directory event: {event.event_type} - {event.src_path}")

        path = os.path.expanduser(path)
        observer = Observer()
        handler = DirHandler()
        observer.schedule(handler, path, recursive=True)
        observer.start()
        
        self.directory_watchers[path] = observer
        logger.info(f"Started watching directory: {path}")

    def register_stream_processor(self, processor_id):
        """Register a stream processor for monitoring."""
        self.stream_processors.add(processor_id)
        self.pipeline_status[processor_id] = {
            'status': 'active',
            'last_active': datetime.now(),
            'processed_count': 0
        }
        logger.info(f"Registered stream processor: {processor_id}")

    def update_stream_status(self, processor_id, status='active', processed_count=None):
        """Update the status of a stream processor."""
        if processor_id not in self.pipeline_status:
            logger.warning(f"Unknown stream processor: {processor_id}")
            return

        self.pipeline_status[processor_id]['status'] = status
        self.pipeline_status[processor_id]['last_active'] = datetime.now()
        if processed_count is not None:
            self.pipeline_status[processor_id]['processed_count'] = processed_count
        
        logger.info(f"Stream processor {processor_id} status: {status}")

    def log_error(self, error_msg, severity='ERROR'):
        """Log an error and update error statistics."""
        self.error_count += 1
        logger.error(f"{severity}: {error_msg}")

    def get_error_rate(self, time_window=3600):
        """Calculate error rate for the past hour."""
        current_time = time.time()
        # Reset error count if time window has passed
        if current_time - self.last_error_check > time_window:
            self.error_count = 0
            self.last_error_check = current_time
        
        return self.error_count / time_window  # errors per second

    def get_system_metrics(self):
        """Get system resource usage metrics."""
        metrics = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        }
        logger.info(f"System metrics: {metrics}")
        return metrics

    def get_pipeline_status(self):
        """Get status of all monitored pipelines."""
        return self.pipeline_status

    def stop_all_watchers(self):
        """Stop all directory watchers."""
        for path, observer in self.directory_watchers.items():
            observer.stop()
            observer.join()
            logger.info(f"Stopped watching directory: {path}")
        self.directory_watchers.clear()

# Example usage:
if __name__ == "__main__":
    monitor = MCPMonitor()
    
    # Start watching MCP directory
    monitor.start_directory_watcher("~/FIELD/_MCP")
    
    # Register a test stream processor
    monitor.register_stream_processor("test_processor")
    
    try:
        while True:
            # Update metrics every 60 seconds
            monitor.get_system_metrics()
            time.sleep(60)
    except KeyboardInterrupt:
        monitor.stop_all_watchers()
