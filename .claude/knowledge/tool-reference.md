# H@MAYA Complete Tool Reference
*All 200+ tools — every parameter, every use case*
*Last updated: 2026-10-23 · No AI/Anthropic tools*

---

## GROUP 1 — VPS COMMANDER (fbtw-vps)
*Server: https://vps-mcp.flybytheway.com/mcp*

### vps_status
What: Full server health snapshot
Returns: OS, RAM, disk, uptime, load average, nginx status
When to use: Every morning briefing, before any deployment

### get_vps_system_status
What: Detailed system metrics
Returns: CPU%, memory breakdown, disk per partition, network stats
When to use: Performance investigation, capacity planning

### vps_list_hosts
What: Lists all configured VPS hosts in the connector
Returns: Host names, modes (read-only vs read-write)
When to use: First call to confirm what hosts are available

### vps_run_command
What: Execute shell command on VPS
Parameters: `command` (string) — allowed: ls, cat, ps, df, pm2 list, systemctl status
Returns: stdout, stderr, exit code
Note: Read-only mode — shell metacharacters (;, |, >) blocked
When to use: Check directory contents, read config files, check process status

### vps_read_file
What: Read a file from VPS filesystem
Parameters: `path` (full absolute path)
Returns: File contents as text
When to use: Reading nginx configs, app files, log files

### vps_write_file
What: Write/overwrite a file on VPS
Parameters: `path`, `content`
Note: Requires write mode — confirm with MAYA before use
When to use: Updating nginx config, app files, knowledge files on server

### vps_list_directory
What: List contents of a directory
Parameters: `path` (directory path)
Returns: Files and subdirectories with sizes and dates
When to use: Exploring server filesystem

### vps_download_file
What: Download file from VPS to local context
Parameters: `path` (VPS path)
Returns: File content
When to use: Retrieving reports, exports, logs for analysis

### vps_upload_file
What: Upload file from local to VPS
Parameters: `path` (destination), `content`
When to use: Deploying updated app files, configs, knowledge files

### vps_list_processes
What: List all running processes
Returns: PID, name, CPU%, memory%, command
When to use: Debugging, performance investigation

### vps_docker_ps
What: List running Docker containers
Returns: Container ID, image, status, ports, names
When to use: If any services are containerized

### get_pm2_status
What: PM2 process manager status
Returns: All PM2 processes — name, status, CPU, memory, restarts, uptime
When to use: Confirming all backend services are running

### vps_tail_log
What: Read last N lines of a log file
Parameters: `path`, `lines` (number, default 100)
Returns: Last N log lines
When to use: Debugging errors, checking recent activity

### get_flybrain_logs
What: FlyBrain application-specific logs
Returns: Structured log entries from FlyBrain service
When to use: Debugging booking or intelligence engine issues

### vps_service
What: Check or control a system service
Parameters: `service` (name), `action` (status/start/stop/restart)
When to use: Managing nginx, node services, system daemons

### vps_disconnect
What: Disconnect from VPS session
When to use: Cleanup after VPS operations

---

## GROUP 2 — POWER AUTOMATE (fbtw-pa)
*Server: https://pa-mcp.flybytheway.com/mcp*

### list_flows
What: List all Power Automate flows
Returns: Flow ID, name, state (enabled/disabled), last run, trigger type
When to use: Audit automation status, find a flow to run or update

### get_flow_definition
What: Get complete flow definition and logic
Parameters: `flow_id`
Returns: Full flow JSON — triggers, actions, conditions, connections
When to use: Understanding what a flow does before modifying

### get_flow_runs
What: History of flow executions
Parameters: `flow_id`, `top` (number of runs)
Returns: Run ID, start time, end time, status (succeeded/failed/running)
When to use: Debugging failed automations, confirming execution

### create_flow
What: Create a new Power Automate flow
Parameters: flow definition JSON
Note: Requires MAYA APPROVED
When to use: Building new automations

### update_flow
What: Replace entire flow definition
Parameters: `flow_id`, new definition
Note: Requires MAYA APPROVED
When to use: Major flow restructure

### patch_flow
What: Update specific parts of a flow
Parameters: `flow_id`, partial update object
Note: Requires MAYA APPROVED
When to use: Small changes to existing flow (e.g., update an email address)

### set_flow_state
What: Enable or disable a flow
Parameters: `flow_id`, `state` (enabled/disabled)
Note: Requires MAYA APPROVED
When to use: Turning automations on/off temporarily

### delete_flow
What: Permanently delete a flow
Parameters: `flow_id`
Note: Requires MAYA APPROVED — irreversible
When to use: Removing obsolete automations

### get_connection_references
What: List all connections used by flows (SharePoint, Outlook, Teams, etc.)
Returns: Connection names, types, status
When to use: Checking which connectors are active, troubleshooting auth failures

### trigger_power_automate
What: Manually trigger a flow that has an HTTP trigger
Parameters: `flow_id`, `body` (payload)
When to use: Running on-demand automations (reports, notifications, sync jobs)

---

## GROUP 3 — MICROSOFT 365 (fbtw-ms)
*Server: https://ms-mcp.flybytheway.com/mcp*

### OUTLOOK — EMAIL

#### outlook_email_search
What: Search emails
Parameters: `query` (text), `folder`, `top` (count), date filters
Returns: Email list with subject, sender, date, snippet
When to use: Finding a specific email, auditing communications

#### outlook_send_mail
What: Send an email immediately
Parameters: `to`, `subject`, `body`, `cc`, `bcc`, `attachments`
Note: Requires MAYA APPROVED
When to use: Sending client comms, reports, alerts

#### outlook_create_draft
What: Create email draft (not sent)
Parameters: `to`, `subject`, `body`
Returns: Draft ID
When to use: Preparing email for MAYA review before sending

#### outlook_create_reply_draft
What: Create reply draft to existing email
Parameters: `message_id`, `body`
When to use: Drafting responses to client or supplier emails

#### outlook_create_reply_all_draft
What: Reply-all draft
Parameters: `message_id`, `body`
When to use: Team or client thread responses

#### outlook_send_draft
What: Send a previously created draft
Parameters: `draft_id`
Note: Requires MAYA APPROVED
When to use: Sending approved drafts

#### outlook_forward_mail
What: Forward an email
Parameters: `message_id`, `to`, `comment`
When to use: Routing emails to correct person

#### outlook_update_draft
What: Edit an existing draft
Parameters: `draft_id`, fields to update
When to use: Revising draft before sending

#### outlook_delete_draft
What: Delete a draft
Parameters: `draft_id`

#### outlook_trash_thread / outlook_untrash_thread
What: Move thread to trash / restore
Parameters: `thread_id`

#### outlook_modify_labels / outlook_modify_thread_labels
What: Add/remove labels on message or thread
Parameters: `message_id` or `thread_id`, `add_labels`, `remove_labels`

#### outlook_batch_delete_messages
What: Delete multiple messages at once
Parameters: `message_ids` (array)

#### outlook_batch_modify_labels
What: Bulk label change
Parameters: `message_ids`, `add_labels`, `remove_labels`

#### outlook_create_filter
What: Create email filter rule
Parameters: filter criteria, action

#### outlook_create_label / outlook_update_label / outlook_delete_label
What: Manage custom labels/folders

#### outlook_set_vacation
What: Set out-of-office auto-reply
Parameters: `enabled`, `start_date`, `end_date`, `message`

### OUTLOOK — CALENDAR

#### outlook_calendar_search
What: Search calendar events
Parameters: `query`, date range
When to use: Finding meetings, checking availability

#### outlook_create_event
What: Create calendar event
Parameters: `subject`, `start`, `end`, `attendees`, `location`, `body`, `online_meeting`
Note: Requires MAYA APPROVED
When to use: Scheduling meetings, setting reminders

#### outlook_update_event
What: Update existing event
Parameters: `event_id`, fields to change

#### outlook_delete_event
What: Delete event
Parameters: `event_id`

#### outlook_respond_to_event
What: Accept/decline/tentative a meeting invitation
Parameters: `event_id`, `response` (accept/decline/tentative), `comment`

#### outlook_find_available_time / find_meeting_availability
What: Find free slots for a meeting
Parameters: `attendees`, `duration`, date range
Returns: Available time slots for all attendees
When to use: Scheduling with multiple people

### TEAMS

#### teams_list_teams
What: List all Teams the account is in
Returns: Team IDs, names, descriptions

#### teams_list_channels
What: List channels in a team
Parameters: `team_id`
Returns: Channel IDs, names, types

#### teams_list_chats
What: List direct chats and group chats
Returns: Chat IDs, names, participants

#### teams_list_channel_messages
What: Read messages from a channel
Parameters: `team_id`, `channel_id`, `top`
Returns: Messages with sender, timestamp, content

#### teams_send_channel_message
What: Post to a Teams channel
Parameters: `team_id`, `channel_id`, `content`
Note: Requires MAYA APPROVED

#### teams_reply_channel_message
What: Reply in a Teams channel thread
Parameters: `team_id`, `channel_id`, `message_id`, `content`

#### teams_send_chat_message
What: Send a direct/group chat message
Parameters: `chat_id`, `content`
Note: Requires MAYA APPROVED

#### teams_create_chat
What: Create a new chat
Parameters: `members` (array of user IDs), `topic`

#### chat_message_search
What: Search across all chats and channels
Parameters: `query`

### SHAREPOINT

#### sharepoint_search
What: Search across SharePoint sites and documents
Parameters: `query`, `site_url`
Returns: Document titles, URLs, modified dates, snippets

#### sharepoint_upload_file
What: Upload a file to SharePoint
Parameters: `site_url`, `folder_path`, `file_name`, `content`
Note: Requires MAYA APPROVED

#### sharepoint_update_file
What: Update existing file content
Parameters: `site_url`, `file_path`, `content`

#### sharepoint_copy_item
What: Copy a file or folder
Parameters: `site_url`, `source_path`, `destination_path`

#### sharepoint_move_item
What: Move a file or folder
Parameters: `site_url`, `source_path`, `destination_path`

#### sharepoint_rename_item
What: Rename a file or folder
Parameters: `site_url`, `item_path`, `new_name`

#### sharepoint_delete_item
What: Delete a file or folder
Parameters: `site_url`, `item_path`
Note: Requires MAYA APPROVED

#### sharepoint_create_folder
What: Create a new folder
Parameters: `site_url`, `parent_path`, `folder_name`

#### sharepoint_folder_search
What: Search within a specific folder
Parameters: `site_url`, `folder_path`, `query`

### PEOPLE

#### search_people
What: Search for people in the organisation
Parameters: `query`
Returns: Name, email, job title, department

#### get_me
What: Get the authenticated account's profile
Returns: Name, email, ID, job title

#### get_granted_scopes
What: List what permissions this connection has
Returns: All OAuth scopes granted

#### read_resource
What: Read a Microsoft 365 resource by URL
Parameters: `url` (Graph API URL)
When to use: Direct Graph API access for anything not covered by named tools

---

## GROUP 4 — SUPABASE DATABASE (fbtw-supa)
*Server: https://supa-mcp.flybytheway.com/mcp*

### supabase_health
What: Check database connection and health
Returns: Connection status, response time
When to use: Every startup check, before DB operations

### supabase_list_tables
What: List all tables in the database
Returns: Table names, schemas
When to use: Exploring database structure

### supabase_describe_table
What: Get table schema
Parameters: `table` (name)
Returns: Columns, types, constraints, indexes, foreign keys
When to use: Understanding a table before querying

### supabase_select
What: Query rows from a table
Parameters: `table`, `columns`, `filter`, `order`, `limit`
Returns: Matching rows
When to use: Reading any data — bookings, clients, transactions, etc.

### supabase_insert_row
What: Insert a new row
Parameters: `table`, `data` (object with column:value pairs)
Note: Requires MAYA APPROVED
When to use: Adding new records

### supabase_update_row
What: Update existing rows
Parameters: `table`, `filter` (which rows), `data` (new values)
Note: Requires MAYA APPROVED
When to use: Updating existing records

### supabase_upsert_row
What: Insert or update (if exists)
Parameters: `table`, `data`, `on_conflict` (unique key)
Note: Requires MAYA APPROVED
When to use: Sync operations where row may or may not exist

### supabase_delete_row
What: Delete rows
Parameters: `table`, `filter`
Note: Requires MAYA APPROVED — confirm before deleting
When to use: Removing records (soft delete preferred)

### supabase_row_count
What: Count rows matching a filter
Parameters: `table`, `filter` (optional)
Returns: Count number
When to use: Quick metrics — "how many bookings this month"

### supabase_list_registers
What: List all register tables
Returns: Register names and metadata
When to use: Exploring what registers exist in the universe

### get_supabase_scan_stats
What: Performance stats — sequential scans, index usage
Returns: Tables with high seq scan counts (missing indexes)
When to use: Database performance auditing

### read_supabase
What: Raw Supabase read with PostgREST syntax
Parameters: `resource` (table/view path), `params`
When to use: Complex queries not covered by standard select

---

## GROUP 5 — UNIVERSE / GOV REGISTER (fbtw-gov)
*Server: https://gov-mcp.flybytheway.com/mcp*

### LOGGING — Founder Activity

#### log_founder_activity
What: Record anything the founder did, decided, or communicated
Parameters: `activity`, `context`, `outcome`, `date`
When to use: After every meaningful action, decision, or meeting

#### log_decision
What: Log a business decision with rationale
Parameters: `decision`, `rationale`, `owner`, `deadline`, `impact`
When to use: Any significant business decision made

#### log_commitment
What: Record a commitment made to someone
Parameters: `commitment`, `to_whom`, `deadline`, `context`
When to use: Any promise or commitment given by MAYA or the business

#### log_risk
What: Document a risk item
Parameters: `risk`, `likelihood`, `impact`, `mitigation`, `owner`
When to use: New risks identified in operations, market, or compliance

#### log_project
What: Register a project or initiative
Parameters: `name`, `description`, `owner`, `timeline`, `status`
When to use: Starting any new project or initiative

#### log_intelligence
What: Store market or competitive intelligence
Parameters: `source`, `content`, `relevance`, `confidence`
When to use: Any useful industry insight, competitor move, or market signal

#### log_opportunity
What: Document a business opportunity
Parameters: `opportunity`, `value_estimate`, `source`, `next_action`, `deadline`
When to use: Any potential revenue or partnership opportunity

#### log_discussion
What: Record a meeting or discussion
Parameters: `with_whom`, `topic`, `outcome`, `actions`
When to use: After any external meeting or internal strategy discussion

#### log_escalation
What: Flag an issue that needs escalation
Parameters: `issue`, `severity`, `escalate_to`, `deadline`
When to use: Any issue that can't be resolved at current level

### REGISTERS — Data Management

#### read_register
What: Read contents of a Universe register
Parameters: `register_name`, filters
Returns: Register rows
When to use: Checking any business register (clients, opportunities, risks, etc.)

#### create_register_list
What: Create a new register (list)
Parameters: `name`, `columns` (schema)
Note: Requires MAYA APPROVED
When to use: Setting up new tracking for a new area

#### get_register_schema
What: Get the column structure of a register
Parameters: `register_name`
When to use: Before querying or updating a register

#### ensure_columns
What: Add columns to a register if they don't exist
Parameters: `register_name`, `columns`
When to use: Extending an existing register's schema

#### update_item
What: Update a row in a register
Parameters: `register_name`, `item_id`, `data`
Note: Requires MAYA APPROVED

#### close_item
What: Mark an item as closed/completed
Parameters: `register_name`, `item_id`

#### link_records
What: Create a link between two register records
Parameters: `source_register`, `source_id`, `target_register`, `target_id`
When to use: Connecting related items (e.g., project → risk, opportunity → client)

#### audit_registers
What: Run an audit across all registers
Returns: Summary of record counts, recent activity, anomalies
When to use: Weekly governance check

### UNIVERSE

#### list_universe
What: List all entities in the FBTW Universe
Returns: All registered entities (companies, projects, people, etc.)
When to use: Getting a full picture of the business universe

#### query_universe_entity
What: Query a specific entity
Parameters: `entity_type`, `query`
Returns: Matching entities with all attributes
When to use: Looking up a specific client, project, or competitor

#### sync_universe_to_competitor_register
What: Sync competitor data from Universe into the competitor register
When to use: Keeping competitor tracking up to date

### REPORTING

#### create_excel_report
What: Generate an Excel report from register data
Parameters: `register_name`, `columns`, `filters`, `filename`
Returns: Excel file
When to use: Weekly reports, board packs, data exports

#### create_daily_report_xlsx
What: Auto-generate daily report
Returns: Excel with day's activity across all registers
When to use: Every morning or end of day

#### generate_review
What: Generate a narrative review document
Parameters: `scope`, `period`
Returns: Structured review text
When to use: Weekly/monthly business reviews

#### generate_and_stream_pdf
What: Generate and stream a PDF document
Parameters: `content`, `template`, `filename`
When to use: Client reports, proposals, formal documents

### BRIEFINGS

#### get_latest_brief
What: Pull MAYA's latest briefing document
Returns: Current priorities, open items, recent decisions
When to use: Morning briefing, re-orientation during work session

#### get_founder_activity_centre
What: Founder's activity dashboard
Returns: Recent logs, open commitments, pending decisions, risks
When to use: Status check, end-of-day review

#### get_api_health
What: FBTW API health status
Returns: All API endpoints status and response times
When to use: System health check

#### create_command_center_page
What: Create/update the H@MAYA command center page
Parameters: `content` (structured data for the page)
When to use: Updating the live command center view

### OTHER

#### classify_notification
What: Classify an incoming notification by type and priority
Parameters: `notification_content`
Returns: Type, priority, recommended action
When to use: Processing incoming alerts or messages

#### sync_automation_registry
What: Sync all Power Automate flows into the automation register
When to use: Weekly audit, after creating/modifying flows

#### create_sharepoint_document
What: Create a document in SharePoint
Parameters: `site`, `folder`, `name`, `content`
Note: Requires MAYA APPROVED
When to use: Creating formal documents, SOPs, reports in SharePoint

---

## GROUP 6 — GOOGLE DRIVE (google-drive)

### search_files
What: Search files across Google Drive
Parameters: `query`, `mime_type`, `parent_folder`
Returns: File names, IDs, URLs, modified dates
When to use: Finding any Drive document

### read_file_content
What: Read file contents
Parameters: `file_id`
Returns: File text content
When to use: Reading Google Docs, text files

### get_file_metadata
What: Get file info without reading content
Parameters: `file_id`
Returns: Name, type, size, owner, modified date, sharing settings

### get_file_permissions
What: Check who has access to a file
Parameters: `file_id`
Returns: Permission list with emails and roles (viewer/editor/owner)

### list_recent_files
What: List recently modified files
Parameters: `top` (count)
Returns: Files sorted by last modified

### download_file_content
What: Download file in its native format
Parameters: `file_id`, `mime_type` (export format)
When to use: Exporting Google Docs as Word/PDF

---

## GROUP 7 — GOOGLE SHEETS (google-sheets)

### get_spreadsheet
What: Get spreadsheet structure and metadata
Parameters: `spreadsheet_id`
Returns: Sheet names, IDs, dimensions
When to use: First step before reading/writing any sheet

### get_values
What: Read cell values from a range
Parameters: `spreadsheet_id`, `range` (e.g., "Sheet1!A1:D20")
Returns: 2D array of values
When to use: Reading data from any tracking sheet

### update_values
What: Write values to a range
Parameters: `spreadsheet_id`, `range`, `values` (2D array)
Note: Requires MAYA APPROVED
When to use: Updating dashboards, trackers, reports

### append_values
What: Append rows to the end of data
Parameters: `spreadsheet_id`, `range`, `values`
When to use: Adding new records to a log or tracker

### update_spreadsheet
What: Update spreadsheet properties (title, locale, timezone)
Parameters: `spreadsheet_id`, properties

### update_formulas
What: Update cell formulas
Parameters: `spreadsheet_id`, `range`, `formulas`
When to use: Updating calculated fields

### batch_clear_values
What: Clear multiple ranges at once
Parameters: `spreadsheet_id`, `ranges` (array)

### insert_dimension
What: Insert rows or columns
Parameters: `spreadsheet_id`, `sheet_id`, `dimension` (ROWS/COLUMNS), `start`, `end`

### copy_sheet_to_another_spreadsheet
What: Copy a sheet tab to a different spreadsheet
Parameters: `source_spreadsheet_id`, `sheet_id`, `destination_spreadsheet_id`
When to use: Creating report copies, archiving monthly data

---

## GROUP 8 — CANVA

### create_design
What: Create a new Canva design
Parameters: `design_type` (presentation/document/social/etc.), `title`
Returns: Design ID, editor URL
When to use: Creating presentations, social posts, marketing materials

### edit_design
What: Open a design for editing
Parameters: `design_id`
Returns: Editor URL

### generate_design
What: AI-generate a design from a brief
Parameters: `design_type`, `prompt`
When to use: Quick first drafts from description

### generate_image
What: Generate an image
Parameters: `prompt`, `style`
Returns: Image URL

### export_design
What: Export design to file
Parameters: `design_id`, `format` (PDF/PNG/JPG/PPTX/MP4)
Returns: Download URL

### search_designs
What: Search existing designs
Parameters: `query`
Returns: Matching designs with IDs

### list_brand_kits
What: List all brand kits
Returns: Brand kit IDs, names, colors, fonts, logos

### list_folder_items
What: List contents of a Canva folder
Parameters: `folder_id`

### resize_design
What: Resize a design to new dimensions
Parameters: `design_id`, `width`, `height` or `design_type`

### remove_background
What: Remove image background
Parameters: `image_id` or upload

### upload_asset_from_url
What: Upload an image from URL into Canva
Parameters: `url`, `name`

### create_upload_url
What: Get a signed URL to upload an asset
Returns: Upload URL for direct upload

### get_design_dataset
What: Get data connected to a design (for data-driven designs)
Parameters: `design_id`

### create_brand_template_draft
What: Create a new brand template
Parameters: `design_id`, template settings

---

## GROUP 9 — HOSTINGER (via gov/VPS)

### VPS Management
#### hostinger_vps_list — List all Hostinger VPS instances
#### hostinger_vps_get — Get details of a specific VPS (IP, OS, specs, status)
#### hostinger_vps_metrics — CPU, RAM, disk, bandwidth usage over time
#### hostinger_vps_firewall_list — List firewall rules
#### hostinger_vps_ssh_keys — List SSH keys configured
#### hostinger_vps_start — Start a stopped VPS (Requires MAYA APPROVED)
#### hostinger_vps_stop — Stop a VPS (Requires MAYA APPROVED)
#### hostinger_vps_restart — Restart a VPS (Requires MAYA APPROVED)
#### hostinger_vps_datacenters — List available datacenters

### DNS Management
#### hostinger_dns_list — List all DNS records for a domain
Parameters: `domain`
Returns: All A, CNAME, MX, TXT, NS records

#### hostinger_dns_update — Update a DNS record
Parameters: `domain`, `record_type`, `name`, `value`, `ttl`
Note: Requires MAYA APPROVED — DNS changes propagate globally

#### hostinger_dns_delete — Delete a DNS record
Note: Requires MAYA APPROVED

#### hostinger_dns_validate — Validate DNS record before applying
Parameters: `domain`, record to validate
Returns: Validation result

#### hostinger_dns_reset — Reset DNS to Hostinger defaults
Note: Requires MAYA APPROVED — use with extreme caution

### Domains
#### hostinger_domains_list — List all domains in the account
#### hostinger_domains_transfers — List domain transfer status

### Hosting
#### hostinger_hosting_websites — List all hosted websites
#### hostinger_hosting_ssl_status — SSL certificate status per domain
#### hostinger_hosting_subdomains — List all subdomains

### Billing
#### hostinger_billing_subscriptions — All active subscriptions, renewal dates, costs

---

## TOOL USAGE RULES

### Always parallel (run simultaneously)
- vps_status + supabase_health + get_pm2_status (morning check)
- Any independent data reads across different systems

### Always sequential (one after another)
- supabase_describe_table → supabase_select (need schema before querying)
- get_flow_definition → patch_flow (need to read before modifying)
- read_register → update_item (need current state before updating)

### Always log after
- Any decision → log_decision
- Any commitment → log_commitment
- Any external meeting → log_discussion
- Any risk identified → log_risk

### Requires MAYA APPROVED
All write/create/delete/modify operations on live systems.
Pull → show MAYA → confirm → execute.
