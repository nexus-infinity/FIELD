# FIELD Data_Lake Drive Sync Setup Guide

## Overview
This system automatically syncs your Google Drive folder containing legal, financial, and investigative documents to your Notion Data_Lake database. It includes intelligent classification, de-duplication, and FIELD system integration with resonance analysis.

## Features
- **Recursive folder scanning** - processes all files and subfolders
- **De-duplication** - updates existing entries instead of creating duplicates
- **Intelligent classification** - auto-tags entities and topics based on filename patterns
- **Investigation priority** - assigns priority levels (Critical, High, Medium, Standard)
- **FIELD integration** - includes resonance frequencies and harmonic analysis
- **Rate limiting** - respects Notion API limits with automatic retry
- **Error handling** - robust error handling with detailed logging

## Step 1: Create Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New Integration"
3. Set the following:
   - **Name**: "FIELD Data_Lake Sync"
   - **Associated workspace**: Your workspace
   - **Capabilities**: Read content, Update content, Insert content
4. Click "Submit"
5. **Copy the Internal Integration Token** - you'll need this later

## Step 2: Share Data_Lake Database

1. Open your Data_Lake database in Notion
2. Click the "Share" button (top right)
3. Click "Invite" and search for your integration name "FIELD Data_Lake Sync"
4. Select the integration and give it "Can edit" permissions
5. Click "Invite"

## Step 3: Get Database ID

1. Open your Data_Lake database in Notion
2. Copy the URL - it looks like: `https://notion.so/yourworkspace/DATABASE_ID?v=...`
3. The DATABASE_ID is the long string between the last slash and the question mark
4. Save this ID for the next step

## Step 4: Create Google Apps Script

1. Go to [Google Apps Script](https://script.google.com)
2. Click "New Project"
3. Delete the default code and paste the entire contents of `notion_drive_sync_production.js`
4. Save the project with name "FIELD Data_Lake Sync"

## Step 5: Configure Script Properties

1. In Apps Script editor, click the gear icon (Project Settings)
2. Scroll down to "Script Properties" section
3. Add these properties:

| Property Name | Value |
|---------------|-------|
| `NOTION_TOKEN` | Your integration token from Step 1 |
| `NOTION_DATABASE_ID` | Your database ID from Step 3 |
| `FOLDER_ID` | `1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ` |

## Step 6: Initial Setup and Testing

1. In the Apps Script editor, select the function dropdown and choose `setupFieldSync`
2. Click the "Run" button
3. Grant permissions when prompted (Drive and external requests)
4. Check the logs - you should see:
   ```
   ✅ Drive folder access confirmed: data_lake
   ✅ Notion database connection confirmed
   🎯 Setup complete! Ready to create daily trigger.
   ```

5. Test with a few files by running `testFieldSync` function
6. Check the classification results in the logs

## Step 7: Run Initial Full Sync

1. Select `syncDriveToNotion` function
2. Click "Run" - this will process ALL files in your Drive folder
3. Monitor the logs for progress updates
4. Check your Notion Data_Lake database to see the synced files

## Step 8: Set Up Daily Automation

1. In Apps Script, select the function `createDailyTrigger`
2. Click "Run" - this creates a daily trigger for 6:00 AM Melbourne time
3. You can view triggers in the left sidebar "Triggers" section
4. The sync will now run automatically every day

## Data_Lake Database Schema

The sync creates these properties in your Notion database:

| Property | Type | Description |
|----------|------|-------------|
| File Name | Title | Original filename |
| Source Link | URL | Direct link to Drive file |
| Date | Date | Date added to database |
| Entity | Multi-select | Auto-classified entities (Rich Family, Corporate Entity, etc.) |
| Topic | Multi-select | Auto-classified topics (Legal Documents, Financial Records, etc.) |
| File Size (KB) | Number | File size in kilobytes |
| File Type | Select | PDF Document, Word Document, Image, etc. |
| Last Modified | Date | When file was last modified in Drive |
| Investigation Priority | Select | Critical, High, Medium, Standard |

## Entity Classifications

The system automatically detects these entity types:

- **Trust Structure** - files containing "trust" or "deed"
- **Rich Family** - files mentioning "rich", "jacques", "susan"
- **Corporate Entity** - "berjak", "ansevata", "centosa"
- **Financial Institution** - "bank", "bekb", "nab"
- **Legal Entity** - "court", "legal", "hunt"
- **Government Authority** - "ibac", "police", "gov"
- **Offshore Structure** - "panama", "offshore"
- **Financial Obligation** - "mortgage", "loan"
- **Property** - "walkerville", "mornington"

## Topic Classifications

Topics are auto-assigned based on content:

- **Financial Records** - bank statements, financial documents
- **Legal Documents** - agreements, contracts
- **Communications** - correspondence, letters, emails
- **Tax Documents** - tax forms, invoices
- **Property Finance** - mortgages, property transactions
- **Property Rights** - easements, covenants
- **Planning Documents** - planning permits, reports
- **Law Enforcement** - police statements, IBAC documents
- **Digital Security** - passwords, security files

## Investigation Priority

Files are automatically prioritized:

- **Critical**: Panama Papers, fraud, police, IBAC documents
- **High**: Trust deeds, corporate documents, financial statements, legal documents
- **Medium**: Property documents, correspondence
- **Standard**: All other documents

## FIELD System Integration

The sync includes FIELD-specific features:

- **Resonance Analysis**: Perfect harmony (777.55Hz) for successful syncs
- **Harmonic State**: PERFECT_HARMONY, MINOR_DISSONANCE, MAJOR_DISSONANCE
- **Chakra Alignment**: CROWN_ALIGNED for optimal performance
- **Sacred Geometry**: Data organized according to FIELD principles

## Monitoring and Maintenance

### Check Last Sync Status
Run `getLastSyncSummary()` to see the most recent sync results:

```javascript
{
  "timestamp": "2024-01-22T06:00:00.000Z",
  "system": "NOTION_DRIVE_SYNC",
  "operation": "DATA_LAKE_SYNC",
  "status": "SUCCESS",
  "metrics": {
    "total_files": 156,
    "processed": 156,
    "created": 12,
    "updated": 144,
    "errors": 0,
    "duration_seconds": 45,
    "success_rate": "100.0%"
  },
  "resonance": {
    "frequency": 777.55,
    "harmonic_state": "PERFECT_HARMONY",
    "chakra_alignment": "CROWN_ALIGNED"
  }
}
```

### Modify Sync Schedule
To change the sync time, delete the existing trigger and create a new one:

```javascript
// Delete existing triggers
ScriptApp.getProjectTriggers()
  .filter(trigger => trigger.getHandlerFunction() === 'syncDriveToNotion')
  .forEach(trigger => ScriptApp.deleteTrigger(trigger));

// Create new trigger for different time
ScriptApp.newTrigger('syncDriveToNotion')
  .timeBased()
  .everyDays(1)
  .atHour(9) // 9 AM instead of 6 AM
  .create();
```

## Troubleshooting

### Common Issues

1. **"Missing NOTION_TOKEN" error**
   - Check Script Properties are set correctly
   - Verify the token hasn't expired

2. **"Cannot access Drive folder" error**
   - Ensure the script has Drive permissions
   - Check the FOLDER_ID is correct

3. **"Notion connection failed" error**
   - Verify the database is shared with the integration
   - Check the database ID is correct

4. **Rate limiting errors**
   - The script handles this automatically with retries
   - If persistent, consider reducing batch size

5. **Files not classified correctly**
   - Modify the `classifyFile_` function patterns
   - Add custom keywords for your specific documents

### Performance Optimization

- The script processes files in batches with rate limiting
- Large folders (500+ files) may take several minutes
- Monitor execution time limits (6 minutes for triggers)

## Security Considerations

- Tokens are stored securely in Script Properties
- Only authorized integration can access your Notion database
- Drive folder permissions control who can add files
- All API calls are logged for audit purposes

## Integration with FIELD Investigation System

This sync system feeds directly into your broader FIELD investigation platform:

1. **Resonance Analysis**: Documents are analyzed for harmonic patterns
2. **Entity Relationships**: Auto-classification enables relationship mapping
3. **Investigation Workflows**: Priority levels guide investigation focus
4. **Data Gravity**: Documents naturally flow to their resonant locations

The sync creates the foundational data layer for your sophisticated investigation and analysis tools, ensuring all relevant documents are immediately available for cross-reference, pattern analysis, and evidence correlation.

## Next Steps

1. Complete the setup following this guide
2. Run the initial sync and verify results
3. Set up the daily trigger
4. Monitor sync performance and adjust classifications as needed
5. Integrate with your broader FIELD investigation workflow

Your Drive folder contains extensive legal and financial documentation that will be invaluable for your investigation. The intelligent classification system will automatically organize everything according to FIELD principles, creating a powerful searchable database for your research.