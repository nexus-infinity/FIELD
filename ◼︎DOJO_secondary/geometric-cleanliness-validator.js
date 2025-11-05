---
symbol: ◼
origin: ~/FIELD/◼DOJO/
created: 2025-01-27T21:30:00+10:00
geometry: tetrahedral-manifest
lineage: ⟡Akron > FIELD > DOJO
---

import { promises as fs } from 'fs';
import path from 'path';
import Redis from 'redis';

/**
 * GeometricCleanlinessValidator - Validates geometric cleanliness and sacred patterns
 * Prevents duplicated logic, unauthorized agents, and maintains symbolic alignment
 */
class GeometricCleanlinessValidator {
    constructor() {
        this.redis = Redis.createClient();
        
        this.prohibitedPatterns = [
            'duplicated_logic',
            'unauthorized_launch_agent',
            'unverified_binary',
            'parasitic_execution',
            'profane_commands',
            'geometric_violation'
        ];

        this.profaneCommands = [
            'rm -rf /',
            'sudo rm -rf',
            'DELETE FROM users',
            'DROP TABLE',
            'DROP DATABASE',
            'format c:',
            'sudo dd if=/dev/zero',
            'killall -9',
            'sudo halt',
            'sudo poweroff',
            'sudo reboot -f',
            'chmod 777 /',
            'chown root:root /'
        ];

        this.allowedBinaryPaths = [
            '~/FIELD/▲ATLAS/',
            '~/FIELD/◼DOJO/',
            '/usr/local/bin',
            '/usr/bin',
            '/bin'
        ];

        this.geometricPatterns = {
            tetrahedral_valid: ['▲', '▼', '●', '◼'],
            sacred_symbols: ['⟡', '⚪', '⚫'],
            lineage_markers: ['Akron', 'FIELD', 'DOJO', 'OBI-WAN', 'TATA', 'ATLAS']
        };
    }

    async initialize() {
        if (!this.redis.isOpen) {
            await this.redis.connect();
        }
        
        // Initialize validation patterns in Redis
        await this.redis.hSet('validation_patterns', {
            'profane_commands_count': this.profaneCommands.length.toString(),
            'geometric_patterns_loaded': 'true',
            'binary_validation_enabled': 'true',
            'last_updated': new Date().toISOString()
        });
        
        console.log('🔬 GeometricCleanlinessValidator initialized');
    }

    async validate(sphere, action) {
        const violations = [];
        const validationId = `validation_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        try {
            // Check for duplicated logic
            if (await this.checkDuplicatedLogic(action)) {
                violations.push('Duplicated logic detected');
            }

            // Validate binary alignment
            if (action.type === 'execute_binary' || this.containsBinaryExecution(action)) {
                const binaryPath = this.extractBinaryPath(action);
                if (binaryPath && !await this.validateBinaryAlignment(binaryPath)) {
                    violations.push('Binary not mapped to symbolic layer');
                }
            }

            // Check for parasitic agents
            if (await this.detectParasiticAgents(action)) {
                violations.push('Parasitic agent pattern detected');
            }

            // Validate geometric patterns
            if (!this.validateGeometricPatterns(action)) {
                violations.push('Geometric pattern validation failed');
            }

            // Check for profane commands
            if (this.containsProfaneCommands(action)) {
                violations.push('Profane commands detected');
            }

            // Sphere-specific validations
            const sphereViolations = await this.validateSphereSpecificRules(sphere, action);
            violations.push(...sphereViolations);

            const result = {
                isClean: violations.length === 0,
                violations,
                sphere,
                timestamp: new Date().toISOString(),
                validation_id: validationId,
                geometric_score: this.calculateGeometricScore(action, violations.length)
            };

            // Log validation result
            await this.logValidationResult(result);
            
            return result;

        } catch (error) {
            violations.push(`Validation error: ${error.message}`);
            return {
                isClean: false,
                violations,
                sphere,
                timestamp: new Date().toISOString(),
                validation_id: validationId,
                error: error.message
            };
        }
    }

    async checkDuplicatedLogic(action) {
        if (!action.content) return false;

        // Check against known patterns in Redis
        const existingHashes = await this.redis.lRange('content_hashes', 0, -1);
        const actionHash = this.generateContentHash(action.content);

        // Check for exact duplicates
        if (existingHashes.includes(actionHash)) {
            return true;
        }

        // Add new hash to tracking
        await this.redis.lPush('content_hashes', actionHash);
        await this.redis.lTrim('content_hashes', 0, 1000); // Keep last 1000 hashes

        // Check for similar patterns (simplified similarity check)
        const similarityThreshold = 0.8;
        for (const existingHash of existingHashes) {
            const similarity = this.calculateSimilarity(actionHash, existingHash);
            if (similarity > similarityThreshold) {
                return true;
            }
        }

        return false;
    }

    async validateBinaryAlignment(binaryPath) {
        // Ensure binary is mapped through ▲ or ◼ symbolic layers
        const isAllowedPath = this.allowedBinaryPaths.some(path => 
            binaryPath.startsWith(path.replace('~', process.env.HOME || '/Users/jbear'))
        );

        if (!isAllowedPath) {
            return false;
        }

        // Check if binary has symbolic validation in Redis
        const symbolicValidation = await this.redis.hGet('binary_validations', binaryPath);
        return symbolicValidation === 'validated';
    }

    async detectParasiticAgents(action) {
        if (!action.content) return false;

        const parasiticPatterns = [
            /crontab.*rm.*rf/i,
            /launchctl.*load.*plist/i,
            /systemctl.*enable.*service/i,
            /\/tmp\/\.\w+/,
            /chmod\s+\+x.*\/tmp/i,
            /curl.*\|.*bash/i,
            /wget.*-O.*\|.*sh/i,
            /nohup.*&$/m
        ];

        return parasiticPatterns.some(pattern => pattern.test(action.content));
    }

    validateGeometricPatterns(action) {
        if (!action.content) return true;

        const content = action.content;
        
        // Check for presence of sacred geometric patterns
        const hasTetrahedralSymbol = this.geometricPatterns.tetrahedral_valid.some(symbol => 
            content.includes(symbol)
        );

        const hasSacredSymbol = this.geometricPatterns.sacred_symbols.some(symbol => 
            content.includes(symbol)
        );

        const hasLineageMarker = this.geometricPatterns.lineage_markers.some(marker => 
            content.toLowerCase().includes(marker.toLowerCase())
        );

        // For sacred operations, at least one geometric marker is required
        if (action.type === 'sacred_operation' || action.sphere === 'FIELD') {
            return hasTetrahedralSymbol || hasSacredSymbol || hasLineageMarker;
        }

        return true; // Non-sacred operations pass by default
    }

    containsProfaneCommands(action) {
        if (!action.content) return false;

        const content = action.content.toLowerCase();
        return this.profaneCommands.some(command => 
            content.includes(command.toLowerCase())
        );
    }

    async validateSphereSpecificRules(sphere, action) {
        const violations = [];

        switch (sphere) {
            case 'AKRON':
                // Archive sphere - read-only access
                if (action.type && ['write', 'delete', 'modify'].includes(action.type)) {
                    violations.push('Write operations not allowed in AKRON sphere');
                }
                break;

            case 'FIELD_LIVING':
                // Living sphere - temporary operations with decay
                if (!action.decay_timer && action.type === 'persistent_operation') {
                    violations.push('Persistent operations in FIELD_LIVING require decay timer');
                }
                break;

            case 'FIELD_DEV':
                // Development sphere - validation required
                if (action.type === 'deploy' && !action.validation_passed) {
                    violations.push('Deployment in FIELD_DEV requires prior validation');
                }
                break;

            case 'FIELD':
                // Sacred sphere - highest purity requirements
                if (!this.validateSacredPurity(action)) {
                    violations.push('Action does not meet sacred purity requirements');
                }
                break;
        }

        return violations;
    }

    validateSacredPurity(action) {
        // Sacred purity checks
        const purityChecks = [
            action.symbolic_anchor !== undefined,
            action.geometric_validation !== false,
            !this.containsProfaneCommands(action),
            this.validateGeometricPatterns(action)
        ];

        return purityChecks.every(check => check === true);
    }

    containsBinaryExecution(action) {
        if (!action.content) return false;

        const binaryPatterns = [
            /\.\/\w+/,
            /\/usr\/bin\/\w+/,
            /\/usr\/local\/bin\/\w+/,
            /\/bin\/\w+/,
            /exec\(/,
            /system\(/,
            /spawn\(/
        ];

        return binaryPatterns.some(pattern => pattern.test(action.content));
    }

    extractBinaryPath(action) {
        if (!action.content) return null;

        const binaryMatches = action.content.match(/([\/\w\-\.]+\/[\w\-\.]+)/g);
        return binaryMatches ? binaryMatches[0] : null;
    }

    calculateGeometricScore(action, violationCount) {
        let score = 1.0;

        // Deduct for violations
        score -= violationCount * 0.2;

        // Bonus for geometric patterns
        if (action.content) {
            const geometricBonus = this.geometricPatterns.tetrahedral_valid.filter(symbol => 
                action.content.includes(symbol)
            ).length * 0.1;
            score += geometricBonus;
        }

        // Bonus for sacred symbols
        if (action.symbolic_anchor) {
            score += 0.2;
        }

        return Math.max(0, Math.min(1, score));
    }

    generateContentHash(content) {
        // Simple hash generation (in production, use crypto.createHash)
        let hash = 0;
        for (let i = 0; i < content.length; i++) {
            const char = content.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return hash.toString(36);
    }

    calculateSimilarity(hash1, hash2) {
        // Simplified similarity calculation
        const str1 = hash1.toString();
        const str2 = hash2.toString();
        
        if (str1 === str2) return 1;
        
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1;
        
        const editDistance = this.levenshteinDistance(longer, shorter);
        return (longer.length - editDistance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    async logValidationResult(result) {
        // Log to Redis
        await this.redis.lPush('validation_history', JSON.stringify(result));
        await this.redis.lTrim('validation_history', 0, 10000); // Keep last 10k validations

        // Log to file system
        const logPath = path.join(process.env.HOME, 'FIELD', '◼DOJO', 'validation-logs');
        await fs.mkdir(logPath, { recursive: true });
        
        const filename = `geometric-validation-${new Date().toISOString().split('T')[0]}.log`;
        await fs.appendFile(path.join(logPath, filename), JSON.stringify(result) + '\n');

        // Update metrics
        await this.updateValidationMetrics(result);
    }

    async updateValidationMetrics(result) {
        const metricsKey = `validation_metrics:${result.sphere}`;
        const today = new Date().toISOString().split('T')[0];
        
        await this.redis.hIncrBy(`${metricsKey}:${today}`, 'total_validations', 1);
        
        if (result.isClean) {
            await this.redis.hIncrBy(`${metricsKey}:${today}`, 'clean_validations', 1);
        } else {
            await this.redis.hIncrBy(`${metricsKey}:${today}`, 'failed_validations', 1);
        }

        await this.redis.hSet(`${metricsKey}:${today}`, 'last_score', result.geometric_score.toString());
    }

    async getValidationMetrics(sphere, date = null) {
        const targetDate = date || new Date().toISOString().split('T')[0];
        const metricsKey = `validation_metrics:${sphere}:${targetDate}`;
        
        return await this.redis.hGetAll(metricsKey);
    }

    async shutdown() {
        if (this.redis.isOpen) {
            await this.redis.quit();
        }
    }
}

export default GeometricCleanlinessValidator;
