"""
Apple Integration Module
========================

Core Apple Events and macOS integration for FIELD symbolic processors.
Handles communication with Apple applications through PyObjC.
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum

# PyObjC imports for macOS integration
try:
    import objc
    from Foundation import (
        NSAppleScript, NSString, NSDate, NSArray, NSDictionary,
        NSNotificationCenter, NSWorkspace, NSBundle, NSUserDefaults
    )
    from AppKit import (
        NSApplication, NSWorkspace, NSAppleEventManager,
        NSApplicationDidBecomeActiveNotification,
        NSApplicationDidResignActiveNotification
    )
    from ScriptingBridge import SBApplication
    PYOBJC_AVAILABLE = True
except ImportError as e:
    logging.warning(f"PyObjC not available: {e}. Apple integration will be limited.")
    PYOBJC_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FieldNodeType(Enum):
    """FIELD Node Types"""
    OBI_WAN = "OBI-WAN"
    TATA = "TATA"
    ATLAS = "ATLAS"
    DOJO = "DOJO"


class AppleAppType(Enum):
    """Supported Apple Applications"""
    FINDER = "com.apple.finder"
    SAFARI = "com.apple.Safari"
    MAIL = "com.apple.mail"
    MESSAGES = "com.apple.MobileSMS"
    NOTES = "com.apple.Notes"
    CALENDAR = "com.apple.iCal"
    CONTACTS = "com.apple.AddressBook"
    PHOTOS = "com.apple.Photos"
    MUSIC = "com.apple.Music"
    XCODE = "com.apple.dt.Xcode"


@dataclass
class FieldEvent:
    """FIELD Node Event Structure"""
    node_type: FieldNodeType
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    target_apps: List[AppleAppType] = None
    metadata: Dict[str, Any] = None


@dataclass
class AppleEvent:
    """Apple Application Event Structure"""
    app_type: AppleAppType
    event_class: str
    event_id: str
    parameters: Dict[str, Any]
    timestamp: datetime
    source_node: FieldNodeType = None


class SecurityManager:
    """Security and permissions manager for Apple integration"""
    
    def __init__(self):
        self.authenticated_apps = set()
        self.permission_cache = {}
        self.keychain_service = "com.field.bridge.security"
    
    def request_permissions(self, app_types: List[AppleAppType]) -> Dict[AppleAppType, bool]:
        """Request permissions for specified Apple applications"""
        permissions = {}
        
        for app_type in app_types:
            try:
                if PYOBJC_AVAILABLE:
                    # Check if app is running and accessible
                    workspace = NSWorkspace.sharedWorkspace()
                    running_apps = workspace.runningApplications()
                    
                    app_found = any(
                        app.bundleIdentifier() == app_type.value 
                        for app in running_apps
                    )
                    
                    permissions[app_type] = app_found
                    if app_found:
                        self.authenticated_apps.add(app_type)
                        logger.info(f"Permission granted for {app_type.value}")
                    else:
                        logger.warning(f"App not running: {app_type.value}")
                else:
                    permissions[app_type] = False
                    logger.warning("PyObjC not available - cannot check app permissions")
                    
            except Exception as e:
                logger.error(f"Error requesting permission for {app_type.value}: {e}")
                permissions[app_type] = False
        
        self.permission_cache.update(permissions)
        return permissions
    
    def is_authorized(self, app_type: AppleAppType) -> bool:
        """Check if app is authorized"""
        return app_type in self.authenticated_apps
    
    def store_credentials(self, service: str, credentials: Dict[str, Any]) -> bool:
        """Store credentials securely (simplified implementation)"""
        try:
            # In a real implementation, this would use macOS Keychain
            credentials_file = os.path.expanduser(f"~/.field_bridge_{service}.json")
            with open(credentials_file, 'w') as f:
                json.dump(credentials, f)
            logger.info(f"Credentials stored for {service}")
            return True
        except Exception as e:
            logger.error(f"Error storing credentials for {service}: {e}")
            return False
    
    def retrieve_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored credentials"""
        try:
            credentials_file = os.path.expanduser(f"~/.field_bridge_{service}.json")
            if os.path.exists(credentials_file):
                with open(credentials_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error retrieving credentials for {service}: {e}")
        return None


class AppleAppConnector:
    """Individual Apple Application Connector"""
    
    def __init__(self, app_type: AppleAppType, security_manager: SecurityManager):
        self.app_type = app_type
        self.security_manager = security_manager
        self.sb_application = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """Connect to the Apple application"""
        if not PYOBJC_AVAILABLE:
            logger.error("PyObjC not available - cannot connect to Apple apps")
            return False
            
        if not self.security_manager.is_authorized(self.app_type):
            logger.error(f"Not authorized to connect to {self.app_type.value}")
            return False
        
        try:
            self.sb_application = SBApplication.applicationWithBundleIdentifier_(
                self.app_type.value
            )
            
            if self.sb_application:
                self.is_connected = True
                logger.info(f"Connected to {self.app_type.value}")
                return True
            else:
                logger.error(f"Failed to connect to {self.app_type.value}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to {self.app_type.value}: {e}")
            return False
    
    def send_apple_event(self, event: AppleEvent) -> bool:
        """Send Apple Event to the connected application"""
        if not self.is_connected:
            logger.error(f"Not connected to {self.app_type.value}")
            return False
        
        try:
            # Create and send Apple Event based on event type
            if self.app_type == AppleAppType.FINDER:
                return self._handle_finder_event(event)
            elif self.app_type == AppleAppType.SAFARI:
                return self._handle_safari_event(event)
            elif self.app_type == AppleAppType.MAIL:
                return self._handle_mail_event(event)
            elif self.app_type == AppleAppType.NOTES:
                return self._handle_notes_event(event)
            else:
                return self._handle_generic_event(event)
                
        except Exception as e:
            logger.error(f"Error sending Apple Event to {self.app_type.value}: {e}")
            return False
    
    def _handle_finder_event(self, event: AppleEvent) -> bool:
        """Handle Finder-specific events"""
        if event.event_class == "file_operation":
            if event.event_id == "reveal_file":
                file_path = event.parameters.get("file_path")
                if file_path:
                    script = f'tell application "Finder" to reveal POSIX file "{file_path}"'
                    return self._execute_applescript(script)
        return False
    
    def _handle_safari_event(self, event: AppleEvent) -> bool:
        """Handle Safari-specific events"""
        if event.event_class == "navigation":
            if event.event_id == "open_url":
                url = event.parameters.get("url")
                if url:
                    script = f'tell application "Safari" to open location "{url}"'
                    return self._execute_applescript(script)
        return False
    
    def _handle_mail_event(self, event: AppleEvent) -> bool:
        """Handle Mail-specific events"""
        if event.event_class == "compose":
            if event.event_id == "new_message":
                recipient = event.parameters.get("recipient", "")
                subject = event.parameters.get("subject", "")
                body = event.parameters.get("body", "")
                
                script = f'''
                tell application "Mail"
                    set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}"}}
                    tell newMessage to make new to recipient at end of to recipients with properties {{address:"{recipient}"}}
                    activate
                end tell
                '''
                return self._execute_applescript(script)
        return False
    
    def _handle_notes_event(self, event: AppleEvent) -> bool:
        """Handle Notes-specific events"""
        if event.event_class == "document":
            if event.event_id == "create_note":
                title = event.parameters.get("title", "FIELD Note")
                content = event.parameters.get("content", "")
                
                script = f'''
                tell application "Notes"
                    make new note with properties {{name:"{title}", body:"{content}"}}
                    activate
                end tell
                '''
                return self._execute_applescript(script)
        return False
    
    def _handle_generic_event(self, event: AppleEvent) -> bool:
        """Handle generic Apple Events"""
        try:
            # Basic activation
            if event.event_class == "application" and event.event_id == "activate":
                script = f'tell application id "{self.app_type.value}" to activate'
                return self._execute_applescript(script)
        except Exception as e:
            logger.error(f"Error handling generic event: {e}")
        return False
    
    def _execute_applescript(self, script: str) -> bool:
        """Execute AppleScript safely"""
        try:
            if PYOBJC_AVAILABLE:
                apple_script = NSAppleScript.alloc().initWithSource_(script)
                result, error = apple_script.executeAndReturnError_(None)
                
                if error:
                    logger.error(f"AppleScript error: {error}")
                    return False
                
                logger.info(f"AppleScript executed successfully: {script[:50]}...")
                return True
            else:
                logger.error("PyObjC not available - cannot execute AppleScript")
                return False
                
        except Exception as e:
            logger.error(f"Error executing AppleScript: {e}")
            return False


class FieldNodeRouter:
    """Router for FIELD node events to Apple applications"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security_manager = security_manager
        self.app_connectors = {}
        self.event_handlers = {}
        self.routing_rules = {}
        self._setup_default_routing()
    
    def _setup_default_routing(self):
        """Setup default routing rules for FIELD nodes"""
        self.routing_rules = {
            FieldNodeType.OBI_WAN: {
                "data_intake": [AppleAppType.MAIL, AppleAppType.NOTES],
                "file_operations": [AppleAppType.FINDER],
                "web_research": [AppleAppType.SAFARI]
            },
            FieldNodeType.TATA: {
                "validation": [AppleAppType.NOTES, AppleAppType.CALENDAR],
                "documentation": [AppleAppType.NOTES],
                "analysis_results": [AppleAppType.MAIL]
            },
            FieldNodeType.ATLAS: {
                "consciousness_mapping": [AppleAppType.PHOTOS, AppleAppType.NOTES],
                "sacred_geometry": [AppleAppType.NOTES],
                "visualization": [AppleAppType.PHOTOS]
            },
            FieldNodeType.DOJO: {
                "interface_events": [AppleAppType.XCODE],
                "system_monitoring": [AppleAppType.NOTES],
                "user_interaction": [AppleAppType.MESSAGES]
            }
        }
    
    def initialize_connectors(self) -> bool:
        """Initialize all required Apple app connectors"""
        # Get all unique app types from routing rules
        required_apps = set()
        for node_rules in self.routing_rules.values():
            for app_list in node_rules.values():
                required_apps.update(app_list)
        
        # Request permissions for all required apps
        permissions = self.security_manager.request_permissions(list(required_apps))
        
        # Initialize connectors for authorized apps
        success_count = 0
        for app_type in required_apps:
            if permissions.get(app_type, False):
                connector = AppleAppConnector(app_type, self.security_manager)
                if connector.connect():
                    self.app_connectors[app_type] = connector
                    success_count += 1
                    logger.info(f"Initialized connector for {app_type.value}")
                else:
                    logger.error(f"Failed to initialize connector for {app_type.value}")
            else:
                logger.warning(f"No permission for {app_type.value}")
        
        logger.info(f"Initialized {success_count}/{len(required_apps)} app connectors")
        return success_count > 0
    
    def route_field_event(self, field_event: FieldEvent) -> bool:
        """Route FIELD event to appropriate Apple applications"""
        try:
            # Get routing rules for the node type
            node_rules = self.routing_rules.get(field_event.node_type, {})
            target_apps = node_rules.get(field_event.event_type, [])
            
            # Override with explicit target apps if provided
            if field_event.target_apps:
                target_apps = field_event.target_apps
            
            if not target_apps:
                logger.warning(f"No routing rules for {field_event.node_type.value}:{field_event.event_type}")
                return False
            
            # Convert FIELD event to Apple events and send
            success_count = 0
            for app_type in target_apps:
                if app_type in self.app_connectors:
                    apple_event = self._convert_field_to_apple_event(field_event, app_type)
                    if self.app_connectors[app_type].send_apple_event(apple_event):
                        success_count += 1
                        logger.info(f"Routed event to {app_type.value}")
                    else:
                        logger.error(f"Failed to route event to {app_type.value}")
                else:
                    logger.warning(f"No connector available for {app_type.value}")
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error routing FIELD event: {e}")
            return False
    
    def _convert_field_to_apple_event(self, field_event: FieldEvent, app_type: AppleAppType) -> AppleEvent:
        """Convert FIELD event to Apple Event format"""
        # Default conversion - customize based on event types
        apple_event = AppleEvent(
            app_type=app_type,
            event_class="field_integration",
            event_id=field_event.event_type,
            parameters=field_event.data,
            timestamp=field_event.timestamp,
            source_node=field_event.node_type
        )
        
        # Customize based on specific field event types
        if field_event.event_type == "data_intake" and app_type == AppleAppType.NOTES:
            apple_event.event_class = "document"
            apple_event.event_id = "create_note"
            apple_event.parameters = {
                "title": f"FIELD {field_event.node_type.value} Data Intake",
                "content": json.dumps(field_event.data, indent=2)
            }
        
        elif field_event.event_type == "file_operations" and app_type == AppleAppType.FINDER:
            apple_event.event_class = "file_operation"
            apple_event.event_id = "reveal_file"
            apple_event.parameters = {
                "file_path": field_event.data.get("file_path", "")
            }
        
        elif field_event.event_type == "web_research" and app_type == AppleAppType.SAFARI:
            apple_event.event_class = "navigation"
            apple_event.event_id = "open_url"
            apple_event.parameters = {
                "url": field_event.data.get("url", "")
            }
        
        return apple_event
    
    def add_custom_routing_rule(self, node_type: FieldNodeType, event_type: str, target_apps: List[AppleAppType]):
        """Add custom routing rule"""
        if node_type not in self.routing_rules:
            self.routing_rules[node_type] = {}
        
        self.routing_rules[node_type][event_type] = target_apps
        logger.info(f"Added routing rule: {node_type.value}:{event_type} -> {[app.value for app in target_apps]}")


class AppleEventsBridge:
    """Main Apple Events Bridge for FIELD integration"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.field_router = FieldNodeRouter(self.security_manager)
        self.is_initialized = False
        self.event_queue = asyncio.Queue()
        self.processing_task = None
    
    async def initialize(self) -> bool:
        """Initialize the Apple Events Bridge"""
        try:
            logger.info("Initializing Apple Events Bridge...")
            
            # Initialize connectors
            if not self.field_router.initialize_connectors():
                logger.error("Failed to initialize Apple app connectors")
                return False
            
            # Start event processing
            self.processing_task = asyncio.create_task(self._process_events())
            
            self.is_initialized = True
            logger.info("Apple Events Bridge initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Apple Events Bridge: {e}")
            return False
    
    async def send_field_event(self, field_event: FieldEvent) -> bool:
        """Send FIELD event through the bridge"""
        if not self.is_initialized:
            logger.error("Bridge not initialized")
            return False
        
        try:
            await self.event_queue.put(field_event)
            logger.info(f"Queued FIELD event: {field_event.node_type.value}:{field_event.event_type}")
            return True
        except Exception as e:
            logger.error(f"Error queueing FIELD event: {e}")
            return False
    
    async def _process_events(self):
        """Process events from the queue"""
        while True:
            try:
                field_event = await self.event_queue.get()
                success = self.field_router.route_field_event(field_event)
                
                if success:
                    logger.info(f"Successfully processed event: {field_event.node_type.value}:{field_event.event_type}")
                else:
                    logger.error(f"Failed to process event: {field_event.node_type.value}:{field_event.event_type}")
                
                self.event_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing event: {e}")
    
    async def shutdown(self):
        """Shutdown the bridge"""
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Apple Events Bridge shutdown complete")


# Export main classes
__all__ = [
    'AppleEventsBridge',
    'FieldNodeRouter', 
    'SecurityManager',
    'AppleAppConnector',
    'FieldEvent',
    'AppleEvent',
    'FieldNodeType',
    'AppleAppType'
]
