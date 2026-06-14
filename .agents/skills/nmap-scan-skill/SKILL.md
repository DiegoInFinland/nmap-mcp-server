---
name: nmap-scan-skill
description: Professional network reconnaissance and port scanning. Use when the user needs to scan a certain IP or DNS for open ports, service versions, OS fingerprints, networks among other details on a target IP or hostname. Or when the user explicitly asks for it. Scans can use IPv4 or IPv6.
---

# Nmap MCP Operational Workflow

## 1. Discovery (The "Find" Step)

- Use the `ping_scan` tool (for IPv4) or `ping6_scan` (for IPv6) to identify live hosts in a subnet.
- **Rule:** Do not perform deep scans on IP ranges until live hosts are confirmed.

## 2. Port & Service Scanning

- Use the `nmap_scan` tool for all primary reconnaissance.
- **Standard Scan:** Pass `-sS -sC -sV` to `nmap_scan` for a balance of speed and detail.
- **Full Range:** Use `-p-` if the user requires a comprehensive port audit.

## 3. Advanced & Vulnerability Recon

- Use `nmap_scan` with the `--script vuln` flag for vulnerability assessments.
- **Aggressive Mode:** Use `-A` for OS detection and traceroute.
- **Constraint:** You **must** ask for user confirmation before passing `-A`, `-T4`, or `--script vuln` to the `nmap_scan` tool.

# Safety & Reporting

- **Timing:** Default to `-T3` within the tool arguments to prevent network instability.
- **Next Steps:** After `nmap_scan` completes, analyze the output and ask the user if they want to target specific open ports with specialized NSE scripts.
