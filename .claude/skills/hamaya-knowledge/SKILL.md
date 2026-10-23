---
name: hamaya-knowledge
description: >
  H@MAYA live knowledge base. Loads all domain knowledge files into the
  agent context: fare rules, carrier policies, travel ops, GST/DGCA updates,
  business SOPs, portal architecture, and any file MAYA has uploaded.
  Use before any fare, booking, compliance, ops, or system question.
  Also defines the knowledge UPDATE PROCESS — how to add new files.
---

# H@MAYA Knowledge Base

## HOW TO UPDATE KNOWLEDGE (Upload Process)

### Method 1 — Share a file in this chat
Drop the file (PDF, Word, Excel, text) directly in the conversation.
Claude will:
1. Read and extract all structured knowledge
2. Add it to the correct knowledge file in `.claude/knowledge/`
3. Commit and push — active in the agent on next session

### Method 2 — Paste content directly
Paste any text, table, policy, or fare rule into the chat.
Say: "Add this to [domain]" — e.g. "Add this to fare rules" or "Add this to carrier policies"
Claude will extract → structure → write to the correct `.claude/knowledge/` file.

### Method 3 — VPS file upload
For large files already on your system:
Use `vps_upload_file` to push to `/var/www/hamaya-knowledge/`
Then tell Claude: "Ingest the file at [path]"

### Knowledge File Map
| What you share | Goes into |
|---|---|
| Fare rules, RBD, ATPCO | `.claude/knowledge/fare-codex.md` |
| Carrier policies (new/updated) | `.claude/knowledge/carrier-policies.md` |
| GST / DGCA / compliance | `.claude/knowledge/india-compliance.md` |
| NDC / API / tech updates | `.claude/knowledge/tech-distribution.md` |
| Corporate client SOPs | `.claude/knowledge/corporate-sops.md` |
| Portal / system architecture | `.claude/knowledge/hamaya-systems.md` |
| Competitor intel | `.claude/knowledge/market-intel.md` |
| Founder decisions / strategy | `.claude/knowledge/founder-strategy.md` |

---

## LOADED KNOWLEDGE MODULES

### Module 1 — Fare Construction Codex (hamaya-fare-codex skill)
STATUS: ✅ LIVE — 100 airlines, ATPCO Cat 1-35, NUC/ROE/BSR, NDC, BSP/ADM
Source: FlyByTheWay Internal · The Codex + Vol 2 · 2026

### Module 2 — India Compliance (india-compliance.md)
STATUS: ✅ LIVE — GST 2.0 (Sep 2025), DGCA 2026, statutory tax rules

### Module 3 — Carrier Policies (carrier-policies.md)
STATUS: ✅ LIVE — Gulf, Europe, APAC, India, Americas, CIS carriers

### Module 4 — Hamaya Systems (hamaya-systems.md)
STATUS: ✅ LIVE — Portal facts, MCP servers, API endpoints, nginx config

### Module 5 — [Your uploads land here]
STATUS: 🔲 EMPTY — Share a file to populate

---

## KNOWLEDGE QUALITY RULES

1. **No hallucinations** — every fare rule must cite The Codex or a carrier source
2. **Confidence labeling** — High / Med / Low on every claim
3. **Date-stamp updates** — every addition tagged with date added
4. **Supersession rule** — newer file overwrites older on same topic
5. **Escalation rule** — if not in knowledge base, say so and escalate to MAYA

---

## CURRENT KNOWLEDGE BASE CONTENTS
