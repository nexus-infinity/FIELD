---
symbol: ◼
origin: ~/FIELD/◼DOJO/
created: 2025-01-27T21:30:00+10:00
geometry: tetrahedral-manifest
lineage: ⟡Akron > FIELD > DOJO
---

import Redis from 'redis';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * SacredSphereStateManager - Manages sacred sphere transitions and state
 * Extends base sphere management with sacred validation and geometric alignment
 */
class SacredSphereStateManager {
    constructor() {
        this.redis = Redis.createClient();
        this.fileHeaderGenerator = new SacredFileHeaderGenerator();
        this.geometricValidator = null; // Will be injected
        this.timezone = '+10:00';
        
        this.sacredMapping = {
            spheres: {
                'AKRON': {
                    path: '/Volumes/Akron/',
                    symbol: '⟡',
                    latitude: 0,
                    longitude: '00:00:00',
                    purity: 'immutable',
                    access_level: 'archive_only',
                    color: '⚪'
                },
                'FIELD': {
                    path: '~/FIELD/',
                    symbol: '⚪',
                    latitude: 90,
                    longitude: 'runtime_rotation',
                    purity: 'sacred',
                    access_level: 'manifestation',
                    color: '🟦'
                },
                'FIELD_LIVING': {
                    path: '~/FIELD-LIVING/',
                    symbol: '⚪',
                    latitude: 'variable',
                    longitude: 'temporal_flow',
                    purity: 'mirror_decay',
                    access_level: 'intake_processing',
                    color: '🟡'
                },
                'FIELD_DEV': {
                    path: '~/FIELD-DEV/',
                    symbol: '⚫',
                    latitude: 45,
                    longitude: 'upward_rotation',
                    purity: 'experimental',
                    access_level: 'validation_testing',
                    color: '🟩'
                }
            },
            tetrahedral_core: {
                '▲': { node: 'ATLAS', function: 'tooling_validation', path: '~/FIELD/▲ATLAS/' },
                '▼': { node: 'TATA', function: 'temporal_truth', path: '~/FIELD/▼TATA/' },
                '●': { node: 'OBI-WAN', function: 'living_memory', path: '~/FIELD/●OBI-WAN/' },
                '◼': { node: 'DOJO', function: 'manifestation', path: '~/FIELD/◼DOJO/' }
            }
        };
    }

    async initialize() {
        if (!this.redis.isOpen) {
            await this.redis.connect();
        }
        
        // Initialize default sacred sphere
        const currentSphere = await this.redis.get('active_sphere');
        if (!currentSphere) {
            await this.redis.set('active_sphere', 'FIELD');
            console.log('🔮 Initialized default sacred sphere: FIELD');
        }
        
        await this.initializeSphereStates();
        console.log('✅ SacredSphereStateManager initialized');
    }

    async initializeSphereStates() {
        for (const [sphereName, config] of Object.entries(this.sacredMapping.spheres)) {
            await this.redis.hSet(`sphere_state:${sphereName}`, {
                symbol: config.symbol,
                path: config.path,
                latitude: config.latitude.toString(),
                longitude: config.longitude.toString(),
                purity: config.purity,
                access_level: config.access_level,
                color: config.color,
                last_accessed: new Date().toISOString()
            });
        }
    }

    async getActiveSphere() {
        return await this.redis.get('active_sphere') || 'FIELD';
    }

    async setSphere(sphereName, validationContext = null) {
        if (!this.sacredMapping.spheres[sphereName]) {
            throw new Error(`Sacred sphere '${sphereName}' not found in sacred mapping`);
        }

        // Validate sphere transition if geometric validator is available
        if (this.geometricValidator && validationContext) {
            const transitionValidation = await this.validateSphereTransition(sphereName, validationContext);
            if (!transitionValidation.isValid) {
                throw new Error(`Sphere transition blocked: ${transitionValidation.violations.join(', ')}`);
            }
        }

        const previousSphere = await this.getActiveSphere();
        await this.redis.set('active_sphere', sphereName);
        await this.manifestSphereChange(sphereName, previousSphere);
        
        console.log(`🌀 Sacred sphere transition: ${previousSphere} → ${sphereName}`);
        return await this.getSphereState(sphereName);
    }

    async manifestSphereChange(newSphere, previousSphere) {
        const config = this.sacredMapping.spheres[newSphere];
        const timestamp = new Date().toISOString();
        
        // Update sphere configuration in Redis
        await this.redis.hSet('current_sphere_config', {
            sphere: newSphere,
            symbol: config.symbol,
            path: config.path,
            purity: config.purity,
            access_level: config.access_level,
            color: config.color,
            latitude: config.latitude.toString(),
            longitude: config.longitude.toString(),
            transitioned_from: previousSphere,
            timestamp
        });

        // Log sphere transition
        const transitionEntry = {
            type: 'sphere_transition',
            from_sphere: previousSphere,
            to_sphere: newSphere,
            config: config,
            timestamp,
            lineage: '◼DOJO → ●OBI-WAN → ⟡Akron'
        };

        await this.redis.lPush('sacred_transitions', JSON.stringify(transitionEntry));
        await this.logSphereTransition(transitionEntry);
    }

    async getSphereState(sphereName) {
        if (!sphereName) {
            sphereName = await this.getActiveSphere();
        }

        const state = await this.redis.hGetAll(`sphere_state:${sphereName}`);
        if (!state || Object.keys(state).length === 0) {
            return this.sacredMapping.spheres[sphereName] || null;
        }

        return {
            ...state,
            latitude: isNaN(state.latitude) ? state.latitude : parseFloat(state.latitude),
            longitude: state.longitude
        };
    }

    async manifestInSacredSphere(sphereName, action) {
        // Validate geometric cleanliness before manifestation
        if (this.geometricValidator) {
            const cleanlinessCheck = await this.geometricValidator.validate(sphereName, action);
            if (!cleanlinessCheck.isClean) {
                throw new Error(`Geometric violation: ${cleanlinessCheck.violations.join(', ')}`);
            }
        }

        // Get sacred sphere configuration
        const sacredConfig = this.sacredMapping.spheres[sphereName];
        if (!sacredConfig) {
            throw new Error(`Sphere ${sphereName} not found in sacred mapping`);
        }

        // Execute based on purity level
        switch (sacredConfig.purity) {
            case 'immutable':
                return await this.archiveOnlyAccess(action);
            case 'sacred':
                return await this.sacredManifestation(action, sacredConfig);
            case 'mirror_decay':
                return await this.temporaryProcessing(action, sacredConfig);
            case 'experimental':
                return await this.validationTesting(action, sacredConfig);
            default:
                throw new Error(`Unknown purity level: ${sacredConfig.purity}`);
        }
    }

    async sacredManifestation(action, config) {
        // Ensure action has proper symbolic validation
        const symbol = this.extractActionSymbol(action);
        if (!['▲', '▼', '●', '◼'].includes(symbol)) {
            throw new Error('Action lacks sacred symbolic alignment');
        }

        // Route to appropriate tetrahedral node
        const nodeConfig = this.sacredMapping.tetrahedral_core[symbol];
        const manifestationPath = nodeConfig.path;

        // Create sacred file with proper header if needed
        if (action.type === 'create_file') {
            const sacredHeader = this.fileHeaderGenerator.generateSacredHeader(
                symbol, 
                manifestationPath
            );
            action.content = sacredHeader + '\n\n' + action.content;
        }

        return await this.executeInPath(manifestationPath, action);
    }

    async temporaryProcessing(action, config) {
        // FIELD-LIVING processing with decay timer
        const decayTimer = 24 * 60 * 60 * 1000; // 24 hours
        
        await this.redis.setEx(
            `field_living:${action.id}`, 
            decayTimer / 1000, 
            JSON.stringify(action)
        );

        // Mark for potential elevation to sacred FIELD
        if (action.elevation_candidate) {
            await this.queueForSacredElevation(action);
        }

        return await this.executeInPath(config.path, action);
    }

    async validateSphereTransition(targetSphere, context) {
        const currentSphere = await this.getActiveSphere();
        const violations = [];

        // Check for valid transition paths
        const validTransitions = {
            'AKRON': [], // Archive is immutable, no transitions out
            'FIELD_LIVING': ['FIELD_DEV', 'FIELD'], // Can elevate to dev or sacred
            'FIELD_DEV': ['FIELD', 'FIELD_LIVING'], // Can elevate to sacred or decay
            'FIELD': ['FIELD_DEV', 'AKRON'] // Can test or archive
        };

        if (!validTransitions[currentSphere]?.includes(targetSphere) && currentSphere !== targetSphere) {
            violations.push(`Invalid transition: ${currentSphere} → ${targetSphere}`);
        }

        // Check context requirements
        if (targetSphere === 'AKRON' && !context?.archival_ready) {
            violations.push('Archival context required for AKRON access');
        }

        return {
            isValid: violations.length === 0,
            violations,
            current_sphere: currentSphere,
            target_sphere: targetSphere
        };
    }

    extractActionSymbol(action) {
        // Extract symbolic intent from action
        const symbolPatterns = {
            '▲': ['tool', 'validate', 'atlas', 'agent'],
            '▼': ['log', 'time', 'truth', 'tata'],
            '●': ['memory', 'sync', 'obi-wan', 'observe'],
            '◼': ['manifest', 'execute', 'dojo', 'action']
        };

        for (const [symbol, patterns] of Object.entries(symbolPatterns)) {
            if (patterns.some(pattern => 
                action.content?.toLowerCase().includes(pattern) ||
                action.type?.toLowerCase().includes(pattern)
            )) {
                return symbol;
            }
        }

        return null;
    }

    async executeInPath(manifestationPath, action) {
        // Placeholder for path-specific execution
        return {
            path: manifestationPath,
            action: action,
            status: 'executed',
            timestamp: new Date().toISOString()
        };
    }

    async queueForSacredElevation(action) {
        await this.redis.lPush('sacred_elevation_queue', JSON.stringify({
            action,
            timestamp: new Date().toISOString(),
            status: 'pending_elevation'
        }));
    }

    async logSphereTransition(transitionEntry) {
        const logPath = path.join(process.env.HOME, 'FIELD', '◼DOJO', 'sphere-transitions');
        await fs.mkdir(logPath, { recursive: true });
        
        const filename = `transitions-${new Date().toISOString().split('T')[0]}.log`;
        await fs.appendFile(path.join(logPath, filename), JSON.stringify(transitionEntry) + '\n');
    }

    setGeometricValidator(validator) {
        this.geometricValidator = validator;
    }

    async shutdown() {
        if (this.redis.isOpen) {
            await this.redis.quit();
        }
    }
}

/**
 * SacredFileHeaderGenerator - Creates sacred headers for manifested files
 */
class SacredFileHeaderGenerator {
    constructor() {
        this.timezone = '+10:00';
    }

    generateSacredHeader(symbol, originPath, geometryType = 'tetrahedral-manifest') {
        const timestamp = new Date().toISOString().replace('Z', this.timezone);
        const lineage = this.generateLineage(originPath);
        
        return `---
symbol: ${symbol}
origin: ${originPath}
created: ${timestamp}
geometry: ${geometryType}
lineage: ${lineage}
---`;
    }

    generateLineage(originPath) {
        if (originPath.includes('FIELD-LIVING')) {
            return '⟡Akron > FIELD-LIVING > FIELD > DOJO';
        } else if (originPath.includes('FIELD-DEV')) {
            return '⟡Akron > FIELD-DEV > FIELD > DOJO';
        } else if (originPath.includes('~/FIELD/')) {
            return '⟡Akron > FIELD > DOJO';
        }
        return '⟡Akron > FIELD';
    }

    validateSacredFile(fileContent) {
        const requiredFields = ['symbol:', 'origin:', 'created:', 'geometry:', 'lineage:'];
        const header = fileContent.split('---')[1];
        
        return requiredFields.every(field => 
            header && header.includes(field)
        );
    }
}

export default SacredSphereStateManager;
export { SacredFileHeaderGenerator };
