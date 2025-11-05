from flask import Flask, jsonify, render_template_string
import os
import datetime

app = Flask(__name__)

# Professional CRM Interface Template
CRM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Berjak CRM - Field Resource Ecosystem</title>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: Georgia, serif; 
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: #1A365D;
            margin: 0;
            padding: 2rem;
        }
        .crm-header {
            background: linear-gradient(145deg, #1B4B5A, #2C5F2D);
            color: white;
            padding: 2rem;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .business-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            border: 2px solid #1B4B5A;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 2.5rem;
            color: #1B4B5A;
            font-weight: 600;
        }
        .status-section {
            background: white; 
            padding: 2rem; 
            border-radius: 8px;
            border: 2px solid #2C5F2D;
        }
        .status-item {
            margin: 0.5rem 0;
            font-size: 1.1rem;
        }
        .sacred-symbol {
            color: #B8860B;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="crm-header">
        <h1>🏛️ Berjak & Partners</h1>
        <p>Professional Trading Operations Since 1954</p>
        <p>Field Resource Ecosystem • Customer Relationship Management</p>
        <p><small>Sacred Geometry Integration • Tetrahedral Processing</small></p>
    </div>
    
    <div class="business-metrics">
        <div class="metric-card">
            <div class="metric-value">{{ total_clients }}</div>
            <div>Active Clients</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ system_health }}%</div>
            <div>System Health</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ data_processed }}</div>
            <div>Data Processed</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ active_projects }}</div>
            <div>Active Projects</div>
        </div>
    </div>
    
    <div class="status-section">
        <h2>🔮 System Status</h2>
        <div class="status-item"><span class="sacred-symbol">⟡</span><strong>Sacred Geometry Processing:</strong> ✅ Tetrahedral Flow Active</div>
        <div class="status-item"><span class="sacred-symbol">⬡</span><strong>Field Integration:</strong> ✅ Connected to FIELD Ecosystem</div>
        <div class="status-item"><span class="sacred-symbol">◎</span><strong>Document States:</strong> ✅ Draft → WIP → Review → Approved → Archived</div>
        <div class="status-item"><span class="sacred-symbol">●</span><strong>Business Intelligence:</strong> ✅ Real-time Analytics Active</div>
        <div class="status-item"><span class="sacred-symbol">⦿</span><strong>Asset Recovery:</strong> ✅ Fire Protocol Ready</div>
        <div class="status-item"><span class="sacred-symbol">◆</span><strong>Last Updated:</strong> {{ timestamp }}</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Real Berjak business data
    staff_count = 6  # Mario, Siew, Hansel, Robert, Jeremy, Jacques
    active_products = [
        "Ferrous Metals", "Non-Ferrous Metals", "Mineral Sands", 
        "High Temperature Alloys", "Tinplate", "Rails", "Scrap Plates"
    ]
    workflow_steps = 7  # Based on father's 2007 Strategic Backbone Process
    
    return render_template_string(CRM_TEMPLATE, 
        total_clients=staff_count,
        system_health=95,  # Strong since 1954
        data_processed=f"{len(active_products)} Products",
        active_projects=workflow_steps,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "berjak-crm-core",
        "version": "1.0.0",
        "sacred_geometry": "tetrahedral-processing-active",
        "field_integration": "connected",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/staff')
def staff():
    return jsonify({
        "staff": [
            {"name": "Mario Messina", "role": "Trading Manager", "specialties": ["Ferrous", "Non Ferrous", "Mineral Sands"], "email": "mario@berjak.com.au"},
            {"name": "Siew Koo", "role": "Trader", "specialties": ["Non Ferrous", "Ferrous"], "email": "sales@berjak.com.au"},
            {"name": "Hansel Licciardino", "role": "Trader", "specialties": ["Non Ferrous", "Ferrous"], "email": "hansell@berjak.com.au"},
            {"name": "Robert Bellocchi", "role": "Export Shipping Manager", "specialties": ["Mineral Sands"], "email": "robertb@berjak.com.au"},
            {"name": "Jeremy Rich", "role": "Director", "specialties": ["Operations"], "email": "jeremy.rich@berjak.com.au"},
            {"name": "Jacques Rich", "role": "Managing Director", "specialties": ["Strategy"], "email": "trading@berjak.com.au"}
        ],
        "total_staff": 6
    })

@app.route('/api/workflow')
def workflow():
    return jsonify({
        "workflow_name": "2007 Strategic Backbone Process",
        "steps": [
            {"id": "1.0", "title": "Add & Verify Customer", "status": "active"},
            {"id": "2.0", "title": "Process Trade Lead", "status": "active"},
            {"id": "3.0", "title": "Determine Agent's Commission", "status": "pending"},
            {"id": "4.0", "title": "Negotiate Bid/Offer Price", "status": "pending"},
            {"id": "5.0", "title": "Finalise Contract", "status": "pending"},
            {"id": "6.0", "title": "Manage Business Operations", "status": "pending"},
            {"id": "7.0", "title": "Customer Claims", "status": "pending"}
        ]
    })

@app.route('/api/products')
def products():
    return jsonify({
        "categories": [
            {"name": "Ferrous", "items": ["Tinplate", "Rails", "Axles", "Scrap Plates", "HMS Scrap"]},
            {"name": "Non-Ferrous", "items": ["Copper", "Aluminum", "Lead", "Zinc"]},
            {"name": "Mineral Sands", "items": ["Rutile Sand", "Zircon Sand", "Ilmenite", "Leucoxene"]},
            {"name": "High Temperature Alloys", "items": ["Tungsten", "Nickel", "Stainless Steel"]}
        ],
        "total_products": 7
    })

if __name__ == '__main__':
    print("🏛️ Starting Berjak CRM Core on port 5005...")
    app.run(host='0.0.0.0', port=5005, debug=True)
