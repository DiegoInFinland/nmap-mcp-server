# Nmap MCP Server

**Dockerized Kali Linux container exposing Nmap scanning as an MCP (Model Context Protocol) tool for AI agents.**

# Agent Instructions

## Architecture

```
AI Client (Claude, etc.)
    │  MCP protocol (stdio)
    ▼
Docker Container (kalilinux/kali-rolling)
    │
    ├── uv             (Python package manager)
    ├── src/server.py  (FastMCP server)
│       ├── @mcp.tool()  →  nmap_scan(target, flags, ports)
│       ├── @mcp.tool()  →  ping_scan(target)
│       └── @mcp.tool()  →  ping6_scan(target)
    └── nmap
```

- **Base image**: `kalilinux/kali-rolling`
- **Runtime**: `uv run src/server.py` (entrypoint)
- **Transport**: MCP stdio

## How to Run

```bash
# Using the helper script (hot-reload with source mount)
./run_dev.sh

# Or without hot-reload
docker run --rm --network host -i nmap-mcp-server
```

## Development

```bash
uv sync          # install dependencies
uv run src/server.py # start server directly (for testing)
```

Dependencies are managed with `uv` and declared in `pyproject.toml`:

## Security Considerations

- Nmap runs inside a temporary container — no persistent access to the host
- Input is split on whitespace and passed directly to Nmap
- File output flags (`-oN`, `-oX`, `-oG`, `-oS`, `-oA`, `--output-xml`) are blocked via `DENY_FLAGS`
- Port values are validated to be within 1-65535 and well-formed ranges
- The tool's `annotations` could be set to `destructiveHint=True` to warn clients that it performs network probes
- If unsure, stop and ask.
