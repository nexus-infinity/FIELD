---
symbol: ◼
origin: ~/FIELD/◼DOJO/
created: 2025-01-27T21:30:00+10:00
geometry: tetrahedral-manifest
lineage: ⟡Akron > FIELD > DOJO
---

import SacredChatBridge from './sacred-chat-bridge.js';
import SacredSphereStateManager from './sacred-sphere-manager.js';
import GeometricCleanlinessValidator from './geometric-cleanliness-validator.js';
import BiologicalFlowProcessor from './biological-flow-processor.js';

/**
 * Sacred Chat Bridge System Integration
 * Mediates all interactive sessions through proper geometric checks and sacred flow
 */

class SacredChatBridgeSystem {
    constructor() {
        this.sacredChatBridge = null;
        this.isInitialized = false;
        this.shutdownHandlers = [];
    }

    async initialize() {
        if (this.isInitialized) {
            console.log('🔄 SacredChatBridge system already initialized');
            return;
        }

        console.log('🌟 Initializing SacredChatBridge system...');

        try {
            // Create and wire all components
            const geometricValidator = new GeometricCleanlinessValidator();
            const sacredSphereManager = new SacredSphereStateManager();
            const biologicalFlowProcessor = new BiologicalFlowProcessor();
            
            // Initialize components
            await geometricValidator.initialize();
            await sacredSphereManager.initialize();
            await biologicalFlowProcessor.initialize();
            
            // Wire dependencies
            sacredSphereManager.setGeometricValidator(geometricValidator);
            
            // Create and initialize main bridge
            this.sacredChatBridge = new SacredChatBridge();
            
            // Inject dependencies
            this.sacredChatBridge.geometricValidator = geometricValidator;
            this.sacredChatBridge.sacredSphereManager = sacredSphereManager;
            this.sacredChatBridge.biologicalFlow = biologicalFlowProcessor;
            
            // Initialize main bridge
            await this.sacredChatBridge.initialize();
            
            // Register shutdown handlers
            this.registerShutdownHandlers();
            
            this.isInitialized = true;
            console.log('✅ SacredChatBridge system fully manifested');
            console.log('🌐 WebSocket server: ws://localhost:8080');
            console.log('🔐 Sacred validation: ENABLED');
            console.log('🌊 Biological flow: ACTIVE');
            console.log('🔬 Geometric cleanliness: ENFORCED');

        } catch (error) {
            console.error('❌ SacredChatBridge system initialization failed:', error);
            throw error;
        }
    }

    registerShutdownHandlers() {
        // Register graceful shutdown for various signals
        const shutdown = async (signal) => {
            console.log(`\n🔄 Received ${signal}, shutting down SacredChatBridge system...`);
            await this.shutdown();
            process.exit(0);
        };

        process.on('SIGINT', shutdown);
        process.on('SIGTERM', shutdown);
        process.on('SIGUSR2', shutdown); // For nodemon

        // Register cleanup handlers
        this.shutdownHandlers.push(() => this.sacredChatBridge?.shutdown());
        this.shutdownHandlers.push(() => this.sacredChatBridge?.geometricValidator?.shutdown());
        this.shutdownHandlers.push(() => this.sacredChatBridge?.sacredSphereManager?.shutdown());
        this.shutdownHandlers.push(() => this.sacredChatBridge?.biologicalFlow?.shutdown());
    }

    async shutdown() {
        if (!this.isInitialized) return;

        console.log('🔄 Shutting down SacredChatBridge system...');

        for (const handler of this.shutdownHandlers) {
            try {
                await handler();
            } catch (error) {
                console.error('Warning: Shutdown handler failed:', error.message);
            }
        }

        this.isInitialized = false;
        console.log('✅ SacredChatBridge system shutdown complete');
    }

    async getSystemStatus() {
        if (!this.isInitialized) {
            return { status: 'not_initialized' };
        }

        try {
            const redis = this.sacredChatBridge.redis;
            const activeConnections = this.sacredChatBridge.activeConnections.size;
            const activeSphere = await redis.get('active_sphere');
            const flowState = await redis.hGetAll('biological_flow_state');
            
            return {
                status: 'active',
                active_connections: activeConnections,
                active_sphere: activeSphere,
                flow_state: flowState,
                websocket_port: 8080,
                sacred_validation: 'enabled',
                geometric_cleanliness: 'enforced',
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                status: 'error',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async switchSphere(sphereName) {
        if (!this.isInitialized) {
            throw new Error('System not initialized');
        }

        return await this.sacredChatBridge.sacredSphereManager.setSphere(sphereName);
    }

    async validateMessage(message, sphere) {
        if (!this.isInitialized) {
            throw new Error('System not initialized');
        }

        return await this.sacredChatBridge.geometricValidator.validate(sphere, message);
    }

    async processFlow(message) {
        if (!this.isInitialized) {
            throw new Error('System not initialized');
        }

        const flow = this.sacredChatBridge.biologicalFlow;
        
        // Full biological flow cycle
        const breathIn = await flow.breathIn(message);
        const processed = await flow.process(breathIn, 'FIELD');
        const breathOut = await flow.breathOut(processed);
        const memoryLoop = await flow.memoryLoop(breathOut);

        return {
            flow_id: breathIn.flow_id,
            stages_completed: ['breathIn', 'process', 'breathOut', 'memoryLoop'],
            final_manifestation: breathOut.manifestation,
            memory_entry: memoryLoop,
            lineage: memoryLoop.lineage
        };
    }
}

// Export system for programmatic use
const sacredChatBridgeSystem = new SacredChatBridgeSystem();

// Auto-initialize if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
    (async () => {
        try {
            await sacredChatBridgeSystem.initialize();
            
            // Keep process alive
            console.log('🔄 SacredChatBridge system running. Press Ctrl+C to stop.');
            
            // Optional: Provide basic CLI interface
            if (process.argv.includes('--status')) {
                const status = await sacredChatBridgeSystem.getSystemStatus();
                console.log('📊 System Status:', JSON.stringify(status, null, 2));
            }
            
        } catch (error) {
            console.error('❌ Failed to start SacredChatBridge system:', error);
            process.exit(1);
        }
    })();
}

export default SacredChatBridgeSystem;
export { sacredChatBridgeSystem };
