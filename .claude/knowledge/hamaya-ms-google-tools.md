# FBTW — Business Tool Index
> Source: FlyByTheWay Complete Business Core · October 23, 2026
> What is built, what is live, what is missing.

---

## TOOLS BUILT & LIVE

| Tool | What It Does |
|---|---|
| **marketing-appbox** | Maps 40+ Claude skills across 13 marketing functions — skill navigation layer |
| **marketing-update** | Structured reporting: 3 sections, max 3 bullets, metrics required, pulls live data first |

---

## WHAT FBTW HAS ✅

| Component | Tool |
|---|---|
| Database | Supabase |
| Automation | Power Automate |
| Communication | Microsoft 365 — Outlook + Teams |
| Cloud infrastructure | Hostinger VPS |
| Design / Creative | Canva + Figma |
| Diagrams / Flows | Lucid + Miro |
| Website | Wix + Hostinger hosting |
| App builder | Lovable |
| Cloud partner | Microsoft Azure |
| Skill layer | marketing-appbox |
| Reporting rules | marketing-update |

---

## WHAT FBTW IS MISSING ❌

| Gap | What's Missing | Best Fix |
|---|---|---|
| Lead capture | No form-to-register pipeline | Wix form → Power Automate → Supabase |
| GDS / Booking data | Manual booking entry only | Amadeus / Sabre API or CSV import flow |
| Accounting | No finance software connected | Zoho Books (API-ready, India GST-friendly) |
| WhatsApp | Client communication missing | WhatsApp Business API via WATI or 360dialog |
| CRM view | No visual pipeline | Lovable lightweight CRM |
| Client portal | No client self-service | Lovable app — booking status + invoice view |

---

## 6 BUSINESS LAYERS

### Layer 1 — Marketing Brain
```
Monday 8AM Auto-trigger
  → Pull metrics (Google Sheets — traditional channels only)
  → Detect drops / wins
  → Create action tasks (FBTW register)
  → Send decision brief (Outlook / Teams)
  → Friday check: tasks done?
  → Log to Supabase
  → Next week starts smarter
```
**Status:** Ready to build. Metrics source: traditional channels tracked in Google Sheets. No digital channel data active yet.

---

### Layer 2 — Sales Core
```
Lead enters (form / email / WhatsApp)
  → Auto-classified (FBTW: classify_notification)
  → Logged to Lead Register (Supabase)
  → Assigned priority + follow-up date
  → Reminder fires (Power Automate)
  → Outcome logged (won / lost / pending)
  → Weekly pipeline report → Outlook
```
**Tools present:** FBTW registers, Supabase, Microsoft 365, Power Automate
**Gap:** ❌ No lead capture form connected. Leads entering manually.

---

### Layer 3 — Operations Core
```
Booking request received
  → Logged to Operations Register
  → Status tracked (pending / confirmed / ticketed / closed)
  → Client communication sent (Outlook / Teams)
  → Escalation triggered if SLA breached
  → Daily ops summary → Founder Activity Centre
```
**Tools present:** FBTW MCP (log_escalation, get_founder_activity_centre), Microsoft 365
**Gap:** ❌ No GDS / booking API connected. Manual entry risk.

---

### Layer 4 — Finance Core
```
Invoice created
  → Logged to Finance Register (Supabase)
  → Payment due date tracked
  → Auto-reminder sent if unpaid (Power Automate)
  → Monthly close report generated
  → PDF exported (FBTW: generate_and_stream_pdf)
  → Stored in SharePoint
```
**Tools present:** FBTW PDF generator, SharePoint, Supabase, Power Automate
**Gap:** ❌ No accounting software connected. Zoho Books recommended.

---

### Layer 5 — Intelligence Core
```
Competitor activity detected
  → Logged (log_intelligence)
  → Market opportunity spotted
  → Logged (log_opportunity)
  → Weekly intelligence brief compiled
  → Feeds into Monday Marketing Brain
  → Informs decisions
```
**Tools present:** FBTW intelligence logs, Supabase, Bright Data plugin
**Status:** Ready to build.

---

### Layer 6 — Founder Control Centre
```
Single daily view →
  Marketing status
  Sales pipeline
  Operations pending
  Finance outstanding
  Intelligence alerts
  VPS / system health (Hostinger VPS)
→ All in one brief → 9AM every day → Outlook
```
**Tools present:** FBTW get_founder_activity_centre, hostinger_vps_metrics, all registers
**Status:** Ready to build.

---

## MARKETING — TRADITIONAL CHANNELS (Active, All Manual)

No digital marketing running. All activity tracked in Google Sheets.

| Channel | What to track |
|---|---|
| **Print Collateral** (brochures, flyers, standees, banners) | Vendor · proof status · cost · distribution count |
| **Outdoor & Signage** | Location · duration · cost · enquiries attributed |
| **Events & Roadshows** | Date · venue · cost · leads · meetings booked |
| **Trade Shows** | Booth cost · footfall · cards collected · pipeline |
| **Corporate Client Visits** | Accounts visited · contacts met · outcome · next step |
| **Agent Outreach** | Agents contacted · activated · bookings attributed |
| **Direct Mail** | Sent · response rate · cost per response |
| **WhatsApp Broadcast** | Sent · delivered · read · replied · converted |
| **PR & Media Coverage** | Coverage count · publication · reach · cost |
| **Sponsorships** | Property · cost · impressions · leads |
| **Partner & Co-marketing** | Partner · offer · leads · revenue attributed |
| **SMS Campaigns** | Sent · delivered · clicked · converted |

**Tracking sheet columns:**
```
Item | Type | Vendor | Cost (INR) | Date | Status | Result | Owner
```

---

## BUILD ORDER

| Week | Task | Priority |
|---|---|---|
| Week 1 | Founder Control Centre — daily 9AM brief | IMMEDIATE |
| Week 2 | Sales Core — lead register + pipeline | HIGH |
| Week 3 | Marketing Brain — closed loop automation | HIGH |
| Week 4 | Operations Core — booking tracking | HIGH |
| Week 5 | Finance Core — invoice + payment reminders | MEDIUM |
| Week 6 | Intelligence Core — competitor + opportunity logs | MEDIUM |
| Week 7 | Wix form + Zoho Books + WhatsApp API | HIGH |
| Week 8 | Client portal via Lovable | MEDIUM |

---

*Review: Monthly or when a new system is added.*
