---
name: hamaya-knowledge
description: >
  H@MAYA knowledge update and ingestion system. Use when MAYA uploads a
  file, pastes new information, or says "update knowledge", "add this",
  "learn this", "ingest this", or provides any document for HAMAYA to
  absorb. Handles all 8 knowledge domains and routes content to the
  correct file automatically.
---

# H@MAYA Knowledge Update System

## HOW TO UPLOAD KNOWLEDGE

MAYA can update HAMAYA's knowledge in 3 ways:

### Method 1 — File Upload (Preferred)
Upload any `.md`, `.txt`, `.pdf`, or `.docx` file directly in the chat.
HAMAYA reads it, extracts knowledge, routes to correct domain file, commits and pushes.

### Method 2 — Paste
Paste any text into chat and say "add this to knowledge" or "learn this".
HAMAYA identifies the domain and ingests it.

### Method 3 — VPS File
Say "ingest file at [path]" — HAMAYA reads the file from VPS directly.

---

## KNOWLEDGE DOMAINS → FILES

| Domain | File | What goes here |
|---|---|---|
| HAMAYA Constitution | `hamaya-constitution.md` | Governance rules, register articles, runtime behaviour |
| Systems & Infrastructure | `hamaya-systems.md` | VPS, portal URLs, MCP servers, nginx configs |
| Fare & Ticketing | `hamaya-fare-codex.md` (skill) | Fare construction, ATPCO, GDS commands, NDC |
| India Compliance | `india-compliance.md` | GST, DGCA, Indian carrier alerts, BSP risk |
| Carrier Policies | `carrier-policies.md` | Fare families, ceased carriers, sanctions, prefixes |
| Tool Reference | `tool-reference.md` | All 200+ tools, parameters, usage rules |
| Project Intelligence | `hamaya-projects.md` | Active projects, milestones, decisions |
| Competitive Intelligence | `hamaya-competitors.md` | Cleartrip, Yatra, FCM, BCD, Quest2Travel data |

---

## INGESTION PROCESS

When a file is uploaded or content is pasted:

1. **Identify domain** — which knowledge file does this belong to?
2. **Check for supersession** — does this replace existing content or add to it?
3. **Extract key facts** — structured tables, rules, policies, dates
4. **Date-stamp** — add `*Last updated: YYYY-MM-DD*` to modified sections
5. **Confidence label** — mark Low/Med/High confidence where appropriate
6. **Write to file** — append or replace the relevant section
7. **Commit and push** — single commit with clear message
8. **Confirm to MAYA** — list exactly what was added/changed

---

## QUALITY RULES

- **No hallucinations** — only write what the uploaded content actually says
- **Confidence labeling** — if source is unclear, mark as `(Confidence: Low)`
- **Supersession** — when new info contradicts existing, keep BOTH with dates, newest on top
- **No loss** — archived content moves to `## ARCHIVED (YYYY-MM-DD)` section, never deleted
- **Source tracking** — every section must have `*Source: [filename or description]*`

---

## KNOWLEDGE GAP ESCALATION

If MAYA asks something not in any knowledge file:
> "Not in current knowledge base. Gap: [exact missing topic]. To add: upload a document covering [topic] and say 'ingest this'."

---

## WHAT HAMAYA KNOWS (Current Modules)

| Module | Status | Last Updated |
|---|---|---|
| HAMAYA Constitution (Groups A-K) | ✅ LOADED | 2026-10-23 |
| India Compliance (GST 2.0, DGCA 2026) | ✅ LOADED | 2026-10-23 |
| Carrier Policies (100 airlines) | ✅ LOADED | 2026-10-23 |
| Systems & Infrastructure (VPS, MCP) | ✅ LOADED | 2026-10-23 |
| Tool Reference (200+ tools) | ✅ LOADED | 2026-10-23 |
| Fare Construction Codex | ✅ LOADED (skill) | 2026-10-23 |
| Project Intelligence | ⬜ EMPTY — upload to populate | — |
| Competitive Intelligence | ⬜ EMPTY — upload to populate | — |
