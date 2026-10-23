# H@MAYA Systems Knowledge
*Last updated: 2026-10-23 · Source: VPS live inspection*

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

## MCP SERVERS (LIVE on VPS)

| Server | Domain | Port | SSL URL |
|---|---|---|---|
| fbtw-vps | VPS Commander | 8101 | https://vps-mcp.flybytheway.com/mcp |
| fbtw-gov | Gov/Universe | 8102 | https://gov-mcp.flybytheway.com/mcp |
| fbtw-ms | Microsoft 365 | 8104 | https://ms-mcp.flybytheway.com/mcp |
| fbtw-supa | Supabase | 8105 | https://supa-mcp.flybytheway.com/mcp |
| fbtw-pa | Power Automate | 8106 | https://pa-mcp.flybytheway.com/mcp |

SSL certificate: /etc/letsencrypt/live/pa-mcp.flybytheway.com/ (covers all 5 subdomains)

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
