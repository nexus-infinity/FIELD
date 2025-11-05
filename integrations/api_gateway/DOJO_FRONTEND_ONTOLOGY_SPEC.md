# DOJO Frontend Ontology Specification
## For dev0.app Vercel Frontend Development

**Version:** 2.0.0  
**Date:** 2025  
**Backend API:** DOJO Unified Intelligence API  
**Base URL:** `http://localhost:8000` (development) / `https://api.berjak2.com` (production)

---

## Executive Summary

This ontology defines the complete data model, relationships, and interaction patterns between the Vercel frontend (business-facing) and the DOJO Unified Intelligence backend. The system serves dual purposes:

1. **Business Intelligence**: Professional, credibility-focused presentation for clients, investors, and stakeholders
2. **Legal Evidence System**: Court-ready evidence management for prosecution and defense

The system includes an AI-driven narrative storytelling engine that crafts flowing, geometry-anchored narratives optimized for specific audiences and outcomes.

---

## Core Ontology Structure

### 1. Entity Types

#### 1.1 EvidenceItem (Base Entity)

The foundational entity representing any piece of validated information in the system.

```typescript
interface EvidenceItem {
  id: string;                      // Unique identifier: "EV_YYYYMMDD_HHMMSS_HASH"
  title: string;                   // Human-readable title
  summary: string;                 // Brief description (200 chars max)
  content: string;                 // Full content or reference
  sourceType: SourceType;          // Origin classification
  geometricPosition: GeometricPosition;  // Position in sacred tetrahedral structure
  temporalPhase: TemporalPhase;    // Time-based classification
  semanticCluster: string[];       // Thematic/topical groupings
  validationScore: number;         // 0.0-1.0: Geometric validation confidence
  chainOfCustody: ChainOfCustody;  // Provenance and integrity tracking
  createdAt: string;               // ISO 8601 timestamp
  updatedAt: string;               // ISO 8601 timestamp
  mediaReferences: MediaReference[];  // Associated visual/document assets
}

enum SourceType {
  EMAIL = "email",
  DOCUMENT = "document",
  DATABASE = "database",
  COURT_FILING = "court_filing",
  CORPORATE_RECORD = "corporate_record",
  POLICE_RECORD = "police_record",
  FINANCIAL_RECORD = "financial_record",
  TESTIMONY = "testimony",
  PHYSICAL_EVIDENCE = "physical_evidence"
}

interface GeometricPosition {
  tetrahedron: "SACRED_FIELD" | "FIELD_LIVING";  // Which tetrahedral structure
  vertex: "DOJO" | "OBI_WAN" | "TATA" | "ATLAS" | "AKRON" | "FIELD_DEV" | "FIELD_OOWL" | "FIELD_LIVING_APEX";
  resonanceFrequency: number;      // Hz: Solfeggio frequency alignment
  validationPath: string[];        // Geometric validation route through structure
}

interface TemporalPhase {
  phase: 1 | 2 | 3;                // Conspiracy phase (if applicable)
  periodStart: string;             // ISO 8601 date
  periodEnd: string | null;        // ISO 8601 date or null if ongoing
  phaseName: string;               // Human-readable phase name
  significance: string;            // Why this phase matters
}

interface ChainOfCustody {
  originalSource: string;          // Origin description
  acquisitionDate: string;         // ISO 8601 timestamp
  shaHash: string;                 // SHA-256 integrity hash
  custodyLog: CustodyEvent[];      // Complete custody history
  admissibilityRating: "HIGH" | "MEDIUM" | "LOW";
}

interface CustodyEvent {
  timestamp: string;               // ISO 8601
  actor: string;                   // Who handled it
  action: string;                  // What they did
  location: string;                // Where (geometric position or physical)
}

interface MediaReference {
  type: "image" | "video" | "audio" | "document" | "timeline" | "diagram";
  url: string;                     // Asset URL
  title: string;                   // Asset title
  description: string;             // Asset description
  thumbnailUrl?: string;           // Preview image URL
}
```

#### 1.2 BusinessIntel (extends EvidenceItem)

Evidence optimized for business/client presentation. Emphasizes credibility, heritage, and professional excellence.

```typescript
interface BusinessIntel extends EvidenceItem {
  businessRelevance: BusinessRelevance;
  tradingImpact: TradingImpact;
  clientConfidence: ClientConfidence;
  presentationMode: "PROFESSIONAL" | "TECHNICAL" | "EXECUTIVE";
}

interface BusinessRelevance {
  category: "HERITAGE" | "INNOVATION" | "TRANSPARENCY" | "INTEGRITY" | "CAPABILITY";
  businessValue: string;           // How this supports business operations
  clientMessage: string;           // What clients should understand from this
  credibilityBoost: number;        // 0.0-1.0: How much this increases trust
}

interface TradingImpact {
  operationalArea: string[];       // Which business areas affected
  historicalContext: string;       // Trading history context
  modernRelevance: string;         // How this applies to current operations
}

interface ClientConfidence {
  transparencyScore: number;       // 0.0-1.0
  professionalismIndicator: number; // 0.0-1.0
  trustMarker: boolean;            // Is this a key trust indicator?
}
```

#### 1.3 LegalIntel (extends EvidenceItem)

Evidence optimized for court/legal proceedings. Emphasizes admissibility, factual proof, and systematic patterns.

```typescript
interface LegalIntel extends EvidenceItem {
  legalRelevance: LegalRelevance;
  criminalCategory: CriminalCategory | null;
  fvioConnection: FVIOConnection | null;
  courtSummary: string;            // Court-ready one-paragraph summary
  exhibitNumber: string | null;    // Court exhibit identifier
}

interface LegalRelevance {
  caseType: "FVIO" | "CONSPIRACY" | "FRAUD" | "CORRUPTION" | "GENERAL";
  legalTheory: string;             // Which legal theory this supports
  prosecutionValue: number;        // 0.0-1.0: Strength for prosecution
  defenseValue: number;            // 0.0-1.0: Strength for defense
  admissibility: "HIGH" | "MEDIUM" | "LOW";
}

interface CriminalCategory {
  primaryOffense: string;          // Main criminal charge supported
  secondaryOffenses: string[];     // Additional charges supported
  jurisdiction: string;            // Legal jurisdiction
  statuteReferences: string[];     // Relevant legal statutes
}

interface FVIOConnection {
  matter: "ADAM_RICH_APPLICATION" | "POLICE_APPLICATION" | "GENERAL";
  hearingDate: string;             // ISO 8601 date
  relevanceToDefense: string;      // How this helps defense
  counterNarrativePower: number;   // 0.0-1.0: How well this counters their narrative
}
```

#### 1.4 Narrative

AI-generated storytelling output, attuned to specific audiences and outcomes.

```typescript
interface Narrative {
  narrativeId: string;             // "NARR_YYYYMMDD_HHMMSS"
  audience: Audience;              // Target audience
  purpose: Purpose;                // Intended outcome
  geometricStructure: string;      // Architectural presentation of truth
  semanticWeaving: SemanticWeaving; // Language choices for audience
  temporalFlow: TemporalPhase[];   // Chronological storytelling
  irrefutableAnchors: string[];    // Key truth points that cannot be disputed
  frequencyAttunement: FrequencyAttunement;  // Forecast/shadowcast analysis
  mediaElements: Record<string, MediaReference[]>;  // Visual components
  narrativeText: string;           // The actual crafted narrative
  successProbability: number;      // 0.0-1.0: Predicted effectiveness
  generatedAt: string;             // ISO 8601 timestamp
}

enum Audience {
  BUSINESS_CLIENT = "business_client",
  COURT_MAGISTRATE = "court_magistrate",
  INVESTOR = "investor",
  REGULATOR = "regulator",
  FAMILY_MEMBER = "family_member",
  PUBLIC = "public"
}

enum Purpose {
  CREDIBILITY = "credibility",
  PROSECUTION = "prosecution",
  DEFENSE = "defense",
  INVESTMENT = "investment",
  COMPLIANCE = "compliance",
  RECONCILIATION = "reconciliation",
  PUBLIC_AWARENESS = "public_awareness"
}

interface SemanticWeaving {
  framing: string;                 // Overall narrative framing
  keyTerms: string[];              // Emphasized vocabulary
  avoidTerms: string[];            // Vocabulary to avoid
  emphasis: string;                // Primary emphasis point
  tone: "professional" | "legal" | "technical" | "compassionate" | "authoritative";
}

interface FrequencyAttunement {
  primaryFrequency: string;        // Main resonance frequency (e.g., "528 Hz - Truth")
  secondaryFrequency: string;      // Supporting frequency
  attunementStrategy: string;      // How to align with audience
  successProbability: number;      // 0.0-1.0: Predicted success
  forecast: string;                // Positive outcome prediction
  shadowcast: string;              // Risk/challenge prediction
}
```

---

### 2. Relationship Types

Relationships connect entities and create the semantic graph structure.

```typescript
interface Relationship {
  relationshipId: string;
  sourceEntityId: string;
  targetEntityId: string;
  relationshipType: RelationType;
  strength: number;                // 0.0-1.0: Relationship strength
  description: string;
  metadata: Record<string, any>;
  createdAt: string;
}

enum RelationType {
  // Evidence relationships
  SUPPORTS = "supports",           // Evidence supports another claim
  CONTRADICTS = "contradicts",     // Evidence contradicts another claim
  CORROBORATES = "corroborates",   // Evidence confirms another piece
  
  // Geometric relationships
  GEOMETRIC_ABOVE = "geometric_above",      // Higher in tetrahedral structure
  GEOMETRIC_BELOW = "geometric_below",      // Lower in tetrahedral structure
  GEOMETRIC_ADJACENT = "geometric_adjacent", // Same level, different vertex
  
  // Temporal relationships
  PRECEDES = "precedes",           // Happened before
  FOLLOWS = "follows",             // Happened after
  CONCURRENT = "concurrent",       // Happened at same time
  CAUSALLY_LINKED = "causally_linked",  // One caused the other
  
  // Semantic relationships
  SEMANTIC_SIMILAR = "semantic_similar",    // Similar theme/topic
  SEMANTIC_CLUSTER = "semantic_cluster",    // Part of same cluster
  SEMANTIC_OPPOSITION = "semantic_opposition", // Opposing themes
  
  // Narrative relationships
  NARRATES = "narrates",           // Narrative includes this evidence
  ILLUSTRATES = "illustrates",     // Media illustrates this evidence
  PROVES = "proves",               // Evidence proves this claim
  
  // Entity relationships
  ENTITY_CONTROLLED_BY = "entity_controlled_by",
  ENTITY_OWNS = "entity_owns",
  ENTITY_TRANSACTED_WITH = "entity_transacted_with",
  ENTITY_COLLUDED_WITH = "entity_colluded_with"
}
```

---

## 3. API Integration Pattern

### 3.1 Business Intelligence Endpoints (For Vercel Frontend)

#### GET /api/v2/business/intelligence

Fetch business intelligence for professional presentation.

**Request:**
```typescript
interface BusinessIntelligenceRequest {
  limit?: number;                  // Default: 100
  category?: "HERITAGE" | "INNOVATION" | "TRANSPARENCY" | "INTEGRITY" | "CAPABILITY";
  offset?: number;                 // For pagination
}
```

**Response:**
```typescript
interface BusinessIntelligenceResponse {
  status: "success" | "error";
  data: BusinessIntel[];
  metadata: {
    totalItems: number;
    validation: string;
    credibilityFoundation: string;
    generatedAt: string;
  };
}
```

**Frontend Usage:**
```typescript
// Fetch and display business intelligence
const response = await fetch('/api/v2/business/intelligence?limit=50&category=HERITAGE');
const { data, metadata } = await response.json();

// Render credibility markers
data.forEach(intel => {
  displayBusinessCard(intel.title, intel.businessRelevance.clientMessage, intel.clientConfidence.transparencyScore);
});
```

---

#### GET /api/v2/business/timeline

Fetch business history timeline for visual presentation.

**Response:**
```typescript
interface TimelineResponse {
  status: "success";
  timeline: Record<string, TimelineEvent>;
  validation: string;
}

interface TimelineEvent {
  event: string;
  type: "foundation" | "operations" | "modernization" | "innovation" | "renaissance";
}
```

**Frontend Usage:**
```typescript
// Render interactive timeline
const { timeline } = await fetch('/api/v2/business/timeline').then(r => r.json());
renderTimeline(timeline, {
  startYear: 1954,
  endYear: 2025,
  highlightEvents: ["foundation", "innovation", "renaissance"]
});
```

---

#### GET /api/v2/business/credibility

Fetch professional credibility markers for client confidence.

**Response:**
```typescript
interface CredibilityResponse {
  status: "success";
  credibilityMarkers: {
    heritage: string;
    validation: string;
    transparency: string;
    innovation: string;
    integrity: string;
    professional: string;
  };
  confidenceScore: number;         // 0.0-1.0
}
```

**Frontend Usage:**
```typescript
// Display credibility dashboard
const { credibilityMarkers, confidenceScore } = await fetchCredibility();
renderCredibilityBadges(credibilityMarkers);
displayConfidenceScore(confidenceScore);  // Visual gauge: 95%
```

---

### 3.2 Legal Evidence Endpoints (For Court/Prosecution)

#### GET /api/v2/legal/evidence

Fetch legal evidence for court proceedings.

**Request:**
```typescript
interface LegalEvidenceRequest {
  caseType: "fvio" | "conspiracy" | "all";
  priority?: "high" | "medium" | "low";
  limit?: number;
}
```

**Response:**
```typescript
interface LegalEvidenceResponse {
  status: "success";
  evidenceItems: LegalIntel[];
  metadata: {
    totalItems: number;
    caseType: string;
    admissibility: "High" | "Medium" | "Low";
    chainOfCustody: string;
    courtReady: boolean;
    generatedAt: string;
  };
}
```

---

#### GET /api/v2/legal/conspiracy-pattern

Fetch geometric pattern analysis showing 23-year conspiracy.

**Response:**
```typescript
interface ConspiracyPatternResponse {
  status: "success";
  pattern: {
    geometricStructure: string;
    apex: string;
    baseVertices: string[];
    controlPoint: string;
    enforcementArm: string;
    closingMechanism: string;
    temporalSpan: string;
    phases: Array<{
      phase: number;
      years: string;
      name: string;
    }>;
  };
  evidenceItems: number;
  geometricProof: string;
}
```

**Frontend Usage:**
```typescript
// Render 3D pyramid visualization
const { pattern } = await fetchConspiracyPattern();
render3DPyramid({
  apex: pattern.apex,
  base: pattern.baseVertices,
  controlPoint: pattern.controlPoint,
  phases: pattern.phases
});
```

---

#### GET /api/v2/legal/fvio-defense

Fetch complete FVIO defense package for October 30th hearing.

**Response:**
```typescript
interface FVIODefenseResponse {
  status: "success";
  defensePackage: {
    caseOverview: {
      hearingDate: string;
      matters: number;
      adamRichApplication: string;
      policeApplication: string;
    };
    keyArguments: {
      adamRichFvio: string[];
      policeApplication: string[];
    };
    evidenceStrength: string;
    successProbability: number;
  };
}
```

---

### 3.3 AI Narrative Engine Endpoints

#### POST /api/v2/narrative/generate

Generate AI-driven narrative attuned to audience and desired outcome.

**Request:**
```typescript
interface NarrativeGenerationRequest {
  audience: Audience;
  purpose: Purpose;
  entities: string[];              // Entity IDs to include
  timeRange?: {
    start: string;                 // ISO 8601 or year
    end: string;
  };
  mediaTypes: ("text" | "timeline" | "diagram" | "image")[];
  tone: "professional" | "legal" | "technical" | "compassionate" | "authoritative";
}
```

**Response:**
```typescript
// Returns Narrative interface (see section 1.4)
```

**Frontend Usage:**
```typescript
// Generate and display narrative
const narrative = await fetch('/api/v2/narrative/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    audience: 'business_client',
    purpose: 'credibility',
    entities: ['BERJAK_METALS', 'JACQUES_RICH'],
    mediaTypes: ['text', 'timeline'],
    tone: 'professional'
  })
}).then(r => r.json());

// Render narrative with media
renderNarrativeView({
  title: "Our Story",
  text: narrative.narrativeText,
  timeline: narrative.mediaElements.timeline,
  confidenceScore: narrative.successProbability
});
```

---

## 4. Frontend Implementation Patterns

### 4.1 Business Intelligence Dashboard

**Purpose:** Professional, client-facing view emphasizing heritage, credibility, and innovation.

**Components:**
- **Hero Section:** "71 Years of Trading Excellence" with credibility score gauge
- **Timeline Visualization:** Interactive 1954-2025 journey
- **Trust Markers Grid:** Geometric validation, transparency, integrity badges
- **Capability Showcase:** F.R.E. system, modern technology, professional foundation

**Data Flow:**
```
User visits homepage
  → Fetch /api/v2/business/intelligence
  → Fetch /api/v2/business/credibility
  → Fetch /api/v2/business/timeline
  → Render dashboard with geometric animations
```

### 4.2 Legal Evidence Portal (Private/Secured)

**Purpose:** Court-ready evidence management and presentation.

**Components:**
- **Evidence Library:** Searchable, filterable evidence items
- **Conspiracy Pattern Visualization:** 3D tetrahedral pyramid
- **FVIO Defense Package:** October 30th hearing preparation
- **Chain of Custody Tracker:** SHA-256 integrity verification

**Data Flow:**
```
Authorized user logs in
  → Fetch /api/v2/legal/evidence?caseType=all
  → Fetch /api/v2/legal/conspiracy-pattern
  → Fetch /api/v2/legal/fvio-defense
  → Render secure portal with PDF export capability
```

### 4.3 AI Narrative Studio

**Purpose:** Generate custom narratives for different audiences.

**Components:**
- **Audience Selector:** Choose target (client, court, investor, etc.)
- **Purpose Selector:** Choose intent (credibility, prosecution, investment, etc.)
- **Entity Picker:** Select which entities/evidence to include
- **Media Options:** Timeline, diagrams, documents
- **Live Preview:** See narrative generation in real-time
- **Success Forecasting:** Predicted effectiveness gauge

**Data Flow:**
```
User configures narrative parameters
  → POST /api/v2/narrative/generate with parameters
  → Receive narrative with success probability
  → Render with media elements
  → Allow export (PDF, Word, presentation)
```

---

## 5. Visual Design Principles

### 5.1 Geometric Validation Indicators

All evidence items should display their geometric validation visually:

- **Tetrahedral Icon:** Show which vertex the evidence originates from
- **Frequency Color:** Use color mapping for Solfeggio frequencies
  - 396 Hz (Root/Red): Foundation, structure
  - 417 Hz (Sacral/Orange): Change, transformation
  - 528 Hz (Solar/Yellow-Green): Truth, DNA repair
  - 639 Hz (Heart/Green): Relationships, trust
  - 741 Hz (Throat/Blue): Communication, transparency
  - 852 Hz (Third Eye/Indigo): Vision, intuition
- **Validation Score:** Visual gauge (0-100%)

### 5.2 Credibility Markers

Business intelligence should emphasize trust:

- **Heritage Badge:** "Est. 1954 - 71 Years"
- **Validation Seal:** "Geometrically Validated"
- **Transparency Badge:** "43,947 Evidence Items"
- **Integrity Marker:** "Zero Tolerance for Fraud"

### 5.3 Legal Strength Indicators

Legal evidence should show court admissibility:

- **Admissibility Rating:** HIGH / MEDIUM / LOW with color coding
- **Chain of Custody:** Verified checkmark with hover detail
- **SHA-256 Hash:** Display truncated hash with copy button
- **Court Exhibit:** If assigned, show exhibit number prominently

---

## 6. Data Relationships & Graph Visualization

### 6.1 Entity Relationship Graph

The frontend should be capable of rendering interactive entity relationship graphs:

**Nodes:**
- Evidence items (BusinessIntel, LegalIntel)
- Corporate entities (CENTOSA SA, PASCALI TRUST, etc.)
- Individuals (Jacques Rich, Adam Rich, etc.)
- Events (September 20 visit, October 30 hearing, etc.)

**Edges:**
- Relationship types (see section 2)
- Visual encoding:
  - **SUPPORTS:** Green solid line
  - **CONTRADICTS:** Red dashed line
  - **GEOMETRIC_ADJACENT:** Blue dotted line
  - **CAUSALLY_LINKED:** Orange arrow
  - **ENTITY_CONTROLLED_BY:** Black bold arrow

### 6.2 Temporal Flow Visualization

Timeline view showing evidence chronologically:

- **Horizontal axis:** Time (1954-2025)
- **Vertical axis:** Impact/significance
- **Clusters:** Group evidence by TemporalPhase
- **Interactive:** Click event to see full evidence detail
- **Filtering:** By case type, entity, semantic cluster

---

## 7. Authentication & Authorization

### 7.1 Public Access (Business Intelligence)

- `/api/v2/business/*` endpoints are publicly accessible
- No authentication required
- Rate limited: 100 requests/minute per IP

### 7.2 Restricted Access (Legal Evidence)

- `/api/v2/legal/*` endpoints require authentication
- JWT token-based authentication
- Role-based access:
  - **OWNER:** Full access (Jeremy Rich)
  - **LEGAL_TEAM:** Read access to legal evidence
  - **FAMILY:** Limited access to specific items
- Rate limited: 1000 requests/minute for authenticated users

### 7.3 Narrative Generation

- `/api/v2/narrative/*` endpoints require authentication
- Usage quota: 100 narratives/day for OWNER
- Narrative history logged for audit trail

---

## 8. Technical Implementation Notes

### 8.1 State Management

Recommended: **React Context + TanStack Query**

```typescript
// Evidence Context
const EvidenceContext = createContext<{
  businessIntel: BusinessIntel[];
  legalIntel: LegalIntel[];
  narratives: Narrative[];
  loading: boolean;
}>();

// API Hooks
const useBusinessIntelligence = (limit: number) => {
  return useQuery(['business-intel', limit], () => 
    fetch(`/api/v2/business/intelligence?limit=${limit}`).then(r => r.json())
  );
};
```

### 8.2 Real-time Updates

If evidence is updated, the frontend should reflect changes:

- **WebSocket connection** for real-time evidence updates
- **Optimistic UI updates** when submitting new evidence
- **Background sync** for offline capability

### 8.3 Performance Optimization

- **Lazy loading:** Load evidence items on scroll
- **Caching:** TanStack Query handles cache invalidation
- **Code splitting:** Separate bundles for business vs legal portals
- **Image optimization:** Use Next.js Image component for media

---

## 9. Export & Integration Capabilities

### 9.1 Export Formats

Users should be able to export:

- **PDF:** Court-ready evidence compilation
- **Excel:** Evidence spreadsheet with metadata
- **JSON:** Raw data for external processing
- **Word:** Narrative documents with formatting

### 9.2 External Integrations

- **Google Drive:** Backup evidence to Drive
- **Notion:** Sync evidence to Notion workspace
- **Email:** Send narrative summaries via email

---

## 10. Testing & Validation

### 10.1 Automated Testing

- **Unit tests:** All API response interfaces
- **Integration tests:** Full user flows (dashboard load, narrative generation)
- **E2E tests:** Cypress for critical paths

### 10.2 Geometric Validation Testing

Every evidence item must pass geometric validation:

- **Coordinate check:** Is it positioned in valid tetrahedral structure?
- **Frequency check:** Does it resonate at valid Solfeggio frequency?
- **Relationship check:** Are relationships logically consistent?

---

## Conclusion

This ontology provides the complete foundation for building the Vercel frontend that seamlessly integrates with the DOJO Unified Intelligence backend. The system serves dual purposes—professional business credibility and rigorous legal evidence management—while maintaining geometric truth validation throughout.

The AI narrative engine ensures every story told is precisely attuned to its audience and outcome, maximizing effectiveness through geometric, semantic, and temporal coherence.

**Next Steps for dev0.app:**
1. Review this ontology specification
2. Confirm TypeScript interface alignment
3. Design UI/UX mockups based on section 5 (Visual Design Principles)
4. Begin implementation with Business Intelligence Dashboard (section 4.1)
5. Integrate AI Narrative Studio for storytelling capability (section 4.3)

**Contact for API Support:**  
Jeremy Rich  
FIELD Architect  
DOJO Integration Team
