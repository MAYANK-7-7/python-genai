---
name: marketing-appbox
description: One-stop marketing toolbox. Maps every marketing function (digital, traditional, analytics, ops) to the connectors, apps and skills available, with connection status and the manual fallback. Use when the user asks which tool to use for a marketing task, wants to pull marketing data from any source, or needs inputs for the marketing-update skill.
---

# Marketing Appbox

Single index of marketing tools. For any marketing task: find the function below, use the first connected tool, fall back to the manual input if none is connected.

Status column reflects the session where this was written (2026-10-23). Connector status changes: confirm a tool is available (ToolSearch) before relying on it, and if it failed to connect, tell the user instead of guessing data.

## Digital marketing

| Function | Connected / usable | Skills to call | Not connected last check |
|---|---|---|---|
| Web analytics (traffic, conversions, funnels) | Google Analytics (search-visibility-kit analytics), Sealmetrics (seal-copilot) | seal-copilot:weekly-health-check, seal-copilot:funnel-analysis, dataslayer-marketing-skills:ds-channel-report | Amplitude, Pendo, Hex |
| SEO and search | Google Search Console (search-visibility-kit gsc) | search-visibility-kit:seo-audit, seo-aeo-geo-ultimate:seo-audit, searchfit-seo:seo-check, marketing:seo-audit | Ahrefs, Similarweb, Supermetrics |
| AI search visibility | none | ai-seo:ai-seo-audit, small-business:seo-ai-visibility | Manifold |
| Paid ads | none live | hyper-marketing:google-ads, meta-ads, tiktok-ads, reddit-ads, pinterest-ads, snapchat-ads, amazon-ads; small-business:ad-manager; dataslayer-marketing-skills:ds-paid-audit; realize-plugin:campaigns | Realize/Taboola, Hyperfx |
| Email marketing | Gmail, Outlook | marketing:email-sequence, hyper-marketing:email-lifecycle, mailercloud:analyze-campaigns | Mailercloud, ActiveCampaign (config missing), Klaviyo |
| Social media | none live | postiz:postiz, small-business:social-content-engine, hyper-marketing:instagram, linkedin, tiktok, youtube, reddit | none |
| Content and copy | Google Docs/Drive, Claude Docs | marketing:content-creation, marketing:draft-content, content-strategy:content-calendar, seo-article-writer-faq:seo-article-writer | none |
| Design and creative | Canva, Figma, Adobe skills, Miro, Lucid | small-business:canva-creator, small-business:brand-style, brand-md:brand, marketing:brand-review | Adobe, Miro plugin (the Miro MCP server is separate) |
| Website and landing pages | Wix, Lovable, Supabase | searchatlas:build-website, searchatlas:launch-website | none |
| Competitor and market intel | Bright Data skills (scrape/search) | marketing:competitive-brief, brightdata-plugin:competitive-intel, manifold-style skills if connected | Nimble, Similarweb |
| Reputation and reviews | none | small-business:review-reputation | none |
| Leads and CRM | Google Sheets as tracker | small-business:lead-finder, crm-autopilot, lead-triage, grow-pipeline | Intercom |
| Automation | Zapier, Power Automate (FBTW-Mcp-PA) | zapier:zapier-explore, zapier:zapier-status | none |

## Traditional marketing

No live connectors exist for these. Track them in one Google Sheet (use Google Sheets tools) with columns: item, type, vendor, cost, date, status, result, owner.

| Function | Tool to use | Manual input needed from user |
|---|---|---|
| Print collateral (brochures, flyers, standees) | Canva or Figma for design, Drive for proofs, Gmail/Outlook for vendor approvals | vendor, proof status, delivery date, cost |
| Outdoor and signage | Sheet tracker, Calendar for install dates | location, duration, cost, enquiries attributed |
| Events, roadshows, trade shows | Calendar, Sheet tracker, Canva for kits | dates, cost, leads captured, meetings booked |
| Corporate and agent outreach (visits, calls) | Sheet tracker, Gmail/Outlook, small-business:outreach-composer | visits done, accounts onboarded |
| Direct mail and WhatsApp broadcast | Sheet tracker | sent, replies, conversions |
| PR and sponsorships | Sheet tracker | coverage count, reach, cost |
| Partner and co-marketing | Sheet tracker | partner, offer, leads |

Attribution tip: give every traditional channel its own phone number, promo code or UTM-tagged QR link so results can be reported with numbers.

## Operations and reporting

| Function | Tool |
|---|---|
| Calendar and deadlines | Google Calendar, Outlook calendar |
| Team comms | Outlook, Teams, Gmail |
| Files and approvals | Google Drive, SharePoint |
| Budget vs spend | Google Sheets |
| Manager update | marketing-update skill (this repo) |
| Weekly rollups | small-business:marketing-monday, small-business:growth-pulse, marketing:performance-report |

## How to use

1. Identify the function. Pick the row.
2. Check the connector is available this session (ToolSearch). If it failed to connect, say so and use the fallback.
3. Pull data, never estimate it. For traditional channels ask the user for the manual inputs.
4. For the manager update, feed results into the marketing-update skill: Wins from results, Blockers from stalled items (vendors, approvals, failed connectors), Priorities from the calendar.

## Maintenance

When the user connects or removes a tool, update the tables above. Keep one row per function, not one per tool.
