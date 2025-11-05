/**
 * FIELD Data_Lake Sync - Production Google Apps Script
 * Syncs Drive folder to Notion Data_Lake database with de-duplication and FIELD integration
 * 
 * Setup Instructions:
 * 1. Google Apps Script → File → Project Properties → Script properties:
 *    - NOTION_TOKEN = your Notion integration secret
 *    - NOTION_DATABASE_ID = your Data_Lake database ID  
 *    - FOLDER_ID = 1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ
 * 
 * 2. Share Data_Lake database with your Notion integration
 * 3. Run syncDriveToNotion() once to authorize
 * 4. Add daily time-driven trigger
 */

function syncDriveToNotion() {
  const props = PropertiesService.getScriptProperties();
  const NOTION_TOKEN = props.getProperty('NOTION_TOKEN');
  const NOTION_DATABASE_ID = props.getProperty('NOTION_DATABASE_ID');
  const FOLDER_ID = props.getProperty('FOLDER_ID') || '1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ';

  if (!NOTION_TOKEN || !NOTION_DATABASE_ID) {
    throw new Error('Missing NOTION_TOKEN or NOTION_DATABASE_ID in Script properties.');
  }

  console.log('🔄 Starting FIELD Data_Lake sync...');
  
  const tz = Session.getScriptTimeZone() || 'Australia/Melbourne';
  const today = Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  const startTime = new Date();

  const files = listFilesRecursively_(FOLDER_ID);
  console.log(`📁 Found ${files.length} files to process`);
  
  let processed = 0;
  let created = 0;
  let updated = 0;
  let errors = 0;

  files.forEach(file => {
    try {
      const result = upsertNotionRow_(NOTION_TOKEN, NOTION_DATABASE_ID, file, today);
      processed++;
      if (result === 'created') created++;
      else if (result === 'updated') updated++;
      
      // Rate limiting - pause every 10 files
      if (processed % 10 === 0) {
        Utilities.sleep(1000);
        console.log(`📊 Processed ${processed}/${files.length} files...`);
      }
      
    } catch (error) {
      console.error(`❌ Error processing ${file.name}: ${error.message}`);
      errors++;
    }
  });

  const duration = (new Date() - startTime) / 1000;
  
  // Create FIELD-compatible summary
  const summary = {
    timestamp: new Date().toISOString(),
    system: 'NOTION_DRIVE_SYNC',
    operation: 'DATA_LAKE_SYNC',
    status: errors === 0 ? 'SUCCESS' : (errors < files.length / 2 ? 'PARTIAL_SUCCESS' : 'FAILED'),
    metrics: {
      total_files: files.length,
      processed: processed,
      created: created,
      updated: updated,
      errors: errors,
      duration_seconds: Math.round(duration),
      success_rate: ((processed - errors) / processed * 100).toFixed(1) + '%'
    },
    resonance: {
      frequency: errors === 0 ? 777.55 : (errors < 5 ? 432.00 : 256.00),
      harmonic_state: errors === 0 ? 'PERFECT_HARMONY' : (errors < 5 ? 'MINOR_DISSONANCE' : 'MAJOR_DISSONANCE'),
      chakra_alignment: errors === 0 ? 'CROWN_ALIGNED' : 'NEEDS_TUNING'
    }
  };

  console.log('✅ FIELD Data_Lake Sync Complete:', JSON.stringify(summary, null, 2));
  
  // Store summary for FIELD system integration
  props.setProperty('LAST_SYNC_SUMMARY', JSON.stringify(summary));
  
  return summary;
}

// Recursively list files in folder and all subfolders
function listFilesRecursively_(rootId) {
  const out = [];
  const stack = [DriveApp.getFolderById(rootId)];
  
  while (stack.length) {
    const folder = stack.pop();
    
    // Add subfolders to stack
    const subFolders = folder.getFolders();
    while (subFolders.hasNext()) {
      stack.push(subFolders.next());
    }
    
    // Add files from current folder
    const files = folder.getFiles();
    while (files.hasNext()) {
      const f = files.next();
      out.push({
        id: f.getId(),
        name: f.getName(),
        url: f.getUrl(),
        lastModified: f.getLastUpdated(),
        size: f.getSize(),
        mimeType: f.getBlob().getContentType(),
        path: getFilePath_(f)
      });
    }
  }
  
  return out;
}

// Get relative path of file for better organization
function getFilePath_(file) {
  const parents = file.getParents();
  if (parents.hasNext()) {
    const parent = parents.next();
    return parent.getName() + '/' + file.getName();
  }
  return file.getName();
}

// Find existing page by Source Link, update if found; otherwise create
function upsertNotionRow_(token, databaseId, file, todayISO) {
  const existing = queryBySourceLink_(token, databaseId, file.url);

  if (existing && existing.results && existing.results.length > 0) {
    // Update existing page
    const pageId = existing.results[0].id;
    const payload = {
      properties: {
        'File Name': { title: [{ text: { content: file.name } }] },
        'Source Link': { url: file.url },
        'Last Modified': { 
          date: { start: Utilities.formatDate(file.lastModified, Session.getScriptTimeZone(), 'yyyy-MM-dd') }
        }
      }
    };
    
    notionFetch_(token, 'https://api.notion.com/v1/pages/' + pageId, 'patch', payload);
    return 'updated';
    
  } else {
    // Create new page with intelligent classification
    const classification = classifyFile_(file.name, file.mimeType, file.path);
    
    const payload = {
      parent: { database_id: databaseId },
      properties: {
        'File Name': { title: [{ text: { content: file.name } }] },
        'Source Link': { url: file.url },
        'Date': { date: { start: todayISO } },
        'Entity': { 
          multi_select: classification.entities.map(name => ({ name }))
        },
        'Topic': { 
          multi_select: classification.topics.map(name => ({ name }))
        },
        'File Size (KB)': { 
          number: Math.round(file.size / 1024)
        },
        'File Type': {
          select: { name: getFileTypeCategory_(file.mimeType) }
        },
        'Last Modified': { 
          date: { start: Utilities.formatDate(file.lastModified, Session.getScriptTimeZone(), 'yyyy-MM-dd') }
        },
        'Investigation Priority': {
          select: { name: getInvestigationPriority_(file.name, file.mimeType) }
        }
      }
    };
    
    notionFetch_(token, 'https://api.notion.com/v1/pages', 'post', payload);
    return 'created';
  }
}

// Intelligent FIELD-based file classification
function classifyFile_(fileName, mimeType, filePath) {
  const name = fileName.toLowerCase();
  const path = filePath.toLowerCase();
  const entities = new Set();
  const topics = new Set();
  
  // Entity detection based on FIELD patterns and your specific data
  if (name.includes('trust') || name.includes('deed')) entities.add('Trust Structure');
  if (name.includes('rich') || name.includes('jacques') || name.includes('susan')) entities.add('Rich Family');
  if (name.includes('berjak') || name.includes('ansevata') || name.includes('centosa')) entities.add('Corporate Entity');
  if (name.includes('bank') || name.includes('bekb') || name.includes('nab')) entities.add('Financial Institution');
  if (name.includes('court') || name.includes('legal') || name.includes('hunt')) entities.add('Legal Entity');
  if (name.includes('ibac') || name.includes('police') || name.includes('gov')) entities.add('Government Authority');
  if (name.includes('panama') || name.includes('offshore')) entities.add('Offshore Structure');
  if (name.includes('mortgage') || name.includes('loan')) entities.add('Financial Obligation');
  if (name.includes('walkerville') || name.includes('mornington')) entities.add('Property');
  
  // Topic classification with investigation focus  
  if (mimeType.includes('pdf') && name.includes('statement')) topics.add('Financial Records');
  if (name.includes('agreement') || name.includes('contract')) topics.add('Legal Documents');
  if (name.includes('correspondence') || name.includes('letter') || name.includes('email')) topics.add('Communications');
  if (name.includes('tax') || name.includes('invoice')) topics.add('Tax Documents');
  if (name.includes('mortgage') || name.includes('discharge')) topics.add('Property Finance');
  if (name.includes('easement') || name.includes('covenant')) topics.add('Property Rights');
  if (name.includes('planning') || name.includes('permit')) topics.add('Planning Documents');
  if (name.includes('police') || name.includes('statement to police')) topics.add('Law Enforcement');
  if (name.includes('password') || name.includes('keychain')) topics.add('Digital Security');
  
  // Default classifications for FIELD system
  if (entities.size === 0) entities.add('Unclassified');
  if (topics.size === 0) {
    if (mimeType.includes('pdf')) topics.add('Document');
    else if (mimeType.includes('image')) topics.add('Evidence');
    else topics.add('Intake');
  }
  
  return { 
    entities: Array.from(entities), 
    topics: Array.from(topics) 
  };
}

// Determine file type category for filtering
function getFileTypeCategory_(mimeType) {
  if (mimeType.includes('pdf')) return 'PDF Document';
  if (mimeType.includes('word') || mimeType.includes('document')) return 'Word Document';
  if (mimeType.includes('image')) return 'Image';
  if (mimeType.includes('spreadsheet')) return 'Spreadsheet';
  if (mimeType.includes('text')) return 'Text File';
  return 'Other';
}

// Determine investigation priority based on content analysis
function getInvestigationPriority_(fileName, mimeType) {
  const name = fileName.toLowerCase();
  
  // High priority indicators
  if (name.includes('panama') || name.includes('offshore')) return 'Critical';
  if (name.includes('fraud') || name.includes('police') || name.includes('ibac')) return 'Critical';
  if (name.includes('trust deed') || name.includes('corporate')) return 'High';
  if (name.includes('financial') || name.includes('bank statement')) return 'High';
  if (name.includes('legal') || name.includes('court')) return 'High';
  if (name.includes('mortgage') || name.includes('property')) return 'Medium';
  if (name.includes('correspondence') || name.includes('email')) return 'Medium';
  
  return 'Standard';
}

// Query database for existing pages by Source Link
function queryBySourceLink_(token, databaseId, url) {
  const payload = {
    filter: {
      property: 'Source Link',
      url: { equals: url }
    },
    page_size: 1
  };
  return notionFetch_(token, 'https://api.notion.com/v1/databases/' + databaseId + '/query', 'post', payload);
}

// Robust Notion API wrapper with error handling and logging
function notionFetch_(token, url, method, payload) {
  try {
    const options = {
      method: method.toUpperCase(),
      contentType: 'application/json',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Notion-Version': '2022-06-28'
      },
      muteHttpExceptions: true
    };
    
    if (payload) {
      options.payload = JSON.stringify(payload);
    }
    
    const response = UrlFetchApp.fetch(url, options);
    const code = response.getResponseCode();
    const body = response.getContentText() || '';
    
    if (code >= 300) {
      console.warn(`🚨 Notion API error ${code} for ${method.toUpperCase()} ${url}: ${body.substring(0, 200)}`);
      
      // Handle rate limiting
      if (code === 429) {
        console.log('⏳ Rate limited, waiting 5 seconds...');
        Utilities.sleep(5000);
        return notionFetch_(token, url, method, payload); // Retry
      }
      
      return { error: true, code: code, message: body };
    }
    
    try {
      return JSON.parse(body);
    } catch (parseError) {
      return { raw: body, code: code };
    }
    
  } catch (error) {
    console.error(`💥 Network error calling Notion API: ${error.message}`);
    throw error;
  }
}

/**
 * Setup and utility functions
 */

// One-time setup function
function setupFieldSync() {
  console.log('🛠️ Setting up FIELD Data_Lake sync system...');
  
  const props = PropertiesService.getScriptProperties();
  
  // Test folder access
  try {
    const folderId = props.getProperty('FOLDER_ID') || '1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ';
    const folder = DriveApp.getFolderById(folderId);
    console.log(`✅ Drive folder access confirmed: ${folder.getName()}`);
  } catch (error) {
    console.error(`❌ Cannot access Drive folder: ${error.message}`);
    return;
  }
  
  // Test Notion connection
  const token = props.getProperty('NOTION_TOKEN');
  const databaseId = props.getProperty('NOTION_DATABASE_ID');
  
  if (!token || !databaseId) {
    console.error('❌ Please set NOTION_TOKEN and NOTION_DATABASE_ID in Script Properties');
    return;
  }
  
  try {
    const testResponse = notionFetch_(token, `https://api.notion.com/v1/databases/${databaseId}`, 'get');
    if (testResponse.error) {
      throw new Error(testResponse.message);
    }
    console.log('✅ Notion database connection confirmed');
  } catch (error) {
    console.error(`❌ Notion connection failed: ${error.message}`);
    return;
  }
  
  console.log('🎯 Setup complete! Ready to create daily trigger.');
}

// Create daily trigger programmatically
function createDailyTrigger() {
  // Delete existing triggers
  ScriptApp.getProjectTriggers()
    .filter(trigger => trigger.getHandlerFunction() === 'syncDriveToNotion')
    .forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Create new trigger for 6 AM daily (Australia/Melbourne time)
  ScriptApp.newTrigger('syncDriveToNotion')
    .timeBased()
    .everyDays(1)
    .atHour(6)
    .create();
  
  console.log('⏰ Daily trigger created for 6:00 AM Melbourne time');
}

// Test function with limited files
function testFieldSync() {
  console.log('🧪 Testing FIELD sync with first 5 files...');
  
  const props = PropertiesService.getScriptProperties();
  const folderId = props.getProperty('FOLDER_ID') || '1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ';
  
  const folder = DriveApp.getFolderById(folderId);
  const files = [];
  const fileIterator = folder.getFiles();
  
  // Get first 5 files for testing
  let count = 0;
  while (fileIterator.hasNext() && count < 5) {
    const f = fileIterator.next();
    files.push({
      id: f.getId(),
      name: f.getName(),
      url: f.getUrl(),
      lastModified: f.getLastUpdated(),
      size: f.getSize(),
      mimeType: f.getBlob().getContentType(),
      path: getFilePath_(f)
    });
    count++;
  }
  
  console.log(`🔬 Testing with ${files.length} files:`);
  files.forEach(file => {
    const classification = classifyFile_(file.name, file.mimeType, file.path);
    console.log(`📄 ${file.name}:`);
    console.log(`   Entities: ${classification.entities.join(', ')}`);
    console.log(`   Topics: ${classification.topics.join(', ')}`);
    console.log(`   Priority: ${getInvestigationPriority_(file.name, file.mimeType)}`);
  });
}

// Get last sync summary for monitoring
function getLastSyncSummary() {
  const props = PropertiesService.getScriptProperties();
  const summary = props.getProperty('LAST_SYNC_SUMMARY');
  
  if (summary) {
    console.log('📊 Last Sync Summary:', JSON.parse(summary));
    return JSON.parse(summary);
  } else {
    console.log('ℹ️ No sync history found');
    return null;
  }
}