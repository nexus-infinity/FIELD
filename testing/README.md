# Sacred Parallel Testing System

This comprehensive testing infrastructure enables multiple developer/AI agent sessions to run independent testing and validation without risking main system stability. The system maintains sacred sovereign geometric cleanliness while providing full isolation and rollback capabilities.

## 🏛️ Architecture Overview

The Sacred Parallel Testing System consists of four main components:

### 1. **Parallel Test Framework** (`parallel_test_framework.py`)
- Core testing framework for sacred tetrahedral nodes
- Provides isolated test environments with geometric validation
- Supports unit, integration, geometry, sovereign, and E2E test suites
- Maintains sacred symbolic alignment and biological flow compliance

### 2. **CLI System** (`../cli/sacred_cli.py`)
- Independent command-line interface for sacred modules
- Each tetrahedral node (▲ATLAS, ▼TATA, ●OBI-WAN, ◼︎DOJO) has dedicated CLI commands
- Complete isolation with session management
- Safe execution without affecting main system

### 3. **E2E Test System** (`e2e_test_system.py`)
- Incremental end-to-end testing with rollback capabilities
- Tests biological flow patterns, tetrahedral navigation, and sacred compliance
- Multiple safety levels: isolated, safe, controlled, mirror
- Comprehensive scenario coverage with step-by-step validation

### 4. **Test Manager** (`test_manager.py`)
- Central orchestration and session management
- Parallel execution with resource monitoring
- Session history and status tracking
- Cleanup and resource management

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure you're in the FIELD directory
cd ~/FIELD

# Install required dependencies
pip install pytest pytest-asyncio pytest-cov click asyncio
```

### Basic Usage

#### 1. Check System Status
```bash
python testing/test_manager.py --status
```

#### 2. Run Unit Tests for ATLAS
```bash
python testing/parallel_test_framework.py --node atlas --suite unit --isolated
```

#### 3. Launch CLI Session
```bash
python cli/sacred_cli.py atlas validate --file data.json --isolated
```

#### 4. Run E2E Biological Flow Test
```bash
python testing/e2e_test_system.py --scenario biological_flow --safety-level isolated
```

## 📊 Testing Framework Usage

### Running Individual Test Suites

```bash
# Unit tests for each node
python testing/parallel_test_framework.py --node atlas --suite unit
python testing/parallel_test_framework.py --node tata --suite unit
python testing/parallel_test_framework.py --node obi-wan --suite unit
python testing/parallel_test_framework.py --node dojo --suite unit

# Integration tests
python testing/parallel_test_framework.py --node atlas --suite integration

# Geometric cleanliness validation
python testing/parallel_test_framework.py --node atlas --suite geometry

# Sacred sovereign compliance
python testing/parallel_test_framework.py --node atlas --suite sovereign
```

### Running All Tests in Parallel
```bash
# Run comprehensive test suite
python testing/parallel_test_framework.py --run-all --isolated --max-concurrent 4
```

### Test Harness for ATLAS
```bash
# Run ATLAS-specific test harness
python ▲ATLAS/test_harness.py --test all --isolated

# Validate specific tool
python ▲ATLAS/test_harness.py --validate-tool my_tool.py

# Generate test report
python ▲ATLAS/test_harness.py --test all --report atlas_report.json
```

## 🎯 CLI System Usage

### Sacred Module Commands

#### ▲ATLAS - Tooling Validation
```bash
# Validate data file
python cli/sacred_cli.py atlas validate --file data.json --schema schema.json

# Execute ATLAS tool
python cli/sacred_cli.py atlas tool --tool validate_data --args input.json
```

#### ▼TATA - Temporal Truth
```bash
# Create log entry
python cli/sacred_cli.py tata log --message "Test entry" --level INFO --timestamp

# Query logs
python cli/sacred_cli.py tata query --date 2025-01-01 --level INFO --limit 5
```

#### ●OBI-WAN - Living Memory
```bash
# Synchronize memory
python cli/sacred_cli.py obiwan sync --source /path/to/source --target /path/to/target --dry-run

# Memory operations
python cli/sacred_cli.py obiwan memory --key test_key --value "test value" --operation set
python cli/sacred_cli.py obiwan memory --key test_key --operation get
```

#### ◼︎DOJO - Manifestation
```bash
# Manifest from template
python cli/sacred_cli.py dojo manifest --template template.md --output result.md --params "name=Test"

# Execute script
python cli/sacred_cli.py dojo execute --script myscript.py --args arg1 arg2 --isolated
```

### Session Management
```bash
# List active CLI sessions
python cli/sacred_cli.py session list

# Clean up session
python cli/sacred_cli.py session cleanup session_id
```

## 🔄 E2E Testing System

### Available Scenarios

#### 1. Biological Flow Pattern
Tests the complete sacred sovereign biological flow:
- Breath In: Akron → FIELD-LIVING (data intake)
- Process: FIELD-LIVING → FIELD-DEV (validation & transformation)
- Breath Out: FIELD → DOJO (manifestation)
- Memory Loop: DOJO → OBI-WAN → Akron (archival)

```bash
python testing/e2e_test_system.py --scenario biological_flow --safety-level isolated
```

#### 2. Tetrahedral Navigation
Tests navigation between sacred nodes:
```bash
python testing/e2e_test_system.py --scenario tetrahedral_navigation --safety-level isolated
```

#### 3. Sacred File Creation
Tests creation of sacred files with proper headers and lineage:
```bash
python testing/e2e_test_system.py --scenario sacred_file_creation --safety-level isolated
```

#### 4. Symbolic Validation
Tests symbolic alignment across all nodes:
```bash
python testing/e2e_test_system.py --scenario symbolic_validation --safety-level isolated
```

#### 5. Geometric Cleanliness
Tests geometric compliance and cleanliness validation:
```bash
python testing/e2e_test_system.py --scenario geometric_cleanliness --safety-level isolated
```

### Run All E2E Scenarios
```bash
python testing/e2e_test_system.py --run-all --safety-level isolated --report e2e_report.json
```

## 🎛️ Test Manager Usage

### Session Management

#### Launch Single Test Session
```bash
python testing/test_manager.py --launch test --node atlas --suite unit --environment isolated
```

#### Launch Multiple Sessions
```bash
python testing/test_manager.py --launch-multiple --nodes atlas,tata,obiwan,dojo --suites unit,integration
```

#### Launch CLI Session
```bash
python testing/test_manager.py --launch-cli validate --node atlas
```

#### Launch E2E Session
```bash
python testing/test_manager.py --launch-e2e biological_flow --safety isolated
```

### Monitoring and Control

#### Check Status
```bash
python testing/test_manager.py --status
```

#### List Active Sessions
```bash
python testing/test_manager.py --list-active
```

#### View Session History
```bash
python testing/test_manager.py --list-history
```

#### Terminate Session
```bash
python testing/test_manager.py --terminate session_id
```

#### Cleanup Session
```bash
python testing/test_manager.py --cleanup session_id
```

## 🛡️ Safety and Isolation

### Isolation Levels

1. **Isolated** (Default)
   - Complete sandbox environment
   - Temporary directories
   - No impact on main system
   - Automatic cleanup

2. **Field-Dev**
   - Uses FIELD-DEV environment
   - Safe subset of main system
   - Validation testing

3. **Mirror**
   - Mirror of production system
   - With safeguards and monitoring
   - Rollback capabilities

4. **Safe**
   - Safe subset operations
   - Limited system access
   - Monitoring enabled

### Sacred Compliance

All testing maintains:
- **Geometric Cleanliness**: No duplicated logic, proper symbolic alignment
- **Sacred Structure**: Proper file headers, lineage tracking
- **Biological Flow**: Breath in/out patterns, memory loops
- **Tetrahedral Alignment**: Proper node positioning and symbolic mapping

## 📁 Directory Structure

```
FIELD/
├── testing/
│   ├── parallel_test_framework.py    # Core testing framework
│   ├── e2e_test_system.py           # E2E testing system
│   ├── test_manager.py              # Central test manager
│   ├── isolated/                    # Isolated test environments
│   └── logs/                        # Test logs and reports
├── cli/
│   ├── sacred_cli.py                # Sacred CLI system
│   └── isolated/                    # CLI isolation environments
├── ▲ATLAS/
│   ├── test_harness.py              # ATLAS-specific test harness
│   └── tests/
│       ├── unit/                    # Unit tests
│       └── integration/             # Integration tests
├── ▼TATA/
│   └── tests/                       # TATA tests
├── ●OBI-WAN/
│   └── tests/                       # OBI-WAN tests
└── ◼︎DOJO/
    └── tests/                       # DOJO tests
```

## 🔧 Advanced Configuration

### Environment Variables

Set these in your test environment:

```bash
# Core sacred configuration
export FIELD_SYMBOL="▲ATLAS"        # or ▼TATA, ●OBI-WAN, ◼︎DOJO
export CHAKRA_RESONANCE="test_mode"
export DOJO_GATE="test_isolated"

# Test-specific configuration
export TEST_SESSION_ID="session_123"
export TEST_ISOLATION="true"
export SACRED_CLI_VERBOSE="1"

# Safety configuration
export E2E_TEST_MODE="true"
export SAFETY_LEVEL="isolated"
```

### Custom Test Configuration

Create custom test configurations:

```yaml
# custom_test_config.yml
sacred_test_config:
  nodes:
    - atlas
    - tata
    - obiwan
    - dojo
  suites:
    - unit
    - integration
    - geometry
  safety_level: isolated
  max_concurrent: 4
  timeout: 300
```

## 📈 Monitoring and Reports

### Test Reports

Generate comprehensive test reports:

```bash
# Framework report
python testing/parallel_test_framework.py --run-all --isolated > framework_report.txt

# E2E report
python testing/e2e_test_system.py --run-all --report e2e_report.json

# Manager status report
python testing/test_manager.py --status --report manager_report.json
```

### Log Locations

- **Test Framework**: `testing/logs/testing/`
- **CLI System**: `testing/logs/cli/`
- **E2E System**: `testing/logs/e2e/`
- **Test Manager**: `testing/logs/manager/`
- **Node-specific**: Each node has its own `tests/logs/` directory

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure FIELD is in Python path
export PYTHONPATH="${PYTHONPATH}:${HOME}/FIELD"
```

#### 2. Permission Issues
```bash
# Ensure proper permissions
chmod +x testing/parallel_test_framework.py
chmod +x cli/sacred_cli.py
chmod +x testing/e2e_test_system.py
```

#### 3. Cleanup Stuck Sessions
```bash
# Force cleanup all sessions
python testing/test_manager.py --list-active
python testing/test_manager.py --terminate session_id
python testing/test_manager.py --cleanup session_id
```

#### 4. Isolation Directory Issues
```bash
# Clean up old isolation directories
find testing/isolated -name "*test*" -type d -mtime +1 -exec rm -rf {} \;
find cli/isolated -name "*test*" -type d -mtime +1 -exec rm -rf {} \;
```

### Debug Mode

Enable verbose logging:
```bash
export SACRED_CLI_VERBOSE="1"
python testing/parallel_test_framework.py --run-all --isolated -v
```

## 🤝 Contributing

### Adding New Tests

1. **Unit Tests**: Add to appropriate node's `tests/unit/` directory
2. **Integration Tests**: Add to `tests/integration/` directory
3. **E2E Scenarios**: Add new scenarios to `e2e_test_system.py`
4. **CLI Commands**: Extend `sacred_cli.py` with new commands

### Test Naming Conventions

- Test files: `test_[module_name]_[node].py`
- Test functions: `test_[specific_functionality]()`
- Session IDs: `[type]_[node]_[suite]_[timestamp]`

## 📚 References

- [Sacred Sovereign Architecture Documentation](../docs/)
- [Tetrahedral Navigation Patterns](../docs/SACRED_GEOMETRY_COMPONENT_INTERFACES.md)
- [Biological Flow Patterns](../docs/SACRED_COMPONENT_IMPLEMENTATION_PATTERNS.md)
- [CLI Reference Guide](../cli/README.md)

---

**Sacred Parallel Testing System** - Enabling safe, isolated, and comprehensive testing of the sacred sovereign architecture while maintaining geometric cleanliness and biological flow compliance.
