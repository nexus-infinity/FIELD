// SIF Provenance Extension Schema for Master Provenance Graph
// Extends the core provenance schema to support hot-swap module tracking

// ════════════════════════════════════════════════════════════════════════
// 1. SIF-SPECIFIC NODE LABELS
// ════════════════════════════════════════════════════════════════════════

// Extend Artifact node with SIF-specific properties
CREATE CONSTRAINT unique_sif_artifact IF NOT EXISTS 
ON (a:Artifact) ASSERT a.sha256 IS UNIQUE;

// SIF Hot-Swap Process node
CREATE CONSTRAINT unique_hotswap_process IF NOT EXISTS 
ON (p:HotSwapProcess) ASSERT p.uuid IS UNIQUE;

// SIF Runtime State snapshots
CREATE CONSTRAINT unique_runtime_snapshot IF NOT EXISTS 
ON (r:RuntimeSnapshot) ASSERT r.uuid IS UNIQUE;

// ════════════════════════════════════════════════════════════════════════
// 2. SIF GEOMETRY NODES (Extend existing GeometryNode)
// ════════════════════════════════════════════════════════════════════════

// Ensure SIF-specific geometry nodes exist
MERGE (sif:GeometryNode {name: "SIF_ENGINE"})
SET sif.glyph = "🔄",
    sif.properties = ["hot_swap", "dynamic_loading", "sovereignty_check"],
    sif.tetrahedral_position = "DOJO_EXTENSION";

// ════════════════════════════════════════════════════════════════════════
// 3. SIF-SPECIFIC RELATIONSHIPS
// ════════════════════════════════════════════════════════════════════════

// Hot-swap compilation relationship
// (:Artifact)-[:HOT_COMPILED_TO]->(:Artifact)

// Runtime state relationship  
// (:Artifact)-[:RUNTIME_STATE]->(:RuntimeSnapshot)

// Sovereignty verification relationship
// (:Artifact)-[:SIF_VERIFIED_BY]->(:Agent {role:"SIF_Validator"})

// Dynamic loading relationship
// (:Artifact)-[:DYNAMICALLY_LOADED_BY]->(:Process)

// Rollback relationship for failed swaps
// (:Artifact)-[:ROLLBACK_FROM]->(:Artifact)

// ════════════════════════════════════════════════════════════════════════
// 4. SIF-SPECIFIC INDEXES
// ════════════════════════════════════════════════════════════════════════

// Index on hot-swap timestamps for performance
CREATE INDEX sif_hotswap_timestamp IF NOT EXISTS
FOR (p:HotSwapProcess) ON (p.swap_timestamp);

// Index on SIF artifact metatron slots
CREATE INDEX sif_metatron_slot IF NOT EXISTS  
FOR (a:Artifact) ON (a.metatron_slot);

// Index on sovereignty validation status
CREATE INDEX sif_sovereignty_status IF NOT EXISTS
FOR (a:Artifact) ON (a.sovereignty_verified);

// Full-text index for SIF-related paths
CREATE FULLTEXT INDEX sif_path_search IF NOT EXISTS
FOR (a:Artifact) ON (a.path, a.sif_module_name);

// ════════════════════════════════════════════════════════════════════════
// 5. SIF PROVENANCE TRACKING PROCEDURES
// ════════════════════════════════════════════════════════════════════════

// Register hot-swap event
CREATE OR REPLACE FUNCTION sif.registerHotSwap(
    sourceHash STRING,
    targetHash STRING, 
    swapVersion STRING,
    agentName STRING
) RETURNS STRING
AS $$
    MERGE (source:Artifact {sha256: sourceHash})
    MERGE (target:Artifact {sha256: targetHash})
    
    CREATE (swap:HotSwapProcess {
        uuid: apoc.create.uuid(),
        swap_version: swapVersion,
        swap_timestamp: datetime(),
        tetrahedral_flow: ["OB1", "TATA", "ATLAS", "DOJO"],
        metatron_alignment: "SIF_HotSwap"
    })
    
    MERGE (agent:Agent {name: agentName})
    SET agent.role = "SIF_Engine",
        agent.sovereignty = "native"
    
    CREATE (target)-[:HOT_COMPILED_FROM]->(source)
    CREATE (swap)-[:COMPILED]->(target)
    CREATE (swap)-[:RUN_BY]->(agent)
    
    RETURN swap.uuid
$$;

// Verify sovereignty chain for SIF modules
CREATE OR REPLACE FUNCTION sif.verifySovereigntyChain(artifactHash STRING)
RETURNS MAP
AS $$
    MATCH (a:Artifact {sha256: artifactHash})
    
    // Check for unverified external influences
    OPTIONAL MATCH path = (a)<-[:DERIVED_FROM|INFLUENCED_BY*0..5]-(influence:Artifact {sovereignty: 'influence'})
    WHERE NOT EXISTS {
        MATCH (influence)-[:VERIFIED_BY]->(:Agent {role: 'TATA'})
    }
    
    // Check for suspicious write-back patterns
    OPTIONAL MATCH writeBack = (a)-[:DERIVED_FROM]->(native:Artifact {sovereignty: 'native'})
    WHERE a.sovereignty = 'influence'
    
    RETURN {
        artifact_hash: artifactHash,
        sovereignty_status: a.sovereignty,
        unverified_influences: count(DISTINCT influence),
        suspicious_writebacks: count(DISTINCT writeBack),
        verification_required: count(DISTINCT influence) > 0 OR count(DISTINCT writeBack) > 0,
        last_verified: a.last_verified,
        risk_level: CASE 
            WHEN count(DISTINCT influence) = 0 AND count(DISTINCT writeBack) = 0 THEN "LOW"
            WHEN count(DISTINCT influence) <= 2 AND count(DISTINCT writeBack) = 0 THEN "MEDIUM" 
            ELSE "HIGH"
        END
    }
$$;

// Generate SIF module lineage tree
CREATE OR REPLACE FUNCTION sif.generateLineageTree(artifactHash STRING)
RETURNS LIST<MAP>
AS $$
    MATCH (n:Artifact {sha256: artifactHash})
    OPTIONAL MATCH path = (n)-[:DERIVED_FROM|GENERATED_BY|HOT_COMPILED_FROM*0..10]->(root)
    WITH collect(DISTINCT path) AS paths
    
    // Convert to tree structure with SIF-specific metadata
    RETURN [p IN paths | {
        path_length: length(p),
        nodes: [node IN nodes(p) | {
            uuid: node.uuid,
            sha256: CASE WHEN node:Artifact THEN node.sha256 ELSE null END,
            type: labels(node)[0],
            sovereignty: CASE WHEN node:Artifact THEN node.sovereignty ELSE null END,
            sif_module: CASE WHEN node:Artifact THEN node.sif_module_name ELSE null END,
            metatron_slot: CASE WHEN node:Artifact THEN node.metatron_slot ELSE null END
        }],
        relationships: [rel IN relationships(p) | type(rel)]
    }]
$$;

// Detect anomalous hot-swap patterns
CREATE OR REPLACE FUNCTION sif.detectAnomalies()
RETURNS LIST<MAP>
AS $$
    // Pattern 1: Too many hot-swaps in short time window
    MATCH (swap:HotSwapProcess)
    WHERE swap.swap_timestamp > datetime() - duration({hours: 1})
    WITH count(swap) as recent_swaps
    
    // Pattern 2: External influence without TATA verification  
    MATCH (ext:Artifact {sovereignty: 'influence'})-[:INFLUENCED_BY]->(target:Artifact)
    WHERE NOT EXISTS {
        MATCH (target)-[:VERIFIED_BY]->(:Agent {role: 'TATA'})
    }
    
    // Pattern 3: Compilation failures followed by successful swaps
    MATCH (failed:HotSwapProcess {status: 'failed'}),
          (success:HotSwapProcess {status: 'success'})
    WHERE success.swap_timestamp > failed.swap_timestamp
    AND duration.between(failed.swap_timestamp, success.swap_timestamp).minutes < 10
    
    RETURN [
        {
            type: "HIGH_FREQUENCY_SWAPS",
            count: recent_swaps,
            severity: CASE WHEN recent_swaps > 10 THEN "HIGH" ELSE "MEDIUM" END
        },
        {
            type: "UNVERIFIED_EXTERNAL_INFLUENCE", 
            count: count(DISTINCT target),
            severity: "HIGH"
        },
        {
            type: "RAPID_RETRY_PATTERN",
            count: count(DISTINCT success),
            severity: "MEDIUM"
        }
    ]
$$;

// ════════════════════════════════════════════════════════════════════════
// 6. SIF WITNESS LOG INTEGRATION
// ════════════════════════════════════════════════════════════════════════

// Create witness log entries for OBI-WAN integration
CREATE OR REPLACE PROCEDURE sif.recordWitnessEvent(
    event STRING,
    artifactHash STRING,
    metadata MAP
) 
YIELD witnessId
AS $$
    CREATE (witness:WitnessLog {
        uuid: apoc.create.uuid(),
        event_type: event,
        artifact_hash: artifactHash,
        timestamp: datetime(),
        metadata: metadata,
        geometry_node: "OBI-WAN",
        sif_related: true
    })
    
    // Link to the artifact
    MATCH (artifact:Artifact {sha256: artifactHash})
    CREATE (witness)-[:WITNESSES]->(artifact)
    
    RETURN witness.uuid as witnessId
$$;

// ════════════════════════════════════════════════════════════════════════
// 7. SIF SECURITY QUERIES
// ════════════════════════════════════════════════════════════════════════

// Query: Find all hot-swapped modules in the last 24 hours
// MATCH (swap:HotSwapProcess)
// WHERE swap.swap_timestamp > datetime() - duration({hours: 24})
// MATCH (swap)-[:COMPILED]->(lib:Artifact)
// RETURN lib.path, lib.sha256, swap.swap_version, swap.swap_timestamp
// ORDER BY swap.swap_timestamp DESC;

// Query: Detect potential security violations in SIF
// MATCH (artifact:Artifact)-[:HOT_COMPILED_FROM]->(source:Artifact)
// WHERE artifact.sovereignty = 'influence' 
// AND source.sovereignty = 'native'
// AND NOT EXISTS {
//     MATCH (artifact)-[:SIF_VERIFIED_BY]->(:Agent {role: 'SIF_Validator'})
// }
// RETURN artifact.sha256, source.sha256, artifact.path
// ORDER BY artifact.created_at DESC;

// Query: Generate complete SIF audit trail
// MATCH path = (lib:Artifact)-[:HOT_COMPILED_FROM|DERIVED_FROM*]-(source:Artifact)
// WHERE lib.metatron_slot = 'SIF-Runtime'
// WITH path, length(path) as depth
// ORDER BY depth DESC
// RETURN path LIMIT 50;

// ════════════════════════════════════════════════════════════════════════
// 8. INITIALIZATION DATA
// ════════════════════════════════════════════════════════════════════════

// Create initial SIF agents
MERGE (sif_engine:Agent {name: "SIF_HotSwap_Engine"})
SET sif_engine.role = "SIF_Engine",
    sif_engine.sovereignty = "native",
    sif_engine.geometry_node = "DOJO",
    sif_engine.capabilities = ["hot_compilation", "sovereignty_check", "rollback"];

MERGE (sif_validator:Agent {name: "SIF_Validator"}) 
SET sif_validator.role = "SIF_Validator",
    sif_validator.sovereignty = "native",
    sif_validator.geometry_node = "TATA",
    sif_validator.capabilities = ["sovereignty_verification", "pattern_detection", "security_audit"];

// Link SIF agents to their geometry nodes
MATCH (sif_engine:Agent {name: "SIF_HotSwap_Engine"})
MATCH (dojo:GeometryNode {name: "DOJO"})
MERGE (sif_engine)-[:OPERATES_FROM]->(dojo);

MATCH (sif_validator:Agent {name: "SIF_Validator"})
MATCH (tata:GeometryNode {name: "TATA"})  
MERGE (sif_validator)-[:OPERATES_FROM]->(tata);

// ════════════════════════════════════════════════════════════════════════
// SCHEMA EXTENSION COMPLETE
// ════════════════════════════════════════════════════════════════════════
