# Nmap MCP Server

**Dockerized Kali Linux container exposing Nmap scanning as an MCP (Model Context Protocol) tool for AI agents.**

# Agent Instructions

## Personas

Use these roles to define your behavior for specific tasks:

- **Security Researcher**: Adopt this role for network audits and vulnerability discovery.
- Path: [.opencode/agents/security-researcher.md](./.opencode/agents/security-researcher.md)

## Skills

You have access to the following specialized capabilities:

- **nmap-scan-skill**: Perform network scans and service enumeration.
  - Documentation: [.agents/skills/nmap-mcp-skill/SKILL.md](./.agents/skills/nmap-scan-skill/SKILL.md)

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

On timeout:

```json
{
  "stdout": "",
  "stderr": "Nmap scan timed out after 300 seconds",
  "returncode": -1
}
```

On unexpected error:

```json
{
  "error": "Error executing Nmap: ..."
}
```

### `ping_scan`

Performs a ping scan (`nmap -sn -R --disable-arp-ping -PE`) on the specified target. Uses ICMP echo requests to avoid ARP ghosts (common in Docker/bridge networks).

| Parameter | Type  | Default | Description                                 |
| --------- | ----- | ------- | ------------------------------------------- |
| `target`  | `str` | —       | The target to scan (IP address or hostname) |

Same response format as `nmap_scan`.

### `ping6_scan`

Performs an IPv6 ping scan (`nmap -6 -sn -R`) on the specified target. Uses Nmap's IPv6 support to discover live IPv6 hosts.

| Parameter | Type  | Default | Description                              |
| --------- | ----- | ------- | ---------------------------------------- |
| `target`  | `str` | —       | The IPv6 target to ping (IP or hostname) |

Same response format as `nmap_scan`.

**Calling from an AI agent:**

```
nmap_scan(target: "127.0.0.1")
nmap_scan(target: "scanme.nmap.org", flags: "-sV", ports: "22,80")
nmap_scan(target: "192.168.1.0/24", flags: "-sn")
nmap_scan(target: "10.0.0.1", flags: "-A -T4")
ping_scan(target: "192.168.1.0/24")
ping6_scan(target: "2001:db8::1")
```

**Defaults & Limits:**

- **Timeout**: 5 minutes (cannot be overridden by the Agent)

## How to Run

```bash
# Using the helper script (hot-reload with source mount)
./run_dev.sh

# Or without hot-reload
docker run --rm --network host -i nmap-mcp-server
```

The project root is volume-mounted so changes take effect without rebuilding.

## Development

```bash
uv sync          # install dependencies
uv run src/server.py # start server directly (for testing)
```

Dependencies are managed with `uv` and declared in `pyproject.toml`:

- `mcp[cli]>=1.27.0`
- `pytest>=9.0.3`

## Security Considerations

- Nmap runs inside a temporary container — no persistent access to the host
- Input is split on whitespace and passed directly to Nmap
- File output flags (`-oN`, `-oX`, `-oG`, `-oS`, `-oA`, `--output-xml`) are blocked via `DENY_FLAGS`
- Port values are validated to be within 1-65535 and well-formed ranges
- The tool's `annotations` could be set to `destructiveHint=True` to warn clients that it performs network probes

## Nmap Command Cheat Sheet

### Basic Scan

```bash
# Scan a single host
nmap 192.168.1.1

# Scan multiple hosts
nmap 192.168.1.1 192.168.1.2

# Scan a subnet
nmap 192.168.1.0/24

# Scan a range
nmap 192.168.1.1-100

# Scan hosts from a file
nmap -iL targets.txt

# Exclude a host
nmap 192.168.1.0/24 --exclude 192.168.1.1

# Exclude hosts from file
nmap 192.168.1.0/24 --excludefile exclude.txt
```

### Host Discovery

```bash
# Ping scan (host discovery only)
nmap -sn 192.168.1.0/24

# No ping
nmap -Pn 192.168.1.1

# ARP discovery
nmap -PR 192.168.1.0/24

# ICMP Echo
nmap -PE 192.168.1.0/24

# ICMP Timestamp
nmap -PP 192.168.1.0/24

# ICMP Netmask
nmap -PM 192.168.1.0/24

# TCP SYN ping
nmap -PS80,443 192.168.1.0/24

# TCP ACK ping
nmap -PA80,443 192.168.1.0/24

# UDP ping
nmap -PU53 192.168.1.0/24
```

### Port Scanning

```bash
# Default top ports
nmap 192.168.1.1

# Scan all ports
nmap -p- 192.168.1.1

# Specific port
nmap -p 80 192.168.1.1

# Multiple ports
nmap -p 22,80,443 192.168.1.1

# Port range
nmap -p 1-1000 192.168.1.1

# Top 100 ports
nmap --top-ports 100 192.168.1.1

# Fast scan
nmap -F 192.168.1.1
```

### TCP Scan Types

```bash
# TCP SYN Scan (default for root)
nmap -sS 192.168.1.1

# TCP Connect Scan
nmap -sT 192.168.1.1

# TCP ACK Scan
nmap -sA 192.168.1.1

# TCP Window Scan
nmap -sW 192.168.1.1

# TCP Maimon Scan
nmap -sM 192.168.1.1

# TCP FIN Scan
nmap -sF 192.168.1.1

# TCP NULL Scan
nmap -sN 192.168.1.1

# TCP Xmas Scan
nmap -sX 192.168.1.1
```

### Service & OS Detection

```bash
# Service/version detection
nmap -sV 192.168.1.1

# Aggressive version detection
nmap -sV --version-intensity 9 192.168.1.1

# Light version detection
nmap -sV --version-light 192.168.1.1

# All probes
nmap -sV --version-all 192.168.1.1
```

### NSE Scripts

```bash
# Default scripts
nmap -sC 192.168.1.1

# Equivalent
nmap --script=default 192.168.1.1

# Run specific script
nmap --script=http-title 192.168.1.1

# Run multiple scripts
nmap --script=http-title,smb-os-discovery 192.168.1.1

# Run all scripts in category
nmap --script=vuln 192.168.1.1

# Authentication scripts
nmap --script=auth 192.168.1.1

# Discovery scripts
nmap --script=discovery 192.168.1.1

# Safe scripts
nmap --script=safe 192.168.1.1

# Malware scripts
nmap --script=malware 192.168.1.1

# Broadcast scripts
nmap --script=broadcast

# Script arguments
nmap --script http-brute --script-args userdb=users.txt
```

### Timing

```bash
# Paranoid
nmap -T0 target

# Sneaky
nmap -T1 target

# Polite
nmap -T2 target

# Normal
nmap -T3 target

# Aggressive
nmap -T4 target

# Insane
nmap -T5 target
```

### Verbose

```bash
# Verbose
nmap -v target

# More verbose
nmap -vv target

# Debugging
nmap -d target

# More debugging
nmap -d9 target

# Packet tracing
nmap --packet-trace target

# Reason for results
nmap --reason target
```

### Firewall evasion and Spoofing

```bash
# Fragment packets
nmap -f target

# More fragmentation
nmap -ff target

# Custom MTU
nmap --mtu 24 target

# Decoys
nmap -D RND:10 target

# Source IP spoofing
nmap -S 10.0.0.1 target

# Source port spoofing
nmap --source-port 53 target

# Append random data
nmap --data-length 25 target

# MAC spoofing
nmap --spoof-mac Dell target

# Bad checksum
nmap --badsum target
```

### Useful Combos

```bash
# Fast reconnaissance
nmap -T4 -F target

# Full TCP scan
nmap -p- -sV -O target

# Vulnerability scan
nmap -sV --script=vuln target

# Web server enumeration
nmap -p80,443 -sV -sC target

# SMB enumeration
nmap -p445 --script=smb-enum-shares,smb-os-discovery target

# Stealth scan
nmap -sS -Pn -T2 target

# Comprehensive assessment
nmap -p- -sS -sV -sC -O -T4 target
```

### NSE Script Categories

```bash
auth
broadcast
brute
default
discovery
dos
exploit
external
fuzzer
intrusive
malware
safe
version
vuln
```
