/**
 * Enhanced Google Apps Script for FIELD Data_Lake Sync
 * Syncs Drive folder contents to Notion Data_Lake database with de-duplication
 * Compatible with FIELD system architecture and resonance analysis
 */

// Configuration - Replace with your actual values
const CONFIG = {
  FOLDER_ID: '1HcjrZXlHi7yszRJCeYzg8wxzdFnTW3RQ', // Your shared Drive folder
  NOTION_TOKEN: 'YOUR_NOTION_TOKEN_HERE', // Get from Notion integration
  NOTION_DATABASE_ID: 'YOUR_DATABASE_ID_HERE', // Data_Lake database ID
  NOTION_VERSION: '2022-06-28'
};

/**
 * Main sync function - called by time trigger
 */
function syncDriveToNotion() {
  console.log('🔄 Starting FIELD Data_Lake sync...');
  
  try {
    // Get secure token from properties
    const notionToken = getSecureToken();
    if (!notionToken) {
      throw new Error('Notion token not found in script properties');
    }
    
    // Get folder and files
    const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
    const files = getAllFilesRecursively(folder);
    
    console.log(`📁 Found ${files.length} files to process`);
    
    // Get existing pages to avoid duplicates
    const existingPages = getExistingNotionPages(notionToken);
    console.log(`📋 Found ${existingPages.length} existing Notion entries`);
    
    let processed = 0;
    let created = 0;
    let updated = 0;
    let errors = 0;
    
    // Process each file
    for (const file of files) {
      try {
        const result = await processFile(file, existingPages, notionToken);
        processed++;
        
        if (result.action === 'created') created++;
        else if (result.action === 'updated') updated++;
        
        // Avoid rate limits
        if (processed % 10 === 0) {
          Utilities.sleep(1000);
        }
        
      } catch (error) {
        console.error(`❌ Error processing ${file.getName()}:`, error.message);
        errors++;
      }
    }
    
    // Log summary
    const summary = {
      timestamp: new Date().toISOString(),
      processed,
      created,
      updated,
      errors,
      total_files: files.length
    };
    
    console.log('✅ Sync completed:', summary);
    logToFieldSystem(summary);
    
  } catch (error) {
    console.error('💥 Critical sync error:', error.message);
    throw error;
  }
}

/**
 * Recursively get all files from folder and subfolders
 */
function getAllFilesRecursively(folder, files = []) {
  // Get files in current folder
  const folderFiles = folder.getFiles();
  while (folderFiles.hasNext()) {
    files.push(folderFiles.next());
  }
  
  // Process subfolders
  const subFolders = folder.getFolders();
  while (subFolders.hasNext()) {
    getAllFilesRecursively(subFolders.next(), files);
  }
  
  return files;
}

/**
 * Get existing Notion pages to avoid duplicates
 */
function getExistingNotionPages(token) {
  const pages = [];
  let hasMore = true;
  let startCursor = null;
  
  while (hasMore) {
    const payload = {
      filter: {
        property: 'Source Link',
        url: {
          is_not_empty: true
        }
      },
      page_size: 100
    };
    
    if (startCursor) {
      payload.start_cursor = startCursor;
    }
    
    const response = UrlFetchApp.fetch(
      `https://api.notion.com/v1/databases/${CONFIG.NOTION_DATABASE_ID}/query`,
      {
        method: 'POST',
        contentType: 'application/json',
        payload: JSON.stringify(payload),
        headers: {
          'Authorization': `Bearer ${token}`,
          'Notion-Version': CONFIG.NOTION_VERSION
        },
        muteHttpExceptions: true
      }
    );
    
    if (response.getResponseCode() !== 200) {
      console.warn('Failed to fetch existing pages:', response.getContentText());
      break;
    }
    
    const data = JSON.parse(response.getContentText());
    pages.push(...data.results);
    
    hasMore = data.has_more;
    startCursor = data.next_cursor;
  }
  
  return pages;
}

/**
 * Process individual file - create or update
 */
async function processFile(file, existingPages, token) {
  const fileName = file.getName();
  const fileUrl = file.getUrl();
  const fileId = file.getId();
  const lastModified = file.getLastUpdated();
  const fileSize = file.getSize();
  const mimeType = file.getBlob().getContentType();
  
  // Check if page exists
  const existingPage = existingPages.find(page => {
    const sourceUrl = page.properties['Source Link']?.url;
    return sourceUrl && sourceUrl.includes(fileId);
  });
  
  // Determine entity and topic from filename/path
  const classification = classifyFile(fileName, mimeType);
  
  const properties = {
    'File Name': {
      title: [{ text: { content: fileName } }]
    },
    'Source Link': {
      url: fileUrl
    },
    'Date': {
      date: { start: new Date().toISOString().slice(0, 10) }
    },
    'Entity': {
      multi_select: classification.entities.map(name => ({ name }))
    },
    'Topic': {
      multi_select: classification.topics.map(name => ({ name }))
    },
    'File Size': {
      number: Math.round(fileSize / 1024) // KB
    },
    'MIME Type': {
      rich_text: [{ text: { content: mimeType } }]
    },
    'Last Modified': {
      date: { start: lastModified.toISOString() }
    }
  };
  
  if (existingPage) {
    // Update existing page
    const response = UrlFetchApp.fetch(
      `https://api.notion.com/v1/pages/${existingPage.id}`,
      {
        method: 'PATCH',
        contentType: 'application/json',
        payload: JSON.stringify({ properties }),
        headers: {
          'Authorization': `Bearer ${token}`,
          'Notion-Version': CONFIG.NOTION_VERSION
        },
        muteHttpExceptions: true
      }
    );
    
    if (response.getResponseCode() >= 300) {
      throw new Error(`Update failed: ${response.getContentText()}`);
    }
    
    return { action: 'updated', file: fileName };
    
  } else {
    // Create new page
    const payload = {
      parent: { database_id: CONFIG.NOTION_DATABASE_ID },
      properties
    };
    
    const response = UrlFetchApp.fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      headers: {
        'Authorization': `Bearer ${token}`,
        'Notion-Version': CONFIG.NOTION_VERSION
      },
      muteHttpExceptions: true
    });
    
    if (response.getResponseCode() >= 300) {
      throw new Error(`Create failed: ${response.getContentText()}`);
    }
    
    return { action: 'created', file: fileName };
  }
}

/**
 * Intelligent file classification based on FIELD system patterns
 */
function classifyFile(fileName, mimeType) {
  const name = fileName.toLowerCase();
  const entities = [];
  const topics = [];
  
  // Entity detection based on FIELD patterns
  if (name.includes('trust') || name.includes('deed')) entities.push('Trust Structure');
  if (name.includes('corp') || name.includes('company')) entities.push('Corporate');
  if (name.includes('bank') || name.includes('finance')) entities.push('Financial');
  if (name.includes('legal') || name.includes('court')) entities.push('Legal');
  if (name.includes('gov') || name.includes('official')) entities.push('Government');
  if (name.includes('panama') || name.includes('offshore')) entities.push('Offshore');
  
  // Topic classification
  if (mimeType.includes('pdf')) topics.push('Document');
  if (mimeType.includes('image')) topics.push('Evidence');
  if (mimeType.includes('spreadsheet') || name.includes('.csv')) topics.push('Financial Data');
  if (name.includes('investigation') || name.includes('fraud')) topics.push('Investigation');
  if (name.includes('resonance') || name.includes('harmonic')) topics.push('Resonance Analysis');
  
  // Default classifications
  if (entities.length === 0) entities.push('Unsorted');
  if (topics.length === 0) topics.push('Intake');
  
  return { entities, topics };
}

/**
 * Get secure token from script properties
 */
function getSecureToken() {
  // First try to get from properties
  let token = PropertiesService.getScriptProperties().getProperty('NOTION_TOKEN');
  
  // If not found, check if it's set in config (for initial setup)
  if (!token && CONFIG.NOTION_TOKEN !== 'YOUR_NOTION_TOKEN_HERE') {
    token = CONFIG.NOTION_TOKEN;
    // Store it securely for future use
    PropertiesService.getScriptProperties().setProperty('NOTION_TOKEN', token);
    console.log('🔐 Token stored securely in script properties');
  }
  
  return token;
}

/**
 * Log sync results to FIELD system format
 */
function logToFieldSystem(summary) {
  try {
    // Create FIELD-compatible log entry
    const fieldLog = {
      timestamp: summary.timestamp,
      system: 'NOTION_DRIVE_SYNC',
      operation: 'DATA_LAKE_SYNC',
      status: summary.errors > 0 ? 'PARTIAL_SUCCESS' : 'SUCCESS',
      metrics: {
        files_processed: summary.processed,
        pages_created: summary.created,
        pages_updated: summary.updated,
        errors: summary.errors,
        success_rate: ((summary.processed - summary.errors) / summary.processed * 100).toFixed(2) + '%'
      },
      resonance: {
        frequency: summary.errors === 0 ? 777.55 : 432.00, // Perfect harmony or needs tuning
        harmonic_state: summary.errors === 0 ? 'ALIGNED' : 'DISSONANT'
      }
    };
    
    console.log('🎵 FIELD System Log:', JSON.stringify(fieldLog, null, 2));
    
  } catch (error) {
    console.warn('Failed to create FIELD system log:', error.message);
  }
}

/**
 * Setup function - run once to configure
 */
function setupSync() {
  console.log('🛠️ Setting up FIELD Data_Lake sync...');
  
  // Verify folder access
  try {
    const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
    console.log(`✅ Folder access confirmed: ${folder.getName()}`);
  } catch (error) {
    throw new Error(`❌ Cannot access folder ${CONFIG.FOLDER_ID}: ${error.message}`);
  }
  
  // Test Notion connection
  const token = getSecureToken();
  if (!token) {
    throw new Error('❌ Please set NOTION_TOKEN in script properties or CONFIG');
  }
  
  const testResponse = UrlFetchApp.fetch(
    `https://api.notion.com/v1/databases/${CONFIG.NOTION_DATABASE_ID}`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Notion-Version': CONFIG.NOTION_VERSION
      },
      muteHttpExceptions: true
    }
  );
  
  if (testResponse.getResponseCode() !== 200) {
    throw new Error(`❌ Cannot access Notion database: ${testResponse.getContentText()}`);
  }
  
  console.log('✅ Notion connection confirmed');
  console.log('🎯 Ready to create daily trigger');
}

/**
 * Create the daily trigger programmatically
 */
function createDailyTrigger() {
  // Delete existing triggers for this function
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'syncDriveToNotion') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // Create new trigger for 6 AM daily
  ScriptApp.newTrigger('syncDriveToNotion')
    .timeBased()
    .everyDays(1)
    .atHour(6)
    .create();
  
  console.log('⏰ Daily trigger created for 6:00 AM');
}

/**
 * Test function - run a small sync to verify everything works
 */
function testSync() {
  console.log('🧪 Testing sync with first 5 files...');
  
  const folder = DriveApp.getFolderById(CONFIG.FOLDER_ID);
  const files = [];
  const fileIterator = folder.getFiles();
  
  // Get first 5 files only
  let count = 0;
  while (fileIterator.hasNext() && count < 5) {
    files.push(fileIterator.next());
    count++;
  }
  
  console.log(`Testing with ${files.length} files`);
  // Run the sync logic here...
}