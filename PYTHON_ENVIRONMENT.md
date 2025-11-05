# 🐍 FIELD Python Environment

## Unified Python Setup for All FIELD Operations

This document describes the standardized Python environment for your FIELD ecosystem, ensuring consistent execution across all conversation systems, servers, and integrations.

---

## 📍 **Environment Location**

**Primary Python**: `/Users/jbear/FIELD/.venv/bin/python` (Python 3.11.13)  
**Quick Access**: `/Users/jbear/FIELD/bin/python` (symlink)  
**Virtual Environment**: `/Users/jbear/FIELD/.venv/`

---

## 🚀 **Usage**

### **Direct Execution**
```bash
# Use FIELD Python directly
/Users/jbear/FIELD/bin/python script.py

# Run conversation server
/Users/jbear/FIELD/bin/python /Users/jbear/FIELD/◎_source_core/conversation_server_integration.py

# Run mobile client
/Users/jbear/FIELD/bin/python /Users/jbear/FIELD/◎_source_core/mobile_conversation_client.py
```

### **Environment Activation** 
```bash
# Activate FIELD Python environment
source /Users/jbear/FIELD/.venv/bin/activate

# Or use the convenience script (when PATH is set)
field-python  # (adds alias to .zshrc)
```

### **Package Management**
```bash
# Install packages in FIELD environment
/Users/jbear/FIELD/bin/pip install package_name

# Or with activated environment
source /Users/jbear/FIELD/.venv/bin/activate
pip install package_name
```

---

## 📦 **Installed Core Packages**

### **Conversation System Dependencies**
- `aiohttp` - Async HTTP client/server for API endpoints
- `websockets` - WebSocket support for real-time mobile communication
- `torch` - AI/ML framework for consciousness modeling
- `numpy` - Numerical computing for sacred frequency calculations
- `pandas` - Data analysis for conversation patterns
- `requests` - HTTP requests for server communication

### **System Integration**
- Python 3.11.13 (Homebrew via `/opt/homebrew/bin/python3.11`)
- Virtual environment isolated from system Python
- Symlinks in `/Users/jbear/FIELD/bin/` for convenient access

---

## 🔧 **File Configurations**

### **Updated Scripts**
All conversation system scripts now use the correct shebang:
```python
#!/Users/jbear/FIELD/.venv/bin/python
```

### **Key Files Using FIELD Python**
- `/Users/jbear/FIELD/◎_source_core/conversation_server_integration.py`
- `/Users/jbear/FIELD/◎_source_core/mobile_conversation_client.py`
- All future Python scripts in the FIELD ecosystem

---

## 🔄 **Maintenance**

### **Re-setup Environment** (if needed)
```bash
/Users/jbear/FIELD/bin/field_python_setup.sh
```

### **Environment Information**
```bash
/Users/jbear/FIELD/bin/field_python_info.py
```

### **Check Current Setup**
```bash
source /Users/jbear/FIELD/.venv/bin/activate
python --version  # Should show Python 3.11.13
which python      # Should show /Users/jbear/FIELD/.venv/bin/python
```

---

## ✅ **Benefits of This Setup**

1. **Unified Environment** - Single Python installation for all FIELD operations
2. **Version Consistency** - Python 3.11.13 across all scripts and servers  
3. **Isolated Dependencies** - No conflicts with system Python or other projects
4. **Easy Access** - Direct paths and symlinks for quick execution
5. **Maintainable** - Setup script can recreate environment if needed
6. **Path Integration** - FIELD/bin added to PATH for system-wide access

---

## 🎯 **Next Steps**

1. **Test the conversation system** with the unified Python environment
2. **Install additional packages** as needed for specific FIELD operations
3. **Use this Python for all new FIELD scripts** to maintain consistency
4. **Document any additional dependencies** in this environment

---

**This is now your single source of truth for Python execution across all FIELD operations.**
