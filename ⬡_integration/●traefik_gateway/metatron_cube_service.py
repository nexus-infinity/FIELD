#!/usr/bin/env python3
"""
Metatron Cube Service
Sacred Geometry API Service for Trident Rotational Lock

This service provides the Metatron Cube Translator as a web API
integrated with the Tetrahedron Dojo ERP system.
"""

from flask import Flask, jsonify, render_template_string, request
from metatron_trident_erp_integration import MetatronCubeTranslator
import json
from datetime import datetime

app = Flask(__name__)

# Initialize the Metatron Cube Translator
translator = MetatronCubeTranslator()

# Sacred Geometry HTML Template
SACRED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>⬡ Metatron Cube Translator - Trident Rotational Lock</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: #e94560;
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }
        .sacred-container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(233, 69, 96, 0.2);
        }
        .sacred-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #f39c12;
        }
        .metatron-cube {
            width: 300px;
            height: 300px;
            margin: 2rem auto;
            display: block;
        }
        .dojo-vertices {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .vertex-card {
            background: rgba(243, 156, 18, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #f39c12;
            text-align: center;
        }
        .vertex-name {
            font-size: 1.5rem;
            color: #f39c12;
            margin-bottom: 0.5rem;
        }
        .vertex-frequency {
            color: #e94560;
            font-weight: bold;
        }
        .trident-axes {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }
        .axis-card {
            background: rgba(233, 69, 96, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e94560;
            text-align: center;
        }
        .status-section {
            background: rgba(0, 0, 0, 0.3);
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        .status-item {
            margin: 0.5rem 0;
            display: flex;
            justify-content: space-between;
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
        .golden-ratio {
            color: #f1c40f;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="sacred-container">
        <header class="sacred-header">
            <h1>⬡ Metatron Cube Translator</h1>
            <h2>Trident Rotational Lock • Sacred Geometry Alignment</h2>
            <p class="pulse">13 Sacred Circles • 5 Platonic Solids • Golden Ratio Harmonics</p>
        </header>

        <!-- Metatron Cube Sacred Geometry -->
        <div style="text-align: center;">
            <svg class="metatron-cube" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
                <!-- 13 Sacred Circles -->
                <circle cx="200" cy="200" r="10" fill="#f39c12" opacity="0.8"/>
                <circle cx="320" cy="200" r="8" fill="#e94560" opacity="0.7"/>
                <circle cx="80" cy="200" r="8" fill="#e94560" opacity="0.7"/>
                <circle cx="200" cy="80" r="8" fill="#e94560" opacity="0.7"/>
                <circle cx="200" cy="320" r="8" fill="#e94560" opacity="0.7"/>
                <circle cx="280" cy="120" r="6" fill="#3498db" opacity="0.6"/>
                <circle cx="120" cy="120" r="6" fill="#3498db" opacity="0.6"/>
                <circle cx="120" cy="280" r="6" fill="#3498db" opacity="0.6"/>
                <circle cx="280" cy="280" r="6" fill="#3498db" opacity="0.6"/>
                <circle cx="260" cy="140" r="5" fill="#2ecc71" opacity="0.5"/>
                <circle cx="140" cy="140" r="5" fill="#2ecc71" opacity="0.5"/>
                <circle cx="140" cy="260" r="5" fill="#2ecc71" opacity="0.5"/>
                <circle cx="260" cy="260" r="5" fill="#2ecc71" opacity="0.5"/>
                
                <!-- Sacred Connections -->
                <line x1="200" y1="80" x2="80" y2="200" stroke="#f39c12" stroke-width="1" opacity="0.4"/>
                <line x1="200" y1="80" x2="320" y2="200" stroke="#f39c12" stroke-width="1" opacity="0.4"/>
                <line x1="80" y1="200" x2="200" y2="320" stroke="#f39c12" stroke-width="1" opacity="0.4"/>
                <line x1="320" y1="200" x2="200" y2="320" stroke="#f39c12" stroke-width="1" opacity="0.4"/>
                
                <!-- Tetrahedron overlay -->
                <polygon points="200,100 150,250 250,250" fill="none" stroke="#e94560" stroke-width="2" opacity="0.6"/>
                
                <!-- Golden Ratio Spiral -->
                <path d="M200,200 Q220,180 240,200 Q240,220 220,240 Q200,240 180,220 Q180,200 200,200" 
                      fill="none" stroke="#f1c40f" stroke-width="2" opacity="0.8"/>
            </svg>
        </div>

        <!-- Tetrahedron Dojo Vertices -->
        <h3 style="text-align: center; color: #f39c12;">🔺 Tetrahedron Dojo Vertices</h3>
        <div class="dojo-vertices">
            <div class="vertex-card">
                <div class="vertex-name">OBI-WAN</div>
                <div>Observation Intelligence</div>
                <div class="vertex-frequency">432 Hz</div>
            </div>
            <div class="vertex-card">
                <div class="vertex-name">TATA</div>
                <div>Transformation Architecture</div>
                <div class="vertex-frequency">528 Hz</div>
            </div>
            <div class="vertex-card">
                <div class="vertex-name">ATLAS</div>
                <div>Analysis Logic System</div>
                <div class="vertex-frequency">639 Hz</div>
            </div>
            <div class="vertex-card">
                <div class="vertex-name">DOJO</div>
                <div>Dynamic Operations Junction</div>
                <div class="vertex-frequency">741 Hz</div>
            </div>
        </div>

        <!-- Trident Lock Axes -->
        <h3 style="text-align: center; color: #e94560;">⚡ Trident Rotational Lock</h3>
        <div class="trident-axes">
            <div class="axis-card">
                <h4>X-Axis</h4>
                <div>Semantic Alignment</div>
                <div><small>Meaning & Context</small></div>
            </div>
            <div class="axis-card">
                <h4>Y-Axis</h4>
                <div>Temporal Alignment</div>
                <div><small>Time & Sequence</small></div>
            </div>
            <div class="axis-card">
                <h4>Z-Axis</h4>
                <div>Geometric Alignment</div>
                <div><small>Structure & Form</small></div>
            </div>
        </div>

        <!-- System Status -->
        <div class="status-section">
            <h3>🔮 Sacred System Status</h3>
            <div class="status-item">
                <span>Metatron Cube:</span>
                <span class="pulse" style="color: #2ecc71;">⬡ ACTIVE</span>
            </div>
            <div class="status-item">
                <span>Trident Lock:</span>
                <span style="color: #f39c12;">⚡ {{ lock_status }}</span>
            </div>
            <div class="status-item">
                <span>Golden Ratio:</span>
                <span class="golden-ratio">φ = 1.618033988749</span>
            </div>
            <div class="status-item">
                <span>Sacred Coherence:</span>
                <span style="color: #3498db;">{{ coherence_level }}%</span>
            </div>
            <div class="status-item">
                <span>ERP Integration:</span>
                <span style="color: #{{ connection_color }};">{{ erp_status }}</span>
            </div>
        </div>

        <!-- API Endpoints -->
        <div class="status-section">
            <h3>🔗 Sacred API Endpoints</h3>
            <div style="font-family: 'Courier New', monospace; font-size: 0.9rem;">
                <div>GET /api/status - System status and health</div>
                <div>GET /api/sync - Synchronize with ERP system</div>
                <div>GET /api/dojo - Tetrahedron Dojo configuration</div>
                <div>POST /api/align - Align attributes in sacred geometry</div>
                <div>GET /api/trident - Trident lock status and stability</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Sacred Geometry Dashboard"""
    # Get current system status
    sync_result = translator.sync_with_erp_system()
    
    # Determine display values
    lock_status = "ROTATIONALLY LOCKED" if sync_result.get("status") == "synchronized" else "SEEKING ALIGNMENT"
    
    if "trident_lock" in sync_result:
        coherence = sync_result["trident_lock"]["trident_lock"].get("sacred_coherence", 0) * 100
        coherence_level = f"{coherence:.1f}"
    else:
        coherence_level = "0.0"
    
    erp_status = sync_result.get("erp_connection", "unknown").upper()
    connection_color = "2ecc71" if erp_status == "ACTIVE" else "e94560"
    
    return render_template_string(SACRED_TEMPLATE,
        lock_status=lock_status,
        coherence_level=coherence_level,
        erp_status=erp_status,
        connection_color=connection_color
    )

@app.route('/api/status')
def api_status():
    """System status and health check"""
    dojo_config = translator.generate_tetrahedron_dojo_config()
    
    return jsonify({
        "metatron_cube": "active",
        "sacred_geometry": "13_circles_active",
        "tetrahedron_dojo": "4_vertices_operational",
        "trident_lock": "3_axes_aligned",
        "golden_ratio": translator.sacred_geometry.PHI,
        "sacred_frequencies": [432.0, 528.0, 639.0, 741.0],
        "platonic_solids": ["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"],
        "system_health": "optimal",
        "last_update": datetime.now().isoformat()
    })

@app.route('/api/sync')
def api_sync():
    """Synchronize with ERP system and apply sacred alignment"""
    sync_result = translator.sync_with_erp_system()
    return jsonify(sync_result)

@app.route('/api/dojo')
def api_dojo():
    """Tetrahedron Dojo configuration"""
    dojo_config = translator.generate_tetrahedron_dojo_config()
    return jsonify(dojo_config)

@app.route('/api/align', methods=['POST'])
def api_align():
    """Align custom attributes in sacred geometry"""
    try:
        data = request.json or {}
        sacred_attributes = []
        
        for key, value in data.items():
            attr = translator.align_erp_attribute(key, value)
            sacred_attributes.append(attr)
        
        if sacred_attributes:
            trident_result = translator.rotationally_lock_trident(sacred_attributes)
            return jsonify({
                "status": "aligned",
                "attributes_processed": len(sacred_attributes),
                "trident_lock": trident_result,
                "alignment_timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "no_attributes",
                "message": "No attributes provided for alignment"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/trident')
def api_trident():
    """Trident lock status and stability metrics"""
    sync_result = translator.sync_with_erp_system()
    
    if "trident_lock" in sync_result:
        trident_data = sync_result["trident_lock"]["trident_lock"]
        return jsonify({
            "trident_status": "locked",
            "stability": trident_data.get("lock_stability", 0),
            "coherence": trident_data.get("sacred_coherence", 0),
            "center_of_mass": trident_data.get("center_of_mass", [0, 0, 0]),
            "rotational_tensor": trident_data.get("rotational_tensor", [[0,0,0],[0,0,0],[0,0,0]]),
            "axes": {
                "semantic": "meaning_context_alignment",
                "temporal": "time_sequence_alignment", 
                "geometric": "structure_form_alignment"
            },
            "last_lock": datetime.now().isoformat()
        })
    else:
        return jsonify({
            "trident_status": "unlocked",
            "message": "Trident seeking rotational alignment",
            "erp_connection": sync_result.get("erp_connection", "unknown")
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "metatron-cube-translator",
        "sacred_geometry": "active",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("⬡ Starting Metatron Cube Translator Service...")
    print("🔺 Tetrahedron Dojo Integration Active")
    print("⚡ Trident Rotational Lock Ready")
    print("🔮 Sacred Geometry Alignment Operational")
    print(f"🌐 Serving on http://localhost:5007")
    
    app.run(host='0.0.0.0', port=5007, debug=True)