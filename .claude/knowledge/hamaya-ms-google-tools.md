# HAMAYA — Microsoft & Google Tool Index
> Every tool gained per connector, MCP server, or artifact. One source of truth.

---

## MICROSOFT

### 1. Microsoft 365 Connector — Claude.ai (`mcp__Microsoft_365__*`)
~40 tools across five surfaces:

| Surface | Tools |
|---|---|
| **Outlook Email** | email_search, send_mail, create_draft, reply_draft, reply_all_draft, forward_mail, update_draft, delete_draft, batch_delete_messages, batch_modify_labels, modify_labels, modify_thread_labels, create_label, update_label, delete_label, create_filter, delete_filter, set_vacation, trash_thread, untrash_thread |
| **Teams** | list_teams, list_channels, list_channel_messages, list_chats, send_channel_message, reply_channel_message, create_chat, send_chat_message, chat_message_search |
| **SharePoint** | sharepoint_search, sharepoint_folder_search, sharepoint_upload_file, sharepoint_update_file, sharepoint_create_folder, sharepoint_copy_item, sharepoint_move_item, sharepoint_rename_item, sharepoint_delete_item |
| **Calendar** | outlook_calendar_search, create_event, update_event, delete_event, respond_to_event, find_meeting_availability, outlook_find_available_time |
| **People / Me** | get_me, search_people, get_granted_scopes, read_resource |

---

### 2. Microsoft Marketing MCP — VPS port 8111
**File:** `/opt/hamaya/microsoft/tools.py`
**Token:** `MS_MKTG_TOKEN` | **Auth:** `az account get-access-token`

| Tool | What it does |
|---|---|
| `mm_list_teams` | All Teams the account belongs to |
| `mm_list_channels` | Channels inside a team |
| `mm_get_channel_messages` | Recent messages from a channel |
| `mm_search_teams_messages` | Full-text search across Teams |
| `mm_list_emails` | Inbox / sent / folder listing |
| `mm_get_email` | Full email content by ID |
| `mm_search_emails` | Keyword search across all Outlook folders |
| `mm_get_email_stats` | Sent / received count for last N days |
| `mm_search_sharepoint` | Search SharePoint docs / pages |
| `mm_list_sharepoint_sites` | All accessible SharePoint sites |
| `mm_get_sharepoint_files` | Files in a site's document library |
| `mm_list_calendar_events` | Calendar events in a date range |
| `mm_get_free_busy` | Availability for one or more users |
| `mm_search_people` | Directory / contacts search |
| `mm_get_my_profile` | Authenticated user's MS profile |
| `mm_send_email` ⚠️ | Send Outlook email — MAYA APPROVED |
| `mm_create_draft_email` ⚠️ | Save draft without sending — MAYA APPROVED |
| `mm_post_teams_message` ⚠️ | Post to Teams channel — MAYA APPROVED |
| `mm_create_calendar_event` ⚠️ | Create calendar event — MAYA APPROVED |

---

### 3. MS Platform MCP — VPS port 8104
**File:** `/opt/hamaya/core/ms_platform_mcp.py`
**Token:** `MSPLATFORM_MCP_TOKEN`

| Tool | What it does |
|---|---|
| `power_list_flows` | List all Power Automate flows |
| `ms_platform_status` | Connectivity check for PA + SharePoint |

---

### 4. MS Tools MCP — VPS port 8109
**File:** `/opt/hamaya/ms/tools.py`
**Token:** `MS_TOOLS_TOKEN` | 28 tools — PA + Copilot Studio combined

**Power Automate (9 tools):**

| Tool | What it does |
|---|---|
| `list_flows` | All flows in the environment |
| `get_flow_definition` | Full JSON of a specific flow |
| `get_connection_references` | Connectors a flow depends on |
| `get_flow_runs` | Run history for a flow |
| `create_flow` ⚠️ | Create new flow — MAYA APPROVED |
| `update_flow` ⚠️ | Update flow definition — MAYA APPROVED |
| `delete_flow` ⚠️ | Delete a flow — MAYA APPROVED |
| `patch_flow` ⚠️ | Patch flow properties — MAYA APPROVED |
| `set_flow_state` ⚠️ | Enable / disable a flow — MAYA APPROVED |

**Copilot Studio (4 tools):**

| Tool | What it does |
|---|---|
| `list_copilot_agents` | All Copilot Studio bots |
| `trigger_power_automate_flow` ⚠️ | Trigger a flow from Copilot — MAYA APPROVED |
| `start_conversation` | Open a Direct Line conversation |
| `send_prompt` | Send message + get reply via Direct Line |

---

### 5. FBTW-Mcp-PA — Claude.ai connector (`mcp__FBTW-Mcp-PA__*`)
9 tools — direct Power Automate CRUD from Claude.ai session (no VPS hop):
`list_flows` · `get_flow_definition` · `get_connection_references` · `get_flow_runs` · `create_flow` · `update_flow` · `delete_flow` · `patch_flow` · `set_flow_state`

---

### 6. Azure — VPS (`az` CLI + hamaya_sovereign_core port 8200)

| Capability | How |
|---|---|
| MS Graph token | `az account get-access-token --resource https://graph.microsoft.com` |
| Copilot Studio OAuth | Client credentials via `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` |
| Entra ID commands | `entra:` prefix in hamaya_sovereign_core natural-language router |
| Azure resource commands | `azure:` prefix in hamaya_sovereign_core |

---

## GOOGLE

### 1. Search Visibility Kit — Claude.ai (`mcp__plugin_search-visibility-kit_*`)
30 tools across GA4 + GSC:

**GA4 Analytics (9 tools):**

| Tool | What it does |
|---|---|
| `run_report` | Custom GA4 report (any metrics/dimensions) |
| `run_realtime_report` | Who is on-site right now |
| `run_funnel_report` | Conversion funnel analysis |
| `run_conversions_report` | Goal completions report |
| `get_account_summaries` | All GA4 properties in the account |
| `get_property_details` | Property config and data streams |
| `get_custom_dimensions_and_metrics` | Custom event definitions |
| `list_google_ads_links` | Linked Google Ads accounts |
| `list_property_annotations` | GA4 annotations |

**Google Search Console (21 tools):**

| Tool | What it does |
|---|---|
| `get_search_analytics` | Clicks, impressions, CTR, position |
| `get_advanced_search_analytics` | Filtered / segmented search data |
| `get_performance_overview` | High-level site performance |
| `get_search_by_page_query` | Per-page keyword breakdown |
| `compare_search_periods` | Period-over-period comparison |
| `inspect_url_enhanced` | URL index status + enhancements |
| `batch_url_inspection` | Bulk URL inspection |
| `check_indexing_issues` | Crawl errors and coverage issues |
| `list_properties` | All verified GSC sites |
| `get_site_details` | Site config |
| `add_site` ⚠️ | Add a site to GSC |
| `delete_site` ⚠️ | Remove a site |
| `manage_sitemaps` ⚠️ | Submit / delete sitemaps |
| `submit_sitemap` ⚠️ | Submit a sitemap URL |
| `delete_sitemap` ⚠️ | Remove a sitemap |
| `get_sitemaps` | List all sitemaps |
| `get_sitemap_details` | Sitemap status + errors |
| `list_sitemaps_enhanced` | Extended sitemap listing |
| `get_capabilities` | What the connector can do |
| `get_creator_info` | Who authorized the connector |
| `reauthenticate` | Re-auth if token expired |

---

### 2. Google Drive — Claude.ai connector (`mcp__Google_Drive__*`)
6 tools:

| Tool | What it does |
|---|---|
| `list_recent_files` | Recently modified files |
| `search_files` | Full-text / name search |
| `get_file_metadata` | File details (size, type, owner) |
| `get_file_permissions` | Who has access |
| `read_file_content` | Read Google Docs / text files |
| `download_file_content` | Download binary / export |

---

### 3. Google Sheets — Claude.ai connector (`mcp__Google_Sheets__*`)
9 tools:

| Tool | What it does |
|---|---|
| `get_spreadsheet` | Spreadsheet metadata + sheet list |
| `get_values` | Read a cell range |
| `update_values` ⚠️ | Write to a range |
| `append_values` ⚠️ | Add rows below existing data |
| `update_spreadsheet` ⚠️ | Batch update (format, merge, etc.) |
| `batch_clear_values` ⚠️ | Clear multiple ranges |
| `insert_dimension` ⚠️ | Insert rows or columns |
| `update_formulas` ⚠️ | Write formulas to cells |
| `copy_sheet_to_another_spreadsheet` ⚠️ | Copy a tab to another file |

---

### 4. Google Calendar — Claude.ai (`mcp__plugin_small-business_google-calendar__*`)
9 tools:

| Tool | What it does |
|---|---|
| `list_calendars` | All calendars in the account |
| `list_events` | Events in a date range |
| `get_event` | Single event details |
| `create_event` ⚠️ | Create a new event |
| `update_event` ⚠️ | Edit an existing event |
| `delete_event` ⚠️ | Delete an event |
| `respond_to_event` ⚠️ | Accept / decline invite |
| `search_events` | Search by keyword |
| `suggest_time` | Find a free slot |

---

### 5. Google Marketing MCP — VPS port 8110
**File:** `/opt/hamaya/google/tools.py`
**Token:** `GOOGLE_MCP_TOKEN` | **Auth:** `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_ACCESS_TOKEN`
11 tools:

| Tool | What it does |
|---|---|
| `gm_get_analytics` | GA4 report (any metrics/dimensions/date range) |
| `gm_get_realtime` | GA4 live active users |
| `gm_get_search_console` | GSC clicks, impressions, CTR, position |
| `gm_list_gsc_sites` | All GSC verified sites |
| `gm_get_ads_campaigns` | Google Ads campaign list |
| `gm_get_ads_performance` | Ads cost / clicks / conversions by date |
| `gm_read_sheet` | Read a Sheets range |
| `gm_list_sheet_tabs` | List all tabs in a spreadsheet |
| `gm_write_sheet` ⚠️ | Write to a Sheets range — MAYA APPROVED |
| `gm_append_sheet` ⚠️ | Append rows to a sheet — MAYA APPROVED |
| `gm_list_drive_files` | List Drive files by query / folder |

---

## ARTIFACT

### Marketing Toolbox — claude.ai/artifact/HSFDJGixWSiDjrHip4Uk37
Visual command center. No MCP calls — reference + tracker only.

| What it shows | Detail |
|---|---|
| 13 Connected tools | GA4, GSC, Sealmetrics, Gmail, Drive, Sheets, Canva, Wix, Bright Data, Zapier, Calendar, Outlook/Teams, SharePoint |
| 2 Partial | ActiveCampaign (URL not set), Postiz (social accounts not linked) |
| 3 Offline | Ahrefs, Klaviyo, Mailercloud (proxy errors) |
| 6 Manual track | Print, Events, Outdoor, PR, Direct Mail, Agent Outreach |
| Activity Tracker | localStorage table — item, channel, vendor, cost, date, status, result |

---

## Port Map Summary

| Port | Server | Stack |
|---|---|---|
| 8101 | FBTW MCP (main) | VPS + PA + merged tools |
| 8102 | Governance MCP | Registers, decisions, risks |
| 8104 | MS Platform MCP | PA list + SharePoint status |
| 8105 | Supabase Admin MCP | DB admin |
| 8107 | Hostinger MCP | DNS, VPS, billing |
| 8108 | Copilot MCP | Copilot Studio tools |
| 8109 | MS Tools MCP | 28 PA + Copilot combined |
| 8110 | Google Marketing MCP | Analytics + GSC + Ads + Sheets + Drive |
| 8111 | Microsoft Marketing MCP | Teams + Outlook + SharePoint + Calendar |
| 8200 | HAMAYA Sovereign Core | HTTP natural-language router |

---

⚠️ = write operation — requires `approval="MAYA APPROVED"` on VPS MCP tools.
