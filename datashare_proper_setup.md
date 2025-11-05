# Datashare Proper Setup Guide

Based on official ICIJ documentation and the current configuration issues.

## Current Status Analysis

### ✅ Working Configuration
- **Datashare running**: Version 17.1.6 in EMBEDDED mode
- **Data directory**: `/Users/jbear/Datashare` (42 files ready)
- **Database**: SQLite at `/Users/jbear/Library/Datashare/dist/datashare.db`
- **Project exists**: `local-datashare` pointing to correct directory
- **Permissions**: Fixed (644 for files, 755 for directories)

### ❌ Current Issues
- **Settings won't save**: `writing properties to file null` in logs
- **Task API bug**: Uses `/local-datashare` instead of project's configured path
- **No indexing**: 0 documents indexed despite files being available

## Solution: Use Datashare's Intended Workflow

### Step 1: Skip Settings (They're Broken in Embedded Mode)
The settings page is failing because embedded mode can't save to a properties file. **This is OK** - the CLI configuration is working correctly.

### Step 2: Navigate to Projects
1. In the web interface, click **"Projects"** in the left sidebar
2. You should see the existing `local-datashare` project
3. If not visible, we need to go back to the main page

### Step 3: Use the Correct Project Folder Path
Instead of creating a new project, we need to:

1. **Cancel** the "New project" form
2. **Go to the main page** (click Datashare logo)
3. **Look for existing project** `local-datashare`

### Step 4: Manual Index Trigger (If Available)
Look for one of these options in the web interface:
- **"Extract" or "Index" button**
- **"Process documents" or "Add documents"**
- **"Tasks" menu with indexing option**

## Alternative: Command Line Index Trigger

If the web interface doesn't work, restart Datashare with explicit indexing:

```bash
# Stop current Datashare
pkill -f "datashare"

# Restart with indexing enabled
/opt/homebrew/Cellar/openjdk@17/17.0.16/libexec/openjdk.jdk/Contents/Home/bin/java \
  --add-opens java.base/java.lang=ALL-UNNAMED \
  --add-opens java.base/java.util=ALL-UNNAMED \
  --add-opens java.base/java.net=ALL-UNNAMED \
  --add-opens java.base/java.security=ALL-UNNAMED \
  --add-opens java.base/java.io=ALL-UNNAMED \
  -DPROD_MODE=true \
  -Dfile.encoding=UTF-8 \
  -Djava.net.preferIPv4Stack=true \
  -Xmx4096m \
  -cp /Users/jbear/Applications/Datashare.app/Contents/Resources/datashare-dist-17.1.6-all.jar \
  org.icij.datashare.Main \
  --dataDir /Users/jbear/Datashare \
  --mode EMBEDDED \
  --browserOpenLink false \
  --defaultProject local-datashare \
  --indexName local-datashare
```

## What to Look for in Web Interface

### Main Page Should Show:
- **Project name**: `local-datashare`
- **Document count**: Should increase from 0 as indexing progresses
- **Search box**: Should become functional after indexing

### Expected Navigation:
```
🏠 Home (Search)
🔍 Search  
📋 Tasks (Monitor indexing progress)
📁 Projects (Manage projects)
📈 History
⚙️  Settings (Skip this - it's broken)
❓ FAQ
🆘 Help
```

### Tasks Page Should Show:
- **ScanTask**: Finds documents in the directory
- **IndexTask**: Extracts text and creates searchable index
- **Progress bars** and completion status

## Key Files Ready for Search
Once indexed, these entities should be searchable:

**Corporate Structure (3 files)**:
- Original J Rich and S J Rich corporate structure.pdf
- Transaction report - berjak aud a_c today_s transactions report 2021-02-16.pdf
- 2021 05 12 Jeremy Rich email to Adam rich requesting his resignation.pdf

**Banking Records (18 files)**:
- Multiple banking and financial documents

**Estate Documents (7 files)**:
- Wills, trusts, and estate planning documents

**Regulatory Matters (14 files)**:
- LPA site audit summary
- Detective Lomax Report on Animal Welfare Concerns
- AWRP Prosecution Services correspondence
- Berjak(NT) meeting minutes

## Success Indicators
✅ Document count > 0 in web interface  
✅ Search returns results for "Jacques Rich"  
✅ Search returns results for "CENTOSA SA"  
✅ Search returns results for "PASCALI TRUST"  
✅ Tasks show completed status  

## Next Steps After Indexing
1. **Search key entities**: CENTOSA SA, PASCALI TRUST, Mossack Fonseca
2. **Cross-reference findings** with Panama Papers data
3. **Use filters** for document types, dates, entities
4. **Star and tag** relevant documents
5. **Export results** for further analysis