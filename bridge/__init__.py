"""
FIELD Python/Swift Integration Bridge
====================================

Comprehensive bridging layer for macOS-level interaction between FIELD symbolic processors
and Apple applications using PyObjC and native Swift/Objective-C integration.

Core Components:
- Apple Events Bridge: Handles communication with Apple apps
- Field Node Router: Routes events between OBI-WAN, TATA, ATLAS, DOJO nodes
- Protocol Manager: Manages symbolic processor routing protocols
- Security Manager: Handles secure authentication and permissions
"""

from .apple_integration import (
    AppleEventsBridge,
    FieldNodeRouter,
    SecurityManager,
    AppleAppConnector
)
from .protocol import (
    FieldProtocol,
    EventRouter,
    SymbolicProcessor
)
from .swift_bridge import (
    SwiftBridge,
    DojoIntegration
)

__version__ = "1.0.0"
__author__ = "FIELD System Integration"

__all__ = [
    'AppleEventsBridge', 
    'FieldNodeRouter', 
    'SecurityManager',
    'AppleAppConnector',
    'FieldProtocol',
    'EventRouter',
    'SymbolicProcessor',
    'SwiftBridge',
    'DojoIntegration'
]
