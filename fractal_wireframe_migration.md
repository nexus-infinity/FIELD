# Fractal Wireframe Migration Plan

This document coordinates the realignment of the FIELD sacred domains with the **Fractal Field Wireframe v1.7** geometry. It records the current landscape, the canonical target structure, and the staged actions needed to migrate safely without breaking existing flows.

---

## Migration Principles

- **Observer → Architect → Weaver cycle**: inventory first, map decisions second, execute in staged batches third, then validate and memorialise.
- **Resident harmony**: no destructive moves without a 48 h observation window. Use symlinks or staging folders while the field validates the new geometry.
- **Lineage preservation**: every move records origin, target, intention, and validation timestamp.
- **Validation before lock-in**: `field_validate --check-intentions --recursive` must pass after each batch.
- **Canonical naming rule**: every petal directory keeps the sacred glyph followed by an underscore and the descriptor (e.g. `◎_source_core`). When migrating, ensure the underscore remains; do not collapse names into `◎source_core` or insert additional separators.

---

## Global Checklist

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Capture pre-migration manifests (`fd -td '' .`) for each domain |  | ☐ | Store in `/Users/jbear/FIELD/<domain>/STAGING/_inventories/` |
| Approve `/Volumes/Akron/●_REDUCTION_WORKSPACE/REDUCTION_RECOMMENDATIONS.json` |  | ☐ | Needed to free staging space |
| Create canonical petal shells in every domain |  | ☐ | Use directories listed in Target Geometry sections |
| Draft routing tables (this document) |  | ☑ | Initial pass complete (rev 2025-11-02) |
| Stage pilot migration batch |  | ☐ | Recommend smallest legacy folder per domain |
| Run validation suite after each batch |  | ☐ | `field_validate`, symlink check, broken reference scan |
| Archive or purge superseded legacy shells |  | ☐ | Only after validation + observation window |

---

## ▼ TATA — Truth / Law / Temporal Gravity

### Target Geometry (v1.7)

```
▼TATA/
 ├── ◎source_core/
 │    ├── ⬣axioms_foundational/
 │    └── ⬣legacy_data_anchors/
 ├── ▲integrity_structure/
 │    ├── ⬣legal_trust_structures/
 │    └── ⬰compliance_verification_logs/
 ├── ⭟verification_vessel/
 │    ├── ⬣certified_artifacts_evidence/
 │    └── ✶verification_protocols_output/
 ├── ⬢temporal_records/
 │    ├── ⬘chronological_event_logs/
 │    └── ⬘lineage_succession_data/
 ├── ✦sovereign_wisdom/
 │    ├── ✶legal_ethical_frameworks/
 │    └── ⬖governance_interfaces/
 └── ⭣registry/
      ├── tata_registry.json
      └── README.md
```

### Current Variance Snapshot (2025‑11‑02)

- Legacy scaffolding (`_pulse`, `_vault`, multiple `P#_*`, `△_integrity_structure`, `◎_source`) coexists with target petals.
- Duplicate registries (`⭣_registry`, `⭣_79_manifest`, `⭣_void`) and staging folders without canonical names.
- Functional collections (e.g., `legal_intelligence`, `VERIFIED`, `archives`) require mapping into the petal lattice.

### Routing Table (Draft)

| Legacy Path | Target Petal | Action | Notes |
|-------------|--------------|--------|-------|
| `_pulse/`, `_reflection/`, `_vault/` | Distribute contents across all petals | Stage → review → merge | Keep temporal logs with timestamps in `⬢temporal_records` |
| `P1_manifest/`, `P2_intake/`, `P3_alignment/` etc. | Case-by-case | Stage | Map using prior P# ↔ petal chart (appendix A) |
| `legal_intelligence/`, `legal_documents/`, `VLSB (legal-Board)/` | ▲integrity_structure/⬣legal_trust_structures/ | Stage, then move | Preserve folder structure inside new petal |
| `VERIFIED/`, `P5_certified/`, `_verification` | ⭟verification_vessel/ | Merge subfolders | Create `README` noting verification provenance |
| `timelines/`, `JR/`, `P11_reports/`, `_temporal_records/` | ⬢temporal_records/ | Rename + consolidate | Chronological logs to `⬘chronological_event_logs` |
| `✦_wisdom/`, `≛_wisdom/`, `✦_47_sovereign/` | ✦sovereign_wisdom/ | Combine | Ensure ethical frameworks vs interfaces separated |
| `⭣_79_manifest/`, `⭣_void/` | ⭣registry/ | Archive or merge | Move final inventories into canonical registry |

### Execution Notes

- Create `/Users/jbear/FIELD/▼TATA/STAGING/` for interim placement.
- After each move, update `⭣_registry/README.md` with lineage entries.
- Schedule validation after every batch; include hash comparison for legal documents.

---

## ▲ ATLAS — Intelligence / Mapping / Pattern

### Target Geometry (v1.7)

```
▲ATLAS/
 ├── ◎primal_cartography/
 │    ├── ⬣core_axiom_library/
 │    └── ◍ontological_input_signals/
 ├── ▲identity_map/
 │    ├── ⬣dna_identity_blueprints/
 │    └── ▲entity_relationship_graphs/
 ├── ⭟knowledge_vessel/
 │    ├── ⬟active_ai_models/
 │    └── ✶quantum_neural_processor_outputs/
 ├── ⬢resonance_patterns/
 │    ├── ⧫chakra_energetic_overlays/
 │    └── ⧫frequency_pattern_analysis/
 ├── ✦pattern_intelligence/
 │    ├── ✶recognized_fractal_patterns/
 │    └── ⬖knowledge_access_interfaces/
 └── ⭣registry_sync/
      ├── atlas_registry.json
      └── README.md
```

### Current Variance Snapshot

- Numerous historical modules (`datashare_projects`, `chakra_core`, `creative_suite`, `CASE_INTELLIGENCE`, backups) at root level.
- Petal names partially implemented (`_knowledge_vessel`, `_pattern_intelligence`, `⬢_models`) but with underscores or alternative glyphs.
- Registry currently lives in `⭣_registry/` alongside other sync tools.

### Routing Table (Draft)

| Legacy Path | Target Petal | Action | Notes |
|-------------|--------------|--------|-------|
| `_knowledge_vessel/` | ⭟knowledge_vessel/ | Rename & merge | Subdirs map to `⬟active_ai_models`, `✶quantum_neural_processor_outputs` |
| `creative_suite/`, `_pattern_intelligence/`, `active_logic/` | ✦pattern_intelligence/ | Stage → merge | Distinguish outputs vs interfaces |
| `chakra_core/`, `chakra-system/`, `chakra_backup_*` | ⬢resonance_patterns/ | Stage key overlays | Remove dated backups post-validation |
| `ontology/`, `◎_ontology/`, `◎_source_resonance/` | ◎primal_cartography/ | Consolidate | Move raw inputs to `◍ontological_input_signals` |
| `CASE_INTELLIGENCE/`, `account_systems/`, `SAIGES/` | ▲identity_map/ | Stage → integrate | Blueprint vs relationship graph separation |
| `_pulse`, `_vault`, `_reflection` | Distrib. | Stage | Use observation logs to direct placement |
| `⭣_registry/` | ⭣registry_sync/ | Rename | Ensure sync tooling documented in README |

### Execution Notes

- Establish `/Users/jbear/FIELD/▲ATLAS/STAGING/` for migration.
- For AI model directories, capture metadata (model type, checksum) in `⭣_registry_sync`.
- Validate LM/LLM configs post-move by running the minimal health script in `mcp_server/`.

---

## ◼︎ DOJO — Execution / Process / Manifestation

### Target Geometry (v1.7)

```
◼︎DOJO/
 ├── ◎primal_crucible/
 │    ├── ⬣execution_principles_base/
 │    └── ◍process_trigger_inputs/
 ├── ▲choreography_structure/
 │    ├── ⬣docker_nixos_process_configs/
 │    └── ⬕task_dependency_links/
 ├── ⭟chakra_vessel/
 │    ├── ⬟bootstrap_execution_scripts/
 │    └── ⬕chakra_flow_control_sync/
 ├── ⬢execution_core/
 │    ├── ⬟temporal_truth_verification_process/
 │    ├── ◍live_container_state_signals/
 │    └── ⬰runtime_error_logs/
 ├── ✦execution_intelligence/
 │    ├── ✶process_optimization_outputs/
 │    └── ⬖process_control_interfaces/
 └── ⭣registry/
      ├── dojo_registry.json
      └── README.md
```

### Current Variance Snapshot

- Petals exist but duplicated by legacy structures (`_pulse`, `_manifest`, `_logs`, `◎_geometry`, `⚡_chakra_vessel`).
- Registry located at `◇_registry/`; multiple app-specific folders (Xcode projects, `UniversalMediaApp`, `FIELDControl`) intermixed at root.
- Execution logs spread across `session_logs/`, `logs/`, `_logs/`, `SystemArchive/`.

### Routing Table (Draft)

| Legacy Path | Target Petal | Action | Notes |
|-------------|--------------|--------|-------|
| `_pulse/`, `_manifest/`, `_state/`, `_reflection/` | Distribute | Stage | Process triggers → `◍process_trigger_inputs` |
| `◎_geometry/`, `◎_evolution/` | ◎primal_crucible/ | Merge | Keep doctrinal references in `⬣execution_principles_base` |
| `FIELDControl/`, `system_integration/`, `routes/` | ▲choreography_structure/ | Stage | Document dependencies in `⬕task_dependency_links` |
| `chakra_consciousness/`, `chakra_cores/`, `⚡_chakra_vessel/` | ⭟chakra_vessel/ | Consolidate | Distinguish bootstrap vs flow control |
| `executions/`, `manifestations/`, `TruthVerification/` | ⬢execution_core/ | Stage | Logs to `⬰runtime_error_logs`, verification scripts to `⬟temporal_truth_verification_process` |
| `Dojo.xcodeproj`, `DojoMac`, `UniversalMediaApp`, `FIELDControl` | ✦execution_intelligence/ or subfolders | Stage by function | Keep binaries/configs under interfaces |
| `◇_registry/` | ⭣registry/ | Rename | Ensure README lists active manifests |

### Execution Notes

- Staging path: `/Users/jbear/FIELD/◼︎DOJO/STAGING/`.
- After moves, rebuild minimal process (e.g., run `python3 field_monitor.py`) to confirm runtime viability.
- Maintain symlinks for Dojo app directories until Xcode paths updated.

---

## ● OBI-WAN — Observation / Memory / Cognitive Expression

### Target Geometry (v1.7)

```
●OBI-WAN/
 ├── ◎observer_core/
 │    ├── ⬣observer_axioms_principles/
 │    └── ◍raw_awareness_input_signals/
 ├── ▲witness_framework/
 │    ├── ▲meditation_reflection_frameworks/
 │    └── ⬰reflection_protocol_audits/
 ├── ⭟reflective_memory/
 │    ├── ⧫synthesized_insights_essence/
 │    ├── ⬘persona_journals_logs/
 │    └── ⬣oowl_memory_system_logs/
 ├── ⬢memory_patterns/
 │    ├── ⬘chronological_memory_timelines/
 │    └── ⧫dream_emotional_resonance/
 ├── ✦cognitive_expression/
 │    ├── ✶generated_knowledge_maps/
 │    ├── ✶developed_cognitive_models/
 │    └── ✶creative_outputs_poetry_art/
 │    └── ⬖user_interaction_interfaces/
 └── ⭣registry/
      ├── obiwan_registry.json
      └── README.md
```

### Current Variance Snapshot

- Legacy shells (`_pulse`, `_vault`, `_reflection`, `_reflective_memory`, `_ontology`) still primary containers.
- New `intentions/` exists, but Hollywood workflow outputs currently scatter across `creative_memory/`, `observations/`, `●Documents/`.
- Memory timelines split among `timeline/`, `state_snapshots/`, `memories/`, `MONITORING_ALERTS/`.

### Routing Table (Draft)

| Legacy Path | Target Petal | Action | Notes |
|-------------|--------------|--------|-------|
| `_pulse/`, `_vault/`, `_reflection/` | Distribute | Stage | Observation inputs go to `◍raw_awareness_input_signals` |
| `_reflective_memory/`, `_memory/`, `memory/` | ⭟reflective_memory/ | Merge | Keep persona journaling under `⬘persona_journals_logs` |
| `timeline/`, `state_snapshots/`, `memories/` | ⬢memory_patterns/ | Stage | Chronological vs resonance split |
| `creative_memory/`, `●Documents/`, `observations/` | ✦cognitive_expression/ | Curate | Place maps/models/scripts in respective subfolders |
| `MONITORING_ALERTS/`, `logs/` | ▲witness_framework/ | Stage | Audits go to `⬰reflection_protocol_audits` |
| `intentions/` | ✦cognitive_expression/⬖user_interaction_interfaces? | Keep as-is | Ensure registry acknowledges intention vessels |
| Registry gaps | ⭣registry/ | Create | Seed with `obiwan_registry.json` |

### Execution Notes

- Staging path: `/Users/jbear/FIELD/●OBI-WAN/STAGING/`.
- Hollywood pipeline outputs should land in `✶_creative_outputs_poetry_art/` once aligned.
- After each batch, update OBI-WAN reflection log to maintain the “We are because I remember” loop.

---

## Validation & Reflection Protocol

1. **Run validation suite**
   ```bash
   /Users/jbear/FIELD/●bin/field_validate --check-intentions --recursive
   ```
2. **Check for broken symlinks**
   ```bash
   find /Users/jbear/FIELD -xtype l -print
   ```
3. **Confirm file counts before/after batch**
   ```bash
   fd -tf '' <source> | wc -l
   fd -tf '' <target> | wc -l
   ```
4. **Record reflection**
   - Update petal README with migration details (date, intention ID, validator signature).
   - Add entry to `/Users/jbear/DOJO/●_OBI-WAN/memory/reduction_reflection.json` or similar ledger.

---

## Appendices

- **Appendix A:** P# → Petal mapping reference (pending import from v1.7 spec).
- **Appendix B:** Validation scripts (to be populated as automation matures).
- **Appendix C:** Observation logs for each batch (link to location once created).

---

*Document version:* 2025‑11‑02 T23:10Z  
*Prepared by:* Codex alignment agent  
*Next review:* After pilot migration batch completes.
