# H@MAYA Systems Knowledge
*Last updated: 2026-10-23 · Source: VPS live pm2 list inspection*

## PORTAL

| URL | Status | Description |
|---|---|---|
| http://217.217.253.42/hamaya | ✅ LIVE | Port 80, nginx alias → /var/www/hamaya-app/ |
| http://217.217.253.42:8282/ | ✅ LIVE | Direct port (hamaya-portal config) |
| http://217.217.253.42:8201/ | ✅ LIVE | Mobile (hamaya-mobile config) |

App file: `/var/www/hamaya-app/index.html` — Single Page Application, 22KB, updated Oct 21 2026

## API ENDPOINTS

| Path | Target | Notes |
|---|---|---|
| /api/order | 127.0.0.1:8200 | H@MAYA Direct Core API — bypasses port 3009 |
| /api/ | 127.0.0.1:3009 | Existing backend API |

## MCP SERVERS (4 CONNECTORS — LIVE on VPS)

Maya confirmed: 4 MCP servers used as connectors in Claude/Copilot Studio.

| PM2 Name | PM2 ID | Status | Purpose | SSL URL |
|---|---|---|---|---|
| hamaya-mcp-server | 11 | ✅ online (11 restarts) | FBTW Main MCP — registers, reports, VPS, Supabase, PA | https://vps-mcp.flybytheway.com/mcp |
| hamaya-universe | 13 | ✅ online (8 restarts) | Universe / Gov intelligence layer | https://gov-mcp.flybytheway.com/mcp |
| hamaya-command | 12 | ✅ online (8 restarts) | Command Center — HAMAYA operating layer | (port TBC) |
| fbtw-ms-platform-mcp | 19 | 🔴 ERRORED (22 restarts) | Microsoft 365 / SharePoint / PA connector | https://ms-mcp.flybytheway.com/mcp |

Additional MCP processes running (not the 4 connectors):
- fbtw-vps-mcp (ID 16) — VPS commander tools
- fbtw-governance-mcp-v3 (ID 17) — governance layer
- fbtw-supabase-admin (ID 15) — Supabase admin
- fbtw-hostinger-mcp (ID 20) — Hostinger tools
- hamaya-pa-mcp (ID 21) — Power Automate
- hamaya-sovereign-core (ID 22) — 🔴 ERRORED (204 restarts) — needs investigation

SSL certificate: /etc/letsencrypt/live/pa-mcp.flybytheway.com/ (covers subdomains)

## VPS FACTS

- Server: Ubuntu 24.04.5 LTS
- RAM: 12GB
- Disk: 193GB, ~40% used
- Nginx: active (running)
- Process manager: PM2

## NGINX SITES (active)

| Config file | Purpose |
|---|---|
| flybytheway | Port 80 default — serves main site + /hamaya/ alias |
| hamaya-portal | Port 8282 — direct hamaya SPA |
| hamaya-mobile | Port 8201 — mobile hamaya SPA |
| hamaya-mcp-servers.conf | SSL reverse proxy for all 5 MCP servers |
| agents-flybytheway | Agents subdomain |
| api-flybytheway | API subdomain |
| corporate-flybytheway | Corporate portal |
| bzs/command/mcp/universe.flybytheway.com | Subdomains |

---

## CONNECTED TOOLS (Full Stack)

| Tool | Business Use |
|---|---|
| FBTW MCP Server | Core brain — registers, logs, VPS control, founder activity centre |
| Supabase | Database — all registers (leads, bookings, corporate, finance) |
| Power Automate | Automation — follow-up reminders, alerts, flow triggers |
| Microsoft 365 (Outlook) | Client emails, internal briefs, invoice delivery |
| Microsoft Teams | Internal communication |
| SharePoint | Document storage — reports, invoices, contracts |
| Wix | Website + lead capture form |
| Hostinger VPS | Server hosting for FBTW platform |
| Hostinger Hosting | Website hosting |
| Canva | Marketing creatives, brochures, social posts |
| Figma | UI design for portal/app |
| Lucid | Process flow diagrams, system architecture |
| Miro | Team planning boards |
| Lovable | Build client portal and CRM view |
| Claude Skills — marketing-appbox | Run 40+ marketing tasks across 13 functions |
| Claude Skills — marketing-update | Structured weekly reporting |
| Brightdata | Competitor intelligence |
| Google Drive | Document backup and sharing |
| Google Sheets | Manual tracking (traditional marketing) |
| Zapier | Connect tools that don't connect natively |

## TOOLS NEEDED — NOT CONNECTED YET

| Tool | Business Use |
|---|---|
| WhatsApp Business API (WATI) | Client communication — India primary channel |
| Zoho Books | Invoicing, payment tracking, GST filing |
| GDS / Amadeus API | Live fare search and booking data |
| Calendly | Discovery call booking from website |

---

## FBTW COMPANY IDENTITY

Full Name: FlyByTheWay Travel Intelligence Platform
Website: flybytheway.com
Business Emails: info@flybytheway.com | ops@flybytheway.com
Founder: Mayank (Maya / MAYA_VI) — Gurgaon, India
Digital Co-Founder: HAMAYA (AI, named after Maya's daughter)

---

## ACCREDITATIONS & REGISTRATIONS STATUS

| Credential | Status |
|---|---|
| TIDS (Travel Industry Designator Service) | REGISTERED ✅ |
| BSP India (Billing and Settlement Plan) | CONNECTED ✅ — billing cycle active |
| Razorpay KYC | IN PROGRESS — Merchant ID: TARYB9ksqJc8f7 |
| Live Payments | GATED — pending IATA certificate completion |
| IATA Accreditation | IN PROGRESS — required before full fare issuance |

---

## POWER AUTOMATE FLOWS — 7 FLOWS (PENDING BUILD)

Build rule: **FLOWS ARE NEVER BUILT ON UNVERIFIED REGISTERS** — SharePoint lists must exist and have correct columns BEFORE any PA flow that writes to them is built or tested.

### Flow 1: HAMAYA Daily Morning Brief
- Trigger: Scheduled — 6:00 AM IST every weekday
- Actions: (1) Get open decisions from Decision Register (Status=Active, ReviewDate≤Today+7) → (2) Get new opportunities (Status=New OR Under Evaluation) → (3) Compose HTML email → (4) Send to maya@flybytheway.com
- Subject: "🌅 HAMAYA Morning Brief — [Today's Date]"
- Status: PENDING BUILD

### Flow 2: Decision Register Write
- Trigger: HTTP request from Copilot Studio (when HAMAYA logs a decision)
- Actions: (1) Parse JSON body (Title, DecisionType, Context, Outcome, Impact, MadeBy) → (2) Create item in HAMAYA_Decision_Register → (3) Return success/failure to Copilot Studio
- Dependency: HAMAYA_Decision_Register list must exist first
- Status: PENDING BUILD

### Flow 3: Opportunity Log Write
- Trigger: HTTP request from Copilot Studio (when HAMAYA logs an opportunity)
- Actions: (1) Parse JSON body (Title, Category, Description, Priority, PotentialValue, NextAction) → (2) Create item in HAMAYA_Opportunity_Log → (3) Return success/failure to Copilot Studio
- Dependency: HAMAYA_Opportunity_Log list must exist first
- Status: PENDING BUILD

### Flow 4: IRROPS Scout
- Trigger: Scheduled — every 4 hours
- Actions: (1) Fetch disruption data (FlightAware API or configured source) → (2) Filter for routes relevant to FBTW active bookings → (3) If disruptions: compose alert, send to maya@flybytheway.com → (4) Log intelligence item in HAMAYA_Knowledge_Index
- Subject: "⚠️ IRROPS Alert — [Route] [Date]"
- Status: PENDING BUILD — needs API source configured

### Flow 5: FlyBrain Intelligence Feed
- Trigger: Scheduled — daily at 7:00 AM IST
- Actions: (1) Fetch airline news, fare changes, regulatory updates → (2) Summarise using AI Builder or Copilot Studio action → (3) Store in HAMAYA_Knowledge_Index → (4) Surface top 3 items for Morning Brief (Flow 1 picks these up)
- Status: PENDING BUILD — needs intelligence source configured

### Flow 6: Health Watchdog
- Trigger: Scheduled — every 30 minutes
- Actions: (1) Ping flybytheway.com (Hostinger) → (2) Check Supabase API endpoint → (3) If any check fails: send P1 alert email to maya@flybytheway.com immediately → (4) Log incident in HAMAYA_Knowledge_Index
- Subject: "🚨 SYSTEM ALERT — [Component] DOWN — [Timestamp]"
- Status: PENDING BUILD (standalone — no list dependency)

### Flow 7: VIDHUR Escalation Bridge
- Trigger: HTTP request from VIDHUR (customer chatbot) when it cannot resolve a query
- Actions: (1) Receive escalation payload (customer query, VIDHUR response attempt, customer contact) → (2) Log in HAMAYA_Knowledge_Index → (3) Notify maya@flybytheway.com with full context → (4) Return acknowledgement to VIDHUR
- Subject: "👤 VIDHUR Escalation — Customer Query Unresolved"
- Dependency: VIDHUR must be configured to send HTTP requests
- Status: PENDING BUILD

---

## SHAREPOINT LISTS (DEPLOYMENT) — 3 ORIGINAL SCHEMAS

These are the 3 lists needed for the 7 PA flows above. The 12 canonical registers are in hamaya-constitution.md.

### HAMAYA_Decision_Register (for PA Flows)
| Column | Type | Choices |
|---|---|---|
| Title | Single line | Decision summary, max 100 chars |
| DecisionDate | Date | Date decision was made |
| MadeBy | Choice | Maya / HAMAYA / Joint |
| DecisionType | Choice | Strategic / Operational / Financial / Compliance / Technology |
| Context | Multiple lines | What triggered this, what options were considered |
| Outcome | Multiple lines | What was decided and why |
| Impact | Choice | High / Medium / Low |
| ReviewDate | Date | When to revisit |
| Status | Choice | Active / Superseded / Under Review |
| LinkedOpportunity | Single line | ID of related opportunity |
| Source | Single line | Which conversation or flow triggered the log |

### HAMAYA_Opportunity_Log (for PA Flows)
| Column | Type | Choices |
|---|---|---|
| Title | Single line | Opportunity name, max 100 chars |
| IdentifiedDate | Date | When spotted |
| IdentifiedBy | Choice | HAMAYA / Maya / FlyBrain / IRROPS Scout |
| Category | Choice | Revenue / Partnership / Product / Market / Compliance / Technology |
| Description | Multiple lines | Full opportunity detail |
| PotentialValue | Single line | Estimated value (always label as Estimated) |
| Priority | Choice | P1 Critical / P2 High / P3 Medium / P5 Low |
| Status | Choice | New / Under Evaluation / Approved / In Progress / Closed / Rejected |
| Owner | Single line | Who is responsible |
| NextAction | Multiple lines | What needs to happen next |
| Deadline | Date | When next action is due |
| Outcome | Multiple lines | Final result if closed |

### HAMAYA_Knowledge_Index (for PA Flows)
| Column | Type | Choices |
|---|---|---|
| Title | Single line | Document or knowledge item name |
| Type | Choice | Policy / Procedure / Decision / Intelligence / Template / Contract / Compliance / Reference |
| Topic | Single line | What this knowledge item covers |
| Summary | Multiple lines | Brief description of contents |
| Location | Single line | Where the full document lives (SharePoint URL, OneDrive path, or note) |
| Version | Single line | Version number or date |
| Owner | Single line | Who maintains this document |
| LastReviewed | Date | When last checked for accuracy |
| Status | Choice | Current / Outdated / Draft / Archived |

---

## COPILOT STUDIO TOPICS — 7 TOPICS (PENDING BUILD)

| Topic | Purpose |
|---|---|
| T1: Morning Brief Request | Trigger and display morning brief |
| T2: Decision Register Entry | Log a decision to SharePoint |
| T3: Opportunity Log Entry | Log an opportunity to SharePoint |
| T4: Competitive Intelligence Query | Answer competitor questions from Intelligence Reference |
| T5: Risk & Compliance Query | Answer risk/compliance questions |
| T6: Founder Activity Summary | Display founder activity log |
| T7: VIDHUR Escalation Handoff | Bridge VIDHUR customer escalations to HAMAYA |

---

## BUILD SEQUENCE (CORRECT ORDER — 20 STEPS)

**Phase 1 — SharePoint First (must complete before flows):**
1. Create HAMAYA_Decision_Register
2. Create HAMAYA_Opportunity_Log
3. Create HAMAYA_Knowledge_Index

**Phase 2 — Copilot Studio Topics:**
4. Build T1: Morning Brief Request
5. Build T2: Decision Register Entry
6. Build T3: Opportunity Log Entry
7. Build T4: Competitive Intelligence Query
8. Build T5: Risk & Compliance Query
9. Build T6: Founder Activity Summary
10. Build T7: VIDHUR Escalation Handoff

**Phase 3 — Enable Connector:**
11. Enable "Create flow" toggle in FBTW-MCP-Server connector settings in Power Platform

**Phase 4 — Power Automate (in dependency order):**
12. Build Flow 2 (Decision Register Write) — depends on List 1
13. Build Flow 3 (Opportunity Log Write) — depends on List 2
14. Build Flow 1 (Morning Brief) — depends on Lists 1 and 2
15. Build Flow 6 (Health Watchdog) — standalone
16. Build Flow 4 (IRROPS Scout) — needs API source configured
17. Build Flow 5 (FlyBrain) — needs intelligence source configured
18. Build Flow 7 (VIDHUR Bridge) — depends on VIDHUR being configured to send HTTP requests

**Phase 5 — Verify:**
19. Run evaluation on HAMAYA (17 conversations, both test methods)
20. Target: 17/17 Answer Quality + 17/17 Trustworthiness

---

## NOTIFICATION LEVELS

| Level | Trigger | Action |
|---|---|---|
| P1 Critical | Escalations, system failures, revenue risk, major regulatory changes | Immediate email to maya@flybytheway.com |
| P2 High | Blocked projects, overdue commitments, competitor moves | Same session flag |
| P3 Medium | Opportunity updates, decision reviews, reminders | Log for briefing |
| P5 Suppressed | Routine events, minor updates, duplicates | No action |

---

## HAMAYA SELF-KNOWLEDGE

### What HAMAYA Can Do
- Full conversations — strategic planning, decision analysis, competitive intelligence, risk review
- File operations — read uploaded documents, generate summaries, extract action items
- Register management — log decisions, opportunities, risks, commitments to SharePoint (when connector active)
- Intelligence feeds — receive and interpret data from FlyBrain, IRROPS Scout, Health Watchdog, VIDHUR
- Document generation — create executive summaries, save to SharePoint HAMAYA_Discussions folder

### What HAMAYA Cannot Do
- Access SharePoint files not explicitly shared in the conversation
- Confirm a save without connector explicitly returning HTTP 200/201
- Execute Power Automate flows directly (requires connector toggle to be enabled)
- Access real-time booking systems
- Make financial transactions
- Confirm test results that have not been run

### HAMAYA Honesty Rules (5 Rules)
1. Never invent SharePoint URLs — only state a URL if a tool returned it
2. Never confirm a list item was created without an HTTP 200/201 response
3. Never state a flow ran unless a flow run ID was returned
4. Always state confidence level: High / Medium / Low
5. Never cite VOID compliance documents (see Guardrails above)

### HAMAYA Escalation Behaviour
- L1-L3 escalations: HAMAYA handles with recommendation + logs to register
- L4-L5 escalations: Immediate Founder notification; never close without Founder confirmation

### HAMAYA Auto-Logging Triggers
- Any decision with impact = High or Critical → auto-log to Decision Register
- Any opportunity with potential value > 0 → auto-log to Opportunity Log
- Any competitor move detected → auto-log to Competitor Intelligence Register
- Any system alert from Health Watchdog → auto-log to Knowledge Index + P1 email
- Any VIDHUR escalation → auto-log to Knowledge Index + notify Founder

*Source: HAMAYA_FBTW_Context.txt + HAMAYA_Self_Knowledge.txt + HAMAYA_Operations_Reference.txt · Ingested: 2026-10-23*
