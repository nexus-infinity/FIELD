# Datashare Manual Indexing - Configuration Bug Workaround

## Problem Identified
- **CLI config**: `--dataDir /Users/jbear/Datashare` ✅ 
- **SQLite config**: `path = /Users/jbear/Datashare` ✅
- **Task API bug**: Hardcodes `dataDir = /local-datashare` ❌

The task API has a bug where it uses the project name as a literal filesystem path instead of using the project's configured path from the database.

## Solution: Use Web Interface

1. **Open Datashare in browser**: http://localhost:9630

2. **Navigate to indexing**:
   - Look for "Index" or "Extract" option in the menu
   - Should show project: `local-datashare` 
   - Should show source path: `/Users/jbear/Datashare` (correct path)

3. **Start indexing through web UI**:
   - The web interface should use the correct project path from the database
   - Monitor progress in the UI

4. **Verify documents indexed**:
   - Check document count in web interface
   - Or run: `sqlite3 "/Users/jbear/Library/Datashare/dist/datashare.db" "SELECT count(*) FROM document;"`

## Current Status
- **Documents copied**: 42 files in 5 project directories ✅
- **Permissions fixed**: All files now 644, directories 755 ✅  
- **Datashare running**: PID 64104 on port 9630 ✅
- **Database healthy**: SQLite integrity check passed ✅

## Key Entities to Search After Indexing
- CENTOSA SA
- PASCALI TRUST
- Jacques Rich
- Adam Rich  
- David Rich
- Mossack Fonseca
- bearer shares
- BERJAK NOMINEES

## Files Ready for Analysis
```
/Users/jbear/Datashare/jacques-rich-corporate-structure/: 3 files
/Users/jbear/Datashare/jacques-rich-banking-records/: 18 files  
/Users/jbear/Datashare/jacques-rich-estate-documents/: 7 files
/Users/jbear/Datashare/jacques-rich-regulatory-matters/: 14 files
/Users/jbear/Datashare/jacques-rich-panama-papers/: 0 files
```

**Total: 42 PDF, DOCX, and TXT files ready for cross-referencing with Panama Papers data**