# Nmap MCP Server

**Dockerized Kali Linux container exposing Nmap scanning as an MCP (Model Context Protocol) tool for AI agents.**

# Agent Instructions

## Personas

Use these roles to define your behavior for specific tasks:

- **Security Researcher**: Adopt this role for network audits and vulnerability discovery.
- Path: [.agents/identities/security-researcher.md](./.agents/identities/security-researcher.md)

## Skills

You have access to the following specialized capabilities:

- **Nmap Recon**: Perform network scans and service enumeration.
  - Documentation: [.agents/skills/nmap-mcp-server/SKILL.md](./.agents/skills/nmap-mcp-server/SKILL.md)

## Operational Boundaries

- **Always**: Verify target authorization before initiating any scan.
- **Ask First**: Before performing vulnerability scripts (`--script vuln`) on production IPs.

## Use Case

Allow AI agents to perform network reconnaissance (port scanning, service detection, OS fingerprinting) using Nmap inside a disposable Kali Linux container. The agent sends commands via MCP, and the container executes Nmap securely.

## Architecture

```
AI Client (Claude, etc.)
    │  MCP protocol (stdio)
    ▼
Docker Container (kalilinux/kali-rolling)
    │
    ├── uv  (Python package manager)
    ├── server.py  (FastMCP server)
    │       ├── @mcp.tool()  →  nmap_scan(target, flags, ports)
    │       └── @mcp.tool()  →  ping_scan(target)
    └── nmap
```

- **Base image**: `kalilinux/kali-rolling`
- **Runtime**: `uv run server.py` (entrypoint)
- **Transport**: MCP stdio

## Available Tool

### `nmap_scan`

Accepts typed parameters for target, flags, and ports, and assembles the Nmap command internally.

| Parameter | Type  | Default | Description                                 |
| --------- | ----- | ------- | ------------------------------------------- |
| `target`  | `str` | —       | The target to scan (IP address or hostname) |
| `flags`   | `str` | `""`    | Additional Nmap flags (e.g., `"-sV -O"`)    |
| `ports`   | `str` | `""`    | Specific ports to scan (e.g., `"80,443"`)   |

**Response format** (`Dict[str, Any]`):

```json
{
  "stdout": "...",
  "stderr": "...",
  "returncode": 0
}
```

On error/timeout:

```json
{
  "error": "Nmap scan timed out"
}
```

### `ping_scan`

Performs a ping scan (`nmap -sn`) on the specified target.

| Parameter | Type  | Default | Description                                 |
| --------- | ----- | ------- | ------------------------------------------- |
| `target`  | `str` | —       | The target to scan (IP address or hostname) |

Same response format as `nmap_scan`.

**Calling from an AI agent:**

```
nmap_scan(target: "127.0.0.1")
nmap_scan(target: "scanme.nmap.org", flags: "-sV", ports: "22,80")
nmap_scan(target: "192.168.1.0/24", flags: "-sn")
nmap_scan(target: "10.0.0.1", flags: "-A -T4")
ping_scan(target: "192.168.1.0/24")
```

**Defaults & Limits:**

- **Timeout**: 5 minutes (cannot be overridden by the Agent)

## How to Run

```bash
# Using the helper script
./run_dev

# Or directly
docker run --rm -it -v $(pwd)/src:/src nmap-mcp-server
```

The `src/` directory is volume-mounted so changes take effect without rebuilding.

## Development

```bash
cd src
uv sync          # install dependencies
uv run server.py # start server directly (for testing)
```

Dependencies are managed with `uv` and declared in `pyproject.toml`:

- `mcp[cli]>=1.27.0`
- `pytest>=9.0.3`

## Security Considerations

- Nmap runs inside a temporary container — no persistent access to the host
- Input is split on whitespace and passed directly to Nmap — no sanitization beyond a basic empty-target check
- The tool's `annotations` could be set to `destructiveHint=True` to warn clients that it performs network probes

## Suggested Improvements

- Add port range validation
- Improve error messages for common Nmap errors
- Make timeout configurable as a tool parameter
