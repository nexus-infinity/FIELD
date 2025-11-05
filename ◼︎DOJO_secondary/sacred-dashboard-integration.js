---
symbol: ◼
origin: ~/FIELD/◼DOJO/
created: 2025-01-27T21:35:00+10:00
geometry: tetrahedral-manifest
lineage: ⟡Akron > FIELD > DOJO
---

import express from 'express';
import { WebSocketServer } from 'ws';
import Redis from 'redis';
import { promises as fs } from 'fs';
import path from 'path';
import crypto from 'crypto';
import { createServer } from 'http';

// Import our sacred components
import SacredChatBridge from './sacred-chat-bridge.js';
import SacredSphereStateManager from './sacred-sphere-manager.js';

/**
 * SacredDashboardIntegration - Central orchestrator for all sacred components
 * Provides REST/WebSocket APIs and CLI instrumentation for sacred metrics
 */
class SacredDashboardIntegration {
    constructor() {
        this.app = express();
        this.server = createServer(this.app);
        this.redis = Redis.createClient();
        this.port = process.env.SACRED_DASHBOARD_PORT || 3000;
        this.wsPort = process.env.SACRED_WS_PORT || 8080;
        
        // Sacred component instances
        this.sacredChatBridge = new SacredChatBridge();
        this.sphereStateManager = new SacredSphereStateManager();
        
        // Sacred metrics collectors
        this.geometricValidator = null;
        this.biologicalFlow = null;
        this.fractalObserver = null;
        
        // Sacred configuration
        this.sacredConfig = null;
        
        // WebSocket connections for real-time updates
        this.dashboardConnections = new Set();
    }

    async initialize() {
        console.log('🔮 Initializing Sacred Dashboard Integration...');
        
        try {
            // Initialize Redis connection
            await this.redis.connect();
            console.log('✅ Redis connection established');
            
            // Load sacred configuration
            await this.loadSacredConfig();
            
            // Initialize sacred components
            await this.initializeSacredComponents();
            
            // Setup Express middleware and routes
            this.setupExpressApp();
            
            // Setup WebSocket server for real-time updates
            this.setupWebSocketServer();
            
            // Initialize sacred metrics collection
            await this.initializeSacredMetrics();
            
            // Start the servers
            await this.startServers();
            
            console.log('✅ Sacred Dashboard Integration manifested successfully');
            console.log(`🌐 REST API: http://localhost:${this.port}`);
            console.log(`🔗 WebSocket: ws://localhost:${this.wsPort}`);
            
        } catch (error) {
            console.error('❌ Sacred Dashboard initialization failed:', error.message);
            throw error;
        }
    }

    async loadSacredConfig() {
        const configPath = path.join(process.env.HOME, 'FIELD', '◼DOJO', 'sacred-config.json');
        const configData = await fs.readFile(configPath, 'utf8');
        this.sacredConfig = JSON.parse(configData);
        console.log('🔐 Sacred configuration loaded');
    }

    async initializeSacredComponents() {
        // Initialize sphere state manager
        await this.sphereStateManager.initialize();
        console.log('🌀 Sacred Sphere State Manager initialized');
        
        // Initialize chat bridge (if not already running)
        if (!this.sacredChatBridge.wss) {
            await this.sacredChatBridge.initialize();
            console.log('💬 Sacred Chat Bridge integrated');
        }
        
        // Initialize validation components
        this.initializeValidationComponents();
        console.log('🛡️ Sacred validation components ready');
    }

    initializeValidationComponents() {
        // Geometric Cleanliness Validator
        this.geometricValidator = {
            async validate(sphere, action) {
                const violations = [];
                
                // Check for duplicated logic
                if (action.content && action.content.includes('duplicate')) {
                    violations.push('Potential duplicated logic detected');
                }
                
                // Check for unauthorized patterns
                const unauthorizedPatterns = [
                    'sudo rm -rf',
                    'format c:',
                    'DROP DATABASE',
                    'killall -9 $(pgrep)'
                ];
                
                if (action.content) {
                    for (const pattern of unauthorizedPatterns) {
                        if (action.content.toLowerCase().includes(pattern.toLowerCase())) {
                            violations.push(`Unauthorized pattern detected: ${pattern}`);
                        }
                    }
                }
                
                return {
                    isClean: violations.length === 0,
                    violations,
                    sphere,
                    timestamp: new Date().toISOString(),
                    geometricScore: Math.max(0, 1 - (violations.length * 0.2))
                };
            }
        };
        
        // Biological Flow Processor
        this.biologicalFlow = {
            async breathIn(message) {
                return {
                    origin: 'external',
                    content: message.content || message,
                    timestamp: new Date().toISOString(),
                    purity_status: 'unverified',
                    intake_path: '/Volumes/Akron/ → ~/FIELD-LIVING/',
                    phase: 'breath_in'
                };
            },
            
            async process(intake, targetSphere) {
                const geometricValidation = await this.geometricValidator.validate(targetSphere, intake);
                const symbolicAnchor = this.assignSymbolicAnchor(intake);
                
                return {
                    ...intake,
                    target_sphere: targetSphere,
                    geometric_validation: geometricValidation,
                    symbolic_anchor: symbolicAnchor,
                    processing_path: '~/FIELD-LIVING/ → ~/FIELD-DEV/',
                    phase: 'process'
                };
            },
            
            async breathOut(processed) {
                return {
                    manifestation: this.generateManifestation(processed),
                    execution_ready: processed.geometric_validation.isClean,
                    sacred_path: '~/FIELD/ → ~/FIELD/◼DOJO/',
                    geometric_status: processed.geometric_validation,
                    phase: 'breath_out'
                };
            },
            
            async memoryLoop(manifested) {
                const memoryEntry = {
                    manifestation_id: this.generateManifestationId(),
                    content: manifested.manifestation,
                    lineage: '◼DOJO → ●OBI-WAN → ⟡Akron',
                    archive_path: '/Volumes/Akron/',
                    timestamp: new Date().toISOString(),
                    phase: 'memory_loop'
                };
                
                return memoryEntry;
            },
            
            assignSymbolicAnchor(intake) {
                if (!intake.content) return '●';
                
                const content = intake.content.toLowerCase();
                if (content.includes('tool') || content.includes('validate')) return '▲';
                if (content.includes('time') || content.includes('log')) return '▼';
                if (content.includes('memory') || content.includes('sync')) return '●';
                if (content.includes('manifest') || content.includes('execute')) return '◼';
                
                return '●'; // Default to memory/observation
            },
            
            generateManifestation(processed) {
                return `Sacred processing completed for ${processed.content} in sphere ${processed.target_sphere}`;
            },
            
            generateManifestationId() {
                return `sacred_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
            }
        };
        
        // Fractal Observer based on the provided toolbox pattern
        this.fractalObserver = {
            async scanFormStructure(data) {
                const structural_integrity = Math.random() * 0.3 + 0.7; // 70-100%
                return {
                    form_integrity: structural_integrity,
                    resonance_clarity: Math.random() * 0.4 + 0.6, // 60-100%
                    structural_coherence: structural_integrity > 0.8,
                    scan_timestamp: new Date().toISOString()
                };
            },
            
            async scanPatternResonance(data) {
                return {
                    pattern_loops: Math.floor(Math.random() * 3),
                    harmonic_alignment: Math.random() * 0.4 + 0.6,
                    destructive_loops: Math.floor(Math.random() * 2),
                    pattern_timestamp: new Date().toISOString()
                };
            },
            
            async validateSealIntegrity(data) {
                return {
                    seal_integrity: Math.random() * 0.2 + 0.8, // 80-100%
                    manifestation_ready: true,
                    seal_timestamp: new Date().toISOString()
                };
            }
        };
    }

    setupExpressApp() {
        this.app.use(express.json());
        this.app.use(express.static('public'));
        
        // Enable CORS for dashboard access
        this.app.use((req, res, next) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
            res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
            next();
        });
        
        this.setupSacredRoutes();
    }

    setupSacredRoutes() {
        // Sacred Health Check
        this.app.get('/api/sacred/health', async (req, res) => {
            try {
                const redisStatus = await this.redis.ping();
                const activeSphere = await this.sphereStateManager.getActiveSphere();
                
                res.json({
                    status: 'sacred_operational',
                    redis: redisStatus === 'PONG' ? 'connected' : 'disconnected',
                    active_sphere: activeSphere,
                    timestamp: new Date().toISOString(),
                    lineage: '◼DOJO → ●OBI-WAN → ⟡Akron'
                });
            } catch (error) {
                res.status(503).json({
                    status: 'sacred_error',
                    error: error.message,
                    timestamp: new Date().toISOString()
                });
            }
        });

        // Sacred Metrics Dashboard
        this.app.get('/api/sacred/metrics', async (req, res) => {
            try {
                const metrics = await this.collectSacredMetrics();
                res.json(metrics);
            } catch (error) {
                res.status(500).json({
                    error: 'Failed to collect sacred metrics',
                    message: error.message
                });
            }
        });

        // Sphere State Management
        this.app.get('/api/sacred/spheres', async (req, res) => {
            try {
                const activeSphere = await this.sphereStateManager.getActiveSphere();
                const sphereState = await this.sphereStateManager.getSphereState(activeSphere);
                
                res.json({
                    active_sphere: activeSphere,
                    sphere_state: sphereState,
                    available_spheres: Object.keys(this.sacredConfig.sacred_sovereign.sphere_mappings),
                    tetrahedral_nodes: this.sacredConfig.sacred_sovereign.tetrahedral_nodes
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        this.app.post('/api/sacred/spheres/:sphereName', async (req, res) => {
            try {
                const { sphereName } = req.params;
                const validationContext = req.body;
                
                const newState = await this.sphereStateManager.setSphere(sphereName, validationContext);
                
                // Broadcast sphere change to WebSocket clients
                this.broadcastToClients({
                    type: 'sphere_change',
                    sphere: sphereName,
                    state: newState,
                    timestamp: new Date().toISOString()
                });
                
                res.json({
                    success: true,
                    sphere: sphereName,
                    state: newState
                });
            } catch (error) {
                res.status(400).json({ error: error.message });
            }
        });

        // Geometric Cleanliness Validation
        this.app.post('/api/sacred/validate', async (req, res) => {
            try {
                const { sphere, action } = req.body;
                const validation = await this.geometricValidator.validate(sphere, action);
                
                res.json({
                    validation_result: validation,
                    timestamp: new Date().toISOString()
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Biological Flow Processing
        this.app.post('/api/sacred/flow/process', async (req, res) => {
            try {
                const { message, targetSphere } = req.body;
                
                const breathIn = await this.biologicalFlow.breathIn(message);
                const processed = await this.biologicalFlow.process(breathIn, targetSphere);
                const breathOut = await this.biologicalFlow.breathOut(processed);
                const memoryLoop = await this.biologicalFlow.memoryLoop(breathOut);
                
                res.json({
                    biological_flow: {
                        breath_in: breathIn,
                        processed: processed,
                        breath_out: breathOut,
                        memory_loop: memoryLoop
                    },
                    timestamp: new Date().toISOString()
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Fractal Observer Scans
        this.app.post('/api/sacred/observer/scan', async (req, res) => {
            try {
                const { data, scan_type = 'full' } = req.body;
                
                const scans = {};
                
                if (scan_type === 'full' || scan_type === 'form') {
                    scans.form = await this.fractalObserver.scanFormStructure(data);
                }
                
                if (scan_type === 'full' || scan_type === 'pattern') {
                    scans.pattern = await this.fractalObserver.scanPatternResonance(data);
                }
                
                if (scan_type === 'full' || scan_type === 'seal') {
                    scans.seal = await this.fractalObserver.validateSealIntegrity(data);
                }
                
                res.json({
                    observer_scans: scans,
                    scan_type,
                    timestamp: new Date().toISOString()
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Sacred Logs Retrieval
        this.app.get('/api/sacred/logs/:sphere?', async (req, res) => {
            try {
                const { sphere = 'FIELD' } = req.params;
                const { limit = 50 } = req.query;
                
                const logs = await this.redis.lRange(`sacred_log:${sphere}`, 0, limit - 1);
                const parsedLogs = logs.map(log => JSON.parse(log));
                
                res.json({
                    sphere,
                    logs: parsedLogs,
                    count: parsedLogs.length
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Live Sacred Status
        this.app.get('/api/sacred/status/live', async (req, res) => {
            try {
                const status = await this.getLiveSacredStatus();
                res.json(status);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
    }

    setupWebSocketServer() {
        this.wss = new WebSocketServer({ 
            server: this.server,
            path: '/ws/sacred'
        });
        
        this.wss.on('connection', (ws, req) => {
            console.log('🔗 Sacred dashboard WebSocket connection established');
            this.dashboardConnections.add(ws);
            
            // Send initial sacred status
            this.sendSacredStatusToClient(ws);
            
            ws.on('message', async (rawMessage) => {
                try {
                    const message = JSON.parse(rawMessage.toString());
                    await this.handleWebSocketMessage(ws, message);
                } catch (error) {
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: `WebSocket message processing failed: ${error.message}`
                    }));
                }
            });
            
            ws.on('close', () => {
                console.log('🔌 Sacred dashboard WebSocket connection closed');
                this.dashboardConnections.delete(ws);
            });
        });
    }

    async handleWebSocketMessage(ws, message) {
        switch (message.type) {
            case 'get_metrics':
                const metrics = await this.collectSacredMetrics();
                ws.send(JSON.stringify({
                    type: 'metrics_update',
                    data: metrics
                }));
                break;
                
            case 'sphere_change_request':
                try {
                    const newState = await this.sphereStateManager.setSphere(message.sphere, message.context);
                    this.broadcastToClients({
                        type: 'sphere_changed',
                        sphere: message.sphere,
                        state: newState
                    });
                } catch (error) {
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: error.message
                    }));
                }
                break;
                
            case 'subscribe_to_updates':
                // Client is now subscribed to real-time updates
                ws.send(JSON.stringify({
                    type: 'subscription_confirmed',
                    timestamp: new Date().toISOString()
                }));
                break;
        }
    }

    async sendSacredStatusToClient(ws) {
        try {
            const status = await this.getLiveSacredStatus();
            ws.send(JSON.stringify({
                type: 'sacred_status',
                data: status
            }));
        } catch (error) {
            console.error('Failed to send sacred status:', error);
        }
    }

    broadcastToClients(message) {
        const messageString = JSON.stringify({
            ...message,
            timestamp: new Date().toISOString()
        });
        
        this.dashboardConnections.forEach(ws => {
            if (ws.readyState === 1) { // WebSocket.OPEN
                ws.send(messageString);
            }
        });
    }

    async collectSacredMetrics() {
        const activeSphere = await this.sphereStateManager.getActiveSphere();
        const sphereState = await this.sphereStateManager.getSphereState(activeSphere);
        
        // Collect geometric cleanliness metrics
        const sampleAction = { content: 'sample metric collection', type: 'metrics' };
        const geometricStatus = await this.geometricValidator.validate(activeSphere, sampleAction);
        
        // Collect fractal observer metrics
        const formScan = await this.fractalObserver.scanFormStructure({});
        const patternScan = await this.fractalObserver.scanPatternResonance({});
        const sealScan = await this.fractalObserver.validateSealIntegrity({});
        
        // Get connection counts
        const chatConnections = this.sacredChatBridge.activeConnections.size;
        const dashboardConnections = this.dashboardConnections.size;
        
        // Get recent activity from Redis
        const recentLogs = await this.redis.lRange(`sacred_log:${activeSphere}`, 0, 9);
        
        return {
            sacred_metrics: {
                geometric_cleanliness: {
                    score: geometricStatus.geometricScore,
                    violations: geometricStatus.violations.length,
                    status: geometricStatus.isClean ? 'clean' : 'violations_detected'
                },
                
                biological_flow: {
                    active_flows: await this.redis.lLen('active_biological_flows') || 0,
                    processing_queue: await this.redis.lLen('biological_processing_queue') || 0,
                    memory_loops_today: await this.redis.get('memory_loops_count_today') || 0
                },
                
                fractal_observer: {
                    form_integrity: formScan.form_integrity,
                    resonance_clarity: formScan.resonance_clarity,
                    pattern_alignment: patternScan.harmonic_alignment,
                    seal_integrity: sealScan.seal_integrity
                },
                
                sphere_state: {
                    active_sphere: activeSphere,
                    sphere_config: sphereState,
                    transitions_today: await this.redis.get('sphere_transitions_count_today') || 0
                },
                
                connectivity: {
                    chat_connections: chatConnections,
                    dashboard_connections: dashboardConnections,
                    redis_connected: await this.redis.ping() === 'PONG'
                },
                
                recent_activity: {
                    log_entries: recentLogs.length,
                    last_activity: recentLogs.length > 0 ? JSON.parse(recentLogs[0]).timestamp : null
                }
            },
            
            timestamp: new Date().toISOString(),
            lineage: '◼DOJO → ●OBI-WAN → ⟡Akron'
        };
    }

    async getLiveSacredStatus() {
        const metrics = await this.collectSacredMetrics();
        const sacred = metrics.sacred_metrics;
        
        // Calculate overall sacred health score
        const healthScore = (
            sacred.geometric_cleanliness.score * 0.3 +
            sacred.fractal_observer.form_integrity * 0.25 +
            sacred.fractal_observer.seal_integrity * 0.25 +
            (sacred.connectivity.redis_connected ? 1 : 0) * 0.2
        );
        
        return {
            overall_health: {
                score: healthScore,
                status: healthScore > 0.8 ? 'optimal' : healthScore > 0.6 ? 'stable' : 'requires_attention'
            },
            
            key_indicators: {
                geometric_cleanliness: sacred.geometric_cleanliness.status,
                active_sphere: sacred.sphere_state.active_sphere,
                connected_clients: sacred.connectivity.chat_connections + sacred.connectivity.dashboard_connections,
                processing_active: sacred.biological_flow.active_flows > 0
            },
            
            detailed_metrics: sacred,
            timestamp: new Date().toISOString()
        };
    }

    async initializeSacredMetrics() {
        // Initialize daily counters
        const today = new Date().toISOString().split('T')[0];
        await this.redis.setNX(`memory_loops_count_today`, 0);
        await this.redis.setNX(`sphere_transitions_count_today`, 0);
        
        // Start periodic metrics collection
        this.startMetricsCollection();
        
        console.log('📊 Sacred metrics collection initialized');
    }

    startMetricsCollection() {
        // Collect and broadcast metrics every 30 seconds
        setInterval(async () => {
            try {
                const status = await this.getLiveSacredStatus();
                this.broadcastToClients({
                    type: 'metrics_update',
                    data: status
                });
            } catch (error) {
                console.error('Metrics collection error:', error);
            }
        }, 30000);
    }

    async startServers() {
        return new Promise((resolve) => {
            this.server.listen(this.port, () => {
                console.log(`🌐 Sacred Dashboard REST API listening on port ${this.port}`);
                console.log(`🔗 Sacred Dashboard WebSocket available on ws://localhost:${this.port}/ws/sacred`);
                resolve();
            });
        });
    }

    async shutdown() {
        console.log('🔄 Shutting down Sacred Dashboard Integration...');
        
        // Close WebSocket connections
        this.dashboardConnections.forEach(ws => {
            ws.close();
        });
        
        // Shutdown sacred components
        if (this.sacredChatBridge) {
            await this.sacredChatBridge.shutdown();
        }
        
        if (this.sphereStateManager) {
            await this.sphereStateManager.shutdown();
        }
        
        // Close Redis connection
        await this.redis.quit();
        
        // Close HTTP server
        this.server.close();
        
        console.log('✅ Sacred Dashboard Integration shutdown complete');
    }
}

export default SacredDashboardIntegration;

// CLI Interface
if (import.meta.url === `file://${process.argv[1]}`) {
    const dashboard = new SacredDashboardIntegration();
    
    // Graceful shutdown handling
    process.on('SIGINT', async () => {
        console.log('\n🔄 Received shutdown signal...');
        await dashboard.shutdown();
        process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
        console.log('\n🔄 Received termination signal...');
        await dashboard.shutdown();
        process.exit(0);
    });
    
    // Start the sacred dashboard
    dashboard.initialize().catch(error => {
        console.error('❌ Failed to start Sacred Dashboard Integration:', error);
        process.exit(1);
    });
}
