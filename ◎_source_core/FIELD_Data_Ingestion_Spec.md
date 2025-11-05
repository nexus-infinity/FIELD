# FIELD ISO-Compliant Data Ingestion Specification
*Version 1.0 - Sacred Geometric Intelligence Architecture*

## Standards Spine (Universal Requirements)

Every data feed entering FIELD must satisfy these ISO-aligned standards:

### 1. Temporal Standards (ISO 8601)
- **observed_at**: Original timestamp from source (NEVER re-stamp)
- Format: `2025-09-16T21:14:00+10:00` (with timezone)
- No ambiguity, clean timeline sorts, universal compatibility

### 2. Location Standards (ISO 3166 + ISO 4217)
- **where**: ISO 3166 codes (e.g., `AU-VIC` for Victoria)
- **currency**: ISO 4217 codes when applicable (e.g., `AUD`)
- Enables stable joins across diverse sources

### 3. Geospatial Standards (ISO 19115/19115-3)
- **geo_metadata**: ISO 19115 compliant metadata for spatial datasets
- Use ANZLIC/GA/ICSM profiles as gold standard
- Essential for map-tied intelligence overlay

### 4. Integrity Standards (Chain of Custody)
- **sha256**: Cryptographic hash of raw payload at capture
- **source_id**: Stable publisher + endpoint identifier
- Immutable provenance and tamper evidence

## Minimal Ingestion Contract

### Core Fields (Mandatory for ALL feeds)
```json
{
  "observed_at": "2025-09-16T21:14:00+10:00",  // ISO 8601 from source
  "source_id": "vicpol:media_releases",        // Publisher:endpoint
  "where": "AU-VIC",                           // ISO 3166 location
  "sha256": "a1b2c3d4...",                     // Integrity hash
  "payload": {},                               // Original data
  "ingested_at": "2025-09-16T21:14:05+10:00", // FIELD timestamp
  "geo_metadata": {}                           // ISO 19115 if applicable
}
```

### Validation Checklist
- [ ] ISO 8601 timestamp validates and parses
- [ ] Source ID follows `publisher:endpoint` format
- [ ] Location uses valid ISO 3166 code
- [ ] SHA256 matches payload hash
- [ ] Geospatial data includes ISO 19115 metadata block

## Error Handling
- **Timestamp Failures**: Log error, attempt timezone inference, flag as `timestamp_uncertain`
- **Hash Mismatches**: Reject ingestion, alert on potential tampering
- **Missing Mandatory Fields**: Queue for manual review, do not auto-process
- **Geo Metadata Missing**: Accept but flag as `geo_incomplete`

## Quality Gates
- **Data Freshness**: Alert if `observed_at` > 24h old for real-time sources
- **Source Reliability**: Track success/failure rates per `source_id`
- **Completeness Scoring**: Rate records 0.0-1.0 based on field completion
- **Chain Integrity**: Cryptographically verify payloads on random sampling

---

*This specification ensures FIELD ingests data with judicial-grade provenance while maintaining compatibility with Australian government data standards and ISO compliance frameworks.*