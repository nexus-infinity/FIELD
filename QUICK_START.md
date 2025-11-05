# Sacred Parallel Testing System - Quick Start Guide

## 🚀 Getting Started

The Sacred Test Launcher (`./sacred-test`) provides easy access to the entire Sacred Parallel Testing System.

### Basic Usage

```bash
# Make the script executable (if needed)
chmod +x sacred-test

# Check system status
./sacred-test status

# Show help
./sacred-test help
```

## 📋 Quick Commands

### System Management
```bash
./sacred-test status                    # Check system status
./sacred-test sessions                  # List active sessions
./sacred-test cleanup SESSION_ID       # Clean up session
./sacred-test validate                  # Validate system integrity
```

### Testing Framework
```bash
# Run specific test suites
./sacred-test test atlas unit           # Unit tests for ATLAS
./sacred-test test tata integration     # Integration tests for TATA
./sacred-test test obiwan geometry      # Geometry tests for OBI-WAN
./sacred-test test dojo sovereign       # Sovereign compliance tests for DOJO

# Quick tests (unit + geometry)
./sacred-test quick atlas               # Quick test for ATLAS
```

### CLI Commands
```bash
# Execute CLI commands for each sacred node
./sacred-test cli atlas validate data.json
./sacred-test cli tata log "Test message"
./sacred-test cli obiwan sync --dry-run
./sacred-test cli dojo manifest --template test.md
```

### End-to-End Testing
```bash
# Run E2E scenarios
./sacred-test e2e biological_flow       # Test biological flow compliance
./sacred-test e2e tetrahedral_navigation # Test navigation between nodes
./sacred-test e2e symbolic_validation   # Test symbolic integrity
./sacred-test e2e geometric_cleanliness  # Test geometric standards
./sacred-test e2e all                    # Run all E2E scenarios
```

### Comprehensive Testing
```bash
./sacred-test all                       # Run complete test suite
```

## 🔧 Available Test Suites

- **unit**: Basic functionality tests
- **integration**: Cross-component integration tests
- **geometry**: Sacred geometric alignment validation
- **sovereign**: Compliance with sacred sovereign principles
- **e2e**: End-to-end workflow validation

## 🏛️ Sacred Nodes

- **▲ATLAS**: Tooling validation and execution
- **▼TATA**: Temporal truth logging and querying
- **●OBI-WAN**: Living memory synchronization
- **◼︎DOJO**: Manifestation and script execution

## 🛡️ Safety Features

All testing operations run in isolated environments to protect system stability:

- ✅ Isolated test sessions
- ✅ Rollback capabilities
- ✅ Geometric cleanliness preservation
- ✅ Symbolic integrity validation
- ✅ Session management and cleanup

## 📚 Examples

```bash
# Daily development workflow
./sacred-test validate                  # Ensure system integrity
./sacred-test quick atlas              # Quick test current work
./sacred-test e2e biological_flow      # Validate biological compliance

# Before major changes
./sacred-test all                      # Comprehensive validation

# Testing specific features
./sacred-test test atlas unit          # Test ATLAS tooling
./sacred-test cli atlas validate data.json  # Validate specific data

# Maintenance
./sacred-test sessions                 # Check active sessions
./sacred-test cleanup old_session_id  # Clean up if needed
```

## 🎯 Next Steps

1. Run `./sacred-test validate` to ensure the system is properly set up
2. Try `./sacred-test quick atlas` for a quick validation
3. Explore the comprehensive testing with `./sacred-test all`
4. Use specific commands as needed for your development workflow

The system is designed for parallel developer/AI agent sessions while maintaining sacred sovereign principles and geometric cleanliness.
