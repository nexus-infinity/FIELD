#!/bin/bash
# Sacred Component Deployment Execution Scripts
# Run each command in separate terminal sessions as needed

echo "🔮 Sacred Component Incremental Deployment System"
echo "=============================================="
echo ""

# Check Python dependencies
echo "📋 Checking Python dependencies..."
python3 -c "import redis, psutil, websockets, flask" 2>/dev/null || {
    echo "⚠️ Missing Python dependencies. Installing..."
    pip3 install redis psutil websockets flask
}

echo ""
echo "🎯 Available Commands (run each in separate terminal):"
echo ""

# Command 1: Run deployment
echo "1. 🚀 Run Sacred Component Deployment:"
echo "   cd /Users/jbear/FIELD/scripts"
echo "   python3 sacred_incremental_deployment.py"
echo ""

# Command 2: Run monitoring dashboard  
echo "2. 📊 Run Real-time Monitoring Dashboard:"
echo "   cd /Users/jbear/FIELD/scripts"
echo "   python3 sacred_dashboard_monitor.py"
echo ""

# Command 3: Run validation only
echo "3. 🔍 Run Validation Only (no deployment):"
echo "   cd /Users/jbear/FIELD/scripts"
echo "   python3 -c \"from sacred_incremental_deployment import SacredDeploymentManager; dm = SacredDeploymentManager(); [print(f'✅ {c[\"name\"]}: {dm.run_comprehensive_validation(c, [])}') for c in dm.sacred_components]\""
echo ""

# Command 4: Check component status
echo "4. 📈 Check Component Status:"
echo "   cd /Users/jbear/FIELD/scripts" 
echo "   python3 -c \"from sacred_dashboard_monitor import SacredDashboardMonitor; monitor = SacredDashboardMonitor(); import json; print(json.dumps(monitor.get_component_status(), indent=2))\""
echo ""

# Command 5: Run single component deployment
echo "5. 🎲 Deploy Single Component (example: ATLAS):"
echo "   cd /Users/jbear/FIELD/scripts"
echo "   python3 -c \"from sacred_incremental_deployment import SacredDeploymentManager; dm = SacredDeploymentManager(); success, result = dm.deploy_component(dm.sacred_components[0], []); print(f'Success: {success}'); import json; print(json.dumps(result, indent=2))\""
echo ""

# Command 6: View logs
echo "6. 📄 View Deployment Logs:"
echo "   tail -f /Users/jbear/FIELD/logs/sacred_deployment.log"
echo ""

# Command 7: View dashboard state
echo "7. 🔄 View Dashboard State (for backward compatibility):"
echo "   cat /Users/jbear/FIELD/logs/dashboard_state.json | jq ."
echo ""

# Command 8: Quick system status
echo "8. ⚡ Quick System Status:"
echo "   cd /Users/jbear/FIELD/scripts"
echo "   python3 -c \"from sacred_dashboard_monitor import SacredDashboardMonitor; import json; print(json.dumps(SacredDashboardMonitor().get_system_status(), indent=2))\""
echo ""

echo "🌟 Usage Tips:"
echo "- Run dashboard monitor first to see real-time updates"
echo "- Use separate terminals for deployment and monitoring"
echo "- Dashboard available at http://localhost:8080"
echo "- WebSocket updates on ws://localhost:8765"
echo ""

# Make this script executable
chmod +x "$0"
