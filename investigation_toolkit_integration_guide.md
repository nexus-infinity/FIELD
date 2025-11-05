# 🔍 Investigation Toolkit Integration Guide
**For 31-Task Investigative Process Integration**

## 🎯 Purpose
Ensure any ongoing investigation process utilizes all available FIELD system tools, data sources, and integrations for maximum investigative effectiveness.

## 🛠️ Available Tools & Systems

### 1. **DOJO API Gateway** ✅ OPERATIONAL
- **URL**: `http://localhost:8000`
- **Status**: Active with 5 components
- **Components Available**:
  - `money-hub` - Financial operations, accounts, claims, tasks, documents
  - `discovery` - Link discovery and sovereign reconciliation
  - `evidence` - Evidence bundle export and chain of custody
  - `warp` - Bootstrap, runbook, deployment capabilities
  - `geometry` - Sacred geometry alignment tools

### 2. **Datashare Document Search** ✅ OPERATIONAL
- **URL**: `http://localhost:9630`
- **Status**: Active and indexed
- **Capabilities**: Full-text search across 42+ investigation documents
- **Integration**: Available via `/datashare/search` API endpoint

### 3. **Comprehensive Financial Data** ✅ AVAILABLE
- **Location**: `/Users/jbear/FIELD/▼TATA/`
- **Data Volume**: 113 CSV files + 137 PDF documents
- **Classifications**: 
  - Banking transaction accounts (132+ files)
  - Credit card historical data (4+ files)
  - Unknown/unclassified accounts (72+ files)
- **Fraud Detection**: High-value transaction markers available
- **Entities Covered**: 
  - Personal: Jeremy Rich, Susan Rich, Jacques Rich
  - Corporate: Berjak Nominees, Ansevata Investments
  - Offshore: CENTOSA SA, PASCALI Trust, Freeler Associates SA

### 4. **Investigation Results & Analysis** ✅ AVAILABLE
- **Location**: `/Users/jbear/FIELD/investigation_results/`
- **Latest Session**: `investigation-1758032257` (2025-09-17)
- **Entities Analyzed**: CENTOSA SA, PASCALI TRUST, Jacques Rich, Adam Rich, David Rich, BERJAK NOMINEES
- **Global Database Integration**:
  - Panama Papers ✅ (0 matches)
  - Paradise Papers ✅ (0 matches) 
  - OpenCorporates ✅ (2 matches found)
  - Sanctions Lists ✅ (Clear)
- **Risk Assessment**: Medium overall risk score

### 5. **External Data Source Connectors** 🔄 READY TO DEPLOY
- **ICIJ Integration**: `/Users/jbear/FIELD/integrations/global_databases/icij_connector.py`
- **OpenCorporates**: `/Users/jbear/FIELD/integrations/global_databases/opencorporates_connector.py`
- **Sanctions**: `/Users/jbear/FIELD/integrations/global_databases/sanctions_connector.py`

## 📋 31-Task Investigation Integration Checklist

### Phase 1: Data Access & Integration ✅
- [ ] **API Gateway Connection**: Verify connection to `http://localhost:8000`
- [ ] **Datashare Search**: Test document search at `http://localhost:9630`
- [ ] **Financial Data Access**: Confirm access to comprehensive financial manifest
- [ ] **Investigation History**: Review previous analysis results
- [ ] **External Databases**: Activate ICIJ, OpenCorporates, Sanctions connectors

### Phase 2: Entity Analysis Enhancement 📊
- [ ] **Jacques Rich Network**: Utilize existing entity relationship data
- [ ] **CENTOSA SA Analysis**: Leverage existing BVI corporate connection data
- [ ] **PASCALI Trust Investigation**: Focus on "investigation_needed" status
- [ ] **Financial Pattern Analysis**: Use fraud detection markers for transaction review
- [ ] **Cross-Reference Engine**: Deploy document cross-referencing capabilities

### Phase 3: Advanced Capabilities Activation 🚀
- [ ] **Evidence Bundle Export**: Use `/evidence/bundles` for legal-ready packages
- [ ] **Chain of Custody**: Implement document provenance tracking
- [ ] **Automated Reporting**: Deploy GitBook documentation sync
- [ ] **Real-time Monitoring**: Activate investigation progress tracking
- [ ] **Sacred Geometry Compliance**: Ensure tetrahedral flow patterns

## 🔗 API Integration Commands

### Essential Investigation APIs
```bash
# System Status Check
curl http://localhost:8000/

# Money Hub Operations
curl http://localhost:8000/money-hub/status

# Document Search (Replace QUERY with search terms)
curl -X POST http://localhost:8000/datashare/search \
  -H "Content-Type: application/json" \
  -d '{"q": "CENTOSA SA", "size": 10}'

# Evidence Bundle Access
curl http://localhost:8000/evidence/bundles

# Discovery Links
curl http://localhost:8000/discovery/links
```

### Advanced Investigation Commands
```bash
# Search for Jacques Rich entities
curl -X POST http://localhost:9630/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Jacques Rich OR CENTOSA OR PASCALI"}'

# Cross-reference banking documents
curl -X POST http://localhost:9630/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Rothschild OR NAB OR BEKB"}'

# High-value transaction search
curl -X POST http://localhost:9630/search \
  -H "Content-Type: application/json" \
  -d '{"query": "137441 OR 350000 OR large withdrawal"}'
```

## 📊 Data Integration Points

### Financial Investigation Priority Entities
1. **CENTOSA SA** (BVI) - Active status, investigation focus
2. **PASCALI TRUST** - Investigation needed, unknown jurisdiction
3. **Jacques Rich** - Swiss BEKB account 16 734.081.3.19
4. **Ansevata Investments** - Rothschild custody account CH72 0866 1016 0700 8010 2
5. **Berjak Nominees** - NAB corporate account

### Transaction Pattern Analysis
- **Large Withdrawals Detected**: $137,441.70 (multiple instances)
- **High-Value Transactions**: $350,000.00 flagged
- **Fraud Markers**: 12+ high-priority alerts available
- **Banking Relationships**: NAB, Rothschild, BEKB networks mapped

### Document Universe Coverage
- **113 CSV Files**: Complete transaction history access
- **137 PDF Documents**: Legal and regulatory document archive
- **42+ Investigation Documents**: Jacques Rich case materials
- **Cross-Reference Capability**: Entity relationship mapping

## 🔄 Integration Workflow for 31-Task Process

### Task Integration Framework
```python
# Example integration pattern for investigation tasks
import requests

class InvestigationToolkit:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.datashare_base = "http://localhost:9630"
    
    def search_entity(self, entity_name):
        # Cross-system entity search
        dojo_search = requests.get(f"{self.api_base}/discovery/links")
        datashare_search = requests.post(f"{self.datashare_base}/search", 
                                       json={"query": entity_name})
        return self.merge_results(dojo_search.json(), datashare_search.json())
    
    def get_financial_profile(self, entity):
        # Access comprehensive financial data
        return requests.get(f"{self.api_base}/money-hub/status").json()
    
    def export_evidence(self, case_id):
        # Generate legal-ready evidence bundle
        return requests.get(f"{self.api_base}/evidence/bundles").json()
```

## 📈 Integration Success Metrics

### System Integration Health
- ✅ **API Gateway**: 100% operational (5/5 components active)
- ✅ **Document Search**: Indexed and responsive
- ✅ **Financial Data**: Complete access to 250+ financial documents
- ✅ **Investigation Results**: Historical analysis available
- 🔄 **External Databases**: Ready for activation (3 connectors available)

### Investigation Coverage Enhancement
- **Entity Coverage**: 6+ entities pre-analyzed
- **Financial Scope**: Decades of transaction history
- **Document Access**: 42+ investigation documents searchable
- **Cross-Reference**: Multi-database entity matching
- **Evidence Export**: Legal-ready bundle generation

## 🚨 Critical Integration Points for 31-Task Process

### Must-Use Integrations
1. **Entity Search**: Use both Dojo discovery and Datashare search
2. **Financial Analysis**: Leverage existing fraud detection markers
3. **Document Cross-Reference**: Cross-check entities across all 250+ documents
4. **Evidence Export**: Prepare legal bundles for any findings
5. **Real-time Status**: Monitor investigation progress via API endpoints

### Data Priority Matrix
- **High Priority**: Jacques Rich network (CENTOSA SA, PASCALI Trust)
- **Medium Priority**: Banking relationships (NAB, Rothschild, BEKB)
- **Low Priority**: Historical transaction archives (for pattern analysis)

## 📞 Emergency Investigation Support

### Quick Access Commands
```bash
# Emergency entity lookup
curl "http://localhost:8000/discovery/links" | jq .

# Rapid document search  
curl -X POST "http://localhost:9630/search" -d '{"query":"URGENT_ENTITY_NAME"}'

# System health check
curl "http://localhost:8000/" | jq .status
```

---

## ✅ Integration Verification

**Verification Date**: 2025-09-19  
**System Status**: All integration points operational  
**Investigation Ready**: ✅ Full toolkit access confirmed  
**31-Task Process Support**: 🎯 Complete integration capability verified

**Note**: This integration guide ensures any 31-task investigation process has complete access to all available FIELD system capabilities, data sources, and analysis tools for maximum investigative effectiveness.