# FBTW Marketing — Actual Tool Inventory
> What is actually being used. No digital campaigns running yet. Traditional marketing is the current reality.

---

## TRADITIONAL MARKETING — Active Channels

These are the channels FBTW currently uses. All tracked manually in Google Sheets.

| Channel | What happens | What to track |
|---|---|---|
| **Print Collateral** | Brochures, flyers, standees, banners | Vendor · proof status · delivery date · cost · distribution count |
| **Outdoor & Signage** | Hoardings, airport displays, metro panels | Location · duration · cost · enquiries attributed |
| **Events & Roadshows** | FBTW-hosted or attended travel events | Date · venue · cost · leads · meetings booked |
| **Trade Shows** | Industry exhibitions | Booth cost · footfall · cards collected · demos · pipeline |
| **Corporate Client Visits** | Direct visits to corporate accounts | Accounts visited · contacts met · outcome · next step |
| **Agent Outreach** | Visits/calls to travel agents, B2B partners | Agents contacted · activated · bookings attributed |
| **Direct Mail** | Physical mailers, courier kits to corporates | Sent · response rate · cost per response |
| **WhatsApp Broadcast** | Bulk messages to leads/clients | Sent · delivered · read · replied · converted |
| **PR & Media Coverage** | Press features, editorial mentions | Coverage count · publication · reach · cost |
| **Sponsorships** | Event or property sponsorships | Property · cost · impressions · leads · brand lift |
| **Partner & Co-marketing** | Joint campaigns with airlines, hotels, aggregators | Partner name · offer · leads · revenue attributed |
| **SMS Campaigns** | Outbound SMS to database | Sent · delivered · clicked · converted · opt-outs |

> Attribution tip: Give each channel its own promo code, phone number, or UTM-tagged QR code so results carry a number.

---

## OPERATIONS TOOLS — Available Now

These are connected and in active use for day-to-day work.

| Tool | What it does |
|---|---|
| **Microsoft Teams** | Internal comms, campaign discussions, file sharing |
| **Outlook** | Client emails, corporate correspondence, calendar |
| **SharePoint** | Document library — proofs, contracts, campaign files |
| **Google Sheets** | Budget tracker, lead tracker, traditional channel log |
| **Google Drive** | File storage, sharing with vendors and clients |
| **Google Calendar / Outlook Calendar** | Campaign deadlines, event dates, meeting scheduling |
| **Canva** | Design for print and digital creatives |
| **Power Automate** | Email triggers, approval workflows, SharePoint automations |
| **Manager Update** | Pull Wins / Blockers / Priorities → `marketing-update` skill |

---

## DIGITAL TOOLS — Exist But Not Active Yet

These connectors are available in Claude.ai but FBTW has no active digital marketing running through them.

| Tool | Status | What is needed to activate |
|---|---|---|
| Google Analytics 4 | Connector present | Website needs GA4 tracking code installed |
| Google Search Console | Connector present | Domain needs to be verified in GSC |
| Google Ads | VPS MCP present | Ad account + budget needed to start |
| SEO (Ahrefs / GSC) | GSC connector present, Ahrefs offline | Active website with pages to optimise |
| Email Marketing (ActiveCampaign) | Connector present, URL not set | Configure URL in /plugin settings |
| Social Media (Postiz) | Connector present | Social accounts need to be linked |

---

## TRACKING SHEET STRUCTURE

Use one Google Sheet for all traditional channels. Columns:

```
Item | Type | Vendor/Platform | Cost (INR) | Date | Status | Result | Owner
```

Examples:
- Brochure print run → Print · ABC Printers · ₹18,000 · Oct 2026 · Delivered · 500 distributed · Maya
- Agent visit (Delhi) → Agent Outreach · Direct · ₹0 · Oct 2026 · Done · 3 agents activated · Sales
- WhatsApp broadcast → WhatsApp · Internal · ₹0 · Oct 2026 · Sent 420 · 18 replies · Marketing

---

## FOR MANAGER UPDATE

Pull from the sheet above + ask Maya for manual inputs:

- **Wins** → channels with numbers (leads, activations, coverage, bookings)
- **Blockers** → vendor delays, approval pending, budget issues
- **Priorities** → next activity with owner and date

Skill: `marketing-update` — produces ready-to-paste update in under 30 seconds.
