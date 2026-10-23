# HAMAYA Marketing Toolbox — Complete Tool Index
> All tools across Digital, SEO, Traditional, and Ops. Status per tool. Source per tool.

---

## STATUS KEY
| Symbol | Meaning |
|---|---|
| ✅ Connected | Live connector in Claude.ai session — tools available now |
| 🔶 Partial | Connector present but config incomplete |
| 🔴 Offline | Connector failing (proxy error or auth issue) |
| ✋ Manual | No connector — track by hand in Google Sheets |
| 🔧 VPS MCP | Available via HAMAYA MCP server on VPS |

---

## 1. WEB ANALYTICS

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Google Analytics 4 (GA4)** | ✅ Connected | Traffic, sessions, bounce rate, conversions, funnels, realtime visitors, custom reports by date/device/channel | Search Visibility Kit (Claude.ai) + Google Marketing MCP port 8110 |
| **Sealmetrics** | ✅ Connected | Privacy-first analytics — sessions, pageviews, channel mix, funnel analysis, weekly health check, drop diagnosis | seal-copilot plugin (Claude.ai) |
| **Amplitude** | 🔴 Offline | Product analytics, retention cohorts, user journeys | Plugin proxy error — cannot connect |
| **Pendo** | 🔴 Offline | In-app engagement, NPS, feature adoption | Plugin proxy error — cannot connect |

---

## 2. SEO & SEARCH VISIBILITY

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Google Search Console** | ✅ Connected | Clicks, impressions, CTR, position by page/query; index status; URL inspection; sitemap management; crawl errors | Search Visibility Kit GSC (Claude.ai) + Google Marketing MCP port 8110 |
| **Ahrefs** | 🔴 Offline | Backlink profile, keyword difficulty, site audit, competitor gaps | Plugin proxy error — cannot connect |
| **Similarweb** | 🔴 Offline | Traffic share, referral sources, competitor benchmarks | Plugin proxy error — cannot connect |
| **Supermetrics** | 🔴 Offline | Cross-channel data aggregation | Plugin proxy error — cannot connect |
| **AI Search Visibility** | ✅ Connected | Check brand/page presence in AI-generated answers (ChatGPT, Gemini, Perplexity) | ai-seo plugin (Claude.ai) |

**SEO actions available now:**
- Run full site SEO audit → `search-visibility-kit:seo-audit`
- Fix on-page SEO → `searchfit-seo:on-page-seo`
- Schema markup → `searchfit-seo:schema-markup`
- Technical SEO → `searchfit-seo:technical-seo`
- AI visibility audit → `ai-seo:ai-seo-audit`

---

## 3. PAID ADVERTISING

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Google Ads** | 🔧 VPS MCP | Campaign list, impressions, clicks, cost, conversions by date | Google Marketing MCP port 8110 (`gm_get_ads_campaigns`, `gm_get_ads_performance`) |
| **Meta Ads (Facebook/Instagram)** | ✋ Manual | No live connector — pull reports from Ads Manager manually | Track in Google Sheets |
| **LinkedIn Ads** | ✋ Manual | No live connector — pull from LinkedIn Campaign Manager | Track in Google Sheets |
| **Google Display / YouTube Ads** | ✋ Manual | No live connector | Track in Google Sheets |
| **Realize / Taboola** | 🔴 Offline | Native advertising campaigns | Plugin proxy error |
| **HyperFX** | 🔴 Offline | Multi-channel ad automation | Plugin proxy error |

---

## 4. EMAIL MARKETING

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Gmail** | ✅ Connected | Send, draft, search, read, label, filter, vacation responder, bulk ops | Microsoft 365 Connector (Outlook) + Gmail plugin (needs auth) |
| **Outlook / Exchange** | ✅ Connected | Send, draft, reply, search, batch delete, label, calendar, shared mailboxes | Microsoft 365 Connector (Claude.ai) + MS Marketing MCP port 8111 |
| **ActiveCampaign** | 🔶 Partial | Email sequences, automations, contact lists, campaign reports | Plugin present but URL not configured — open /plugin settings |
| **Mailercloud** | 🔴 Offline | Email campaigns, list management, deliverability | Plugin proxy error — cannot connect |
| **Klaviyo** | 🔴 Offline | E-commerce email flows, segmentation | Plugin proxy error — cannot connect |

**Email actions available now:**
- Draft email sequence → `marketing:email-sequence`
- Analyse campaigns (Mailercloud) → `mailercloud:analyze-campaigns` *(when fixed)*
- ActiveCampaign weekly digest → `activecampaign:weekly-digest` *(when URL set)*

---

## 5. SOCIAL MEDIA

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Postiz** | 🔶 Partial | Schedule and publish posts across platforms | Plugin present but social accounts not linked |
| **Instagram** | ✋ Manual | No live connector for posting/analytics — use Canva for creatives | Postiz (when linked) |
| **LinkedIn** | ✋ Manual | No live connector | Postiz (when linked) |
| **Facebook** | ✋ Manual | No live connector | Postiz (when linked) |
| **YouTube** | ✋ Manual | No live connector | Postiz (when linked) |
| **X / Twitter** | ✋ Manual | No live connector | Postiz (when linked) |

**Social skills available now** *(for strategy and copy — not live posting)*:
- Instagram strategy → `hyper-marketing:instagram`
- LinkedIn strategy → `hyper-marketing:linkedin`
- YouTube strategy → `hyper-marketing:youtube`
- Content calendar → `content-strategy:content-calendar`
- Social content engine → `small-business:social-content-engine`

---

## 6. CONTENT & CREATIVE

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Canva** | ✅ Connected | Design banners, brochures, social posts, presentations, brand templates | Canva MCP (Claude.ai) |
| **Figma** | ✅ Connected | UI/UX design, prototypes, design system components | Figma MCP (Claude.ai) |
| **Google Drive** | ✅ Connected | Store files, share proofs, read Docs, search content | Google Drive connector (Claude.ai) + Google Marketing MCP port 8110 |
| **Google Docs** | ✅ Connected | Read and edit documents (via Drive connector) | Google Drive connector |
| **Miro** | 🔴 Offline | Whiteboards, campaign planning boards | Plugin proxy error |
| **Adobe** | 🔴 Offline | Photoshop, Illustrator, Acrobat, PDF generation | Plugin proxy error |

---

## 7. WEBSITE & LANDING PAGES

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Wix** | ✅ Connected | Build pages, deploy site, manage CMS, SEO settings | Wix MCP (Claude.ai) |
| **Lovable** | ✅ Connected | Build web apps and landing pages with AI | Lovable MCP (Claude.ai) |
| **Supabase** | ✅ Connected | Database for web apps, user auth, edge functions | Supabase MCP (Claude.ai) + HAMAYA Supabase Admin MCP port 8105 |
| **Bright Data** | ✅ Connected | Web scraping, competitor page monitoring, price tracking | Bright Data plugin (Claude.ai) |

---

## 8. MARKET & COMPETITOR INTELLIGENCE

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Bright Data** | ✅ Connected | Scrape competitor sites, monitor brand mentions, extract pricing, build lead lists | Bright Data plugin (Claude.ai) |
| **Nimble** | 🔴 Offline | B2B company and contact intelligence | Plugin proxy error |
| **Manifold** | 🔴 Offline | Competitor teardowns, market mapping, social monitoring | Plugin proxy error |

**Intelligence skills available now:**
- Competitor brief → `marketing:competitive-brief`
- Competitor intel → `brightdata-plugin:competitive-intel`
- SEO competitor gaps → `searchfit-seo:competitor-analyzer`

---

## 9. MARKETING AUTOMATION & CRM

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Zapier** | ✅ Connected | Connect apps, automate workflows, trigger actions across tools | Zapier MCP (Claude.ai) |
| **Power Automate** | ✅ Connected | Microsoft flows — email triggers, SharePoint automations, Teams alerts | FBTW-Mcp-PA (Claude.ai) + MS Tools MCP port 8109 |
| **ActiveCampaign CRM** | 🔶 Partial | Contact tracking, deal pipeline, automations | Plugin present, URL not set |
| **Google Sheets as CRM** | ✅ Connected | Track leads, campaigns, budgets, vendors, results | Google Sheets connector (Claude.ai) + Google Marketing MCP port 8110 |

---

## 10. TRADITIONAL MARKETING — ALL MANUAL TRACK

> No live connectors. Log all activity in a Google Sheet with columns: **item · type · vendor · cost · date · status · result · owner**
> Attribution tip: give each channel its own promo code, phone number, or UTM-tagged QR code.

| Channel | What to track | Where to ask for numbers |
|---|---|---|
| **Print Collateral** (brochures, flyers, standees, banners) | Vendor, proof status, delivery date, cost, distribution count | Print vendor / in-house |
| **Outdoor & Signage** (hoardings, airport displays, metro) | Location, size, duration, cost, attributed enquiries | Outdoor vendor |
| **Events & Roadshows** | Date, venue, cost, leads captured, meetings booked, follow-up rate | Event team |
| **Trade Shows** | Booth cost, footfall, cards collected, demos given, pipeline added | Trade show lead |
| **Corporate Client Visits** | Accounts visited, contacts met, outcome, next step | Sales / ops |
| **Agent Outreach** (travel agents, B2B) | Agents contacted, activated, bookings attributed | Sales team |
| **Direct Mail** (physical mailers, courier kits) | Sent count, response rate, cost per response | Marketing ops |
| **WhatsApp Broadcast** | Sent, delivered, read, replied, converted | WhatsApp Business / operator |
| **PR & Media Coverage** | Coverage count, publication, reach, sentiment, cost | PR agency or in-house |
| **Sponsorships** | Event/property, cost, impressions, leads, brand lift | Sponsorship partner |
| **Partner & Co-marketing** | Partner name, offer, leads generated, revenue attributed | Partner manager |
| **SMS Campaigns** | Sent, delivered, clicked, converted, opt-outs | SMS provider |

---

## 11. OPS & REPORTING

| Tool | Status | What you can do | Source |
|---|---|---|---|
| **Google Calendar** | ✅ Connected | Campaign deadlines, event dates, team meetings, free-busy check | Google Calendar plugin (Claude.ai) |
| **Outlook Calendar** | ✅ Connected | Corporate calendar, meeting invites, availability | Microsoft 365 Connector (Claude.ai) + MS Marketing MCP port 8111 |
| **Microsoft Teams** | ✅ Connected | Channel comms, campaign discussions, file sharing, search | Microsoft 365 Connector + MS Marketing MCP port 8111 |
| **SharePoint** | ✅ Connected | Document library, approval workflows, campaign file store | Microsoft 365 Connector + MS Marketing MCP port 8111 |
| **Google Sheets** | ✅ Connected | Budget vs spend tracker, traditional channel log, lead tracker | Google Sheets connector (Claude.ai) + Google Marketing MCP port 8110 |
| **Manager Update** | ✅ Connected | Auto-pull Wins / Blockers / Priorities from live tools | `marketing-update` skill (this project) |
| **Marketing Toolbox UI** | ✅ Published | Visual command center — status cards, setup guides, activity tracker | claude.ai/artifact/HSFDJGixWSiDjrHip4Uk37 |

---

## 12. HAMAYA VPS MCP SERVERS — MARKETING LAYER

| Server | Port | Tools |
|---|---|---|
| Google Marketing MCP | 8110 | GA4 · GSC · Google Ads · Sheets · Drive (11 tools) |
| Microsoft Marketing MCP | 8111 | Teams · Outlook · SharePoint · Calendar (19 tools) |
| MS Tools MCP | 8109 | Power Automate CRUD + Copilot Studio (28 tools) |
| MS Platform MCP | 8104 | PA list + SharePoint status (2 tools) |

---

## SUMMARY COUNT

| Category | Connected | Partial | Offline | Manual |
|---|---|---|---|---|
| Web Analytics | 2 | 0 | 2 | 0 |
| SEO | 2 | 0 | 3 | 0 |
| Paid Ads | 1 (VPS) | 0 | 2 | 3 |
| Email | 2 | 1 | 2 | 0 |
| Social | 0 | 1 | 0 | 5 |
| Content & Creative | 3 | 0 | 2 | 0 |
| Website | 3 | 0 | 0 | 0 |
| Intelligence | 1 | 0 | 2 | 0 |
| Automation & CRM | 3 | 1 | 0 | 0 |
| Traditional | 0 | 0 | 0 | 12 |
| Ops & Reporting | 6 | 0 | 0 | 0 |

---

⚠️ Write operations on VPS MCP tools require `approval="MAYA APPROVED"`.
🔶 To fix Partial tools: open `/plugin` panel in Claude.ai and complete config.
🔴 To fix Offline tools: check proxy settings — most fail with 403 proxy tunnel error.
