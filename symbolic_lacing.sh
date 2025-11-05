#!/usr/bin/env bash
set -euo pipefail

# Define base directories
FIELD_ROOT="/Users/jbear/FIELD"
LIVING_ROOT="/Users/jbear/FIELD-LIVING"

# Ensure directories exist
mkdir -p "${FIELD_ROOT}/●◎_memory_core"
mkdir -p "${FIELD_ROOT}/▲ATLAS"
mkdir -p "${FIELD_ROOT}/▼TATA"
mkdir -p "${FIELD_ROOT}/◼_dojo"

# Create symbolic links for tetrahedral flow
ln -sf "${LIVING_ROOT}/●◎_memory_core" "${FIELD_ROOT}/●◎_memory_core"
ln -sf "${LIVING_ROOT}/▲ATLAS" "${FIELD_ROOT}/▲ATLAS"
ln -sf "${LIVING_ROOT}/▼TATA" "${FIELD_ROOT}/▼TATA"
ln -sf "${LIVING_ROOT}/◼_dojo" "${FIELD_ROOT}/◼_dojo"

# Create symbolic links for the sacred geometry pattern
ln -sf "${FIELD_ROOT}/●◎_memory_core/patterns" "${FIELD_ROOT}/▲ATLAS/patterns"
ln -sf "${FIELD_ROOT}/▲ATLAS/intelligence" "${FIELD_ROOT}/▼TATA/verification"
ln -sf "${FIELD_ROOT}/▼TATA/integrity" "${FIELD_ROOT}/◼_dojo/execution"
ln -sf "${FIELD_ROOT}/◼_dojo/manifestation" "${FIELD_ROOT}/●◎_memory_core/reflection"

echo "✅ Symbolic lacing complete - tetrahedral flow established."
