---
name: nmap-scan-skill
description: Professional network reconnaissance and port scanning. Use when the user needs to scan a certain IP or DNS for open ports, service versions, OS fingerprints, networks among other details on a target IP or hostname. Or when the user explicitly asks for it. Scans can use IPv4 or IPv6.
---

# Nmap Tool Skill

The Nmap Tool Skill is designed for professional network reconnaissance and port scanning. It allows you to identify open ports, service versions, and OS fingerprints on a target IP or hostname. This skill is essential for security assessments, penetration testing, and network inventory management.

## Usage

To use the Nmap Tool Skill, simply provide a target IP address or hostname along with any specific scanning options you want to use. For example:
`nmap -sV -O  target_ip_or_hostname`  
This command will perform a service version detection and OS fingerprinting scan on the specified target.

## Options

It is important to note that all this options are optional and can be used in combination to customize your scan based on your specific needs.
For better understanding of the available options and their usage, it is recommended to refer to the Nmap documentation. See below for useful links, or use the `nmap --help` command to explore the various scanning techniques and options that can be utilized with this skill.

Some commonly used options include:

- `-O`: Enables OS detection.
- `-p`: Specify ports to scan (e.g., `-p 80,443`).
- `-A`: Enables aggressive scan options, including OS detection, version detection, script scanning, and traceroute.
- `-T4`: Sets the timing template to 4 (aggressive) for faster scanning.
- `-f`: Enables fragmentation of packets to evade firewalls.

## Nmap MCP Server Workflow

### 1. Find more information and discover live hosts on a network:

- First it is wise to find some useful information, for example, visit: https://nmap.org/book/man-port-scanning-techniques.html to understand the different scanning techniques and options available with Nmap. This will help you to understand the appropriate scanning options based on your specific needs and the target system you are assessing.
- Before performing a scan, it is recommended to find active hosts. This will help you to identify which devices are online and can be scanned further. Use `ping_scan` (IPv4) or `ping6_scan` (IPv6) to perform a ping scan on a subnet or specific IP address to discover live hosts.

### 2. Scan for open ports and services using `nmap_scan`:

- Once you have identified live hosts, you can perform a more detailed scan to identify open ports and services. This will help you to understand what services are running on the target system and potentially identify vulnerabilities. Commonly used options include:
  - `-sS <target_ip_or_hostname>`: This command performs a SYN scan to identify open ports on the target system.
  - `-p- <target_ip_or_hostname>`: This command performs a scan of all ports on the target system.

### 3. Perform deep reconnaissance and vulnerability assessment:

- After identifying open ports and services, you can perform a more comprehensive scan to gather detailed information about the target system. This may include service version detection, OS fingerprinting, and vulnerability scanning. Commonly used options include:
  - `-sV <target_ip_or_hostname>`: This command enables service version detection to identify the specific versions of services running on the target system.
  - `-O <target_ip_or_hostname>`: This command enables OS detection to determine the operating system running on the target system.
  - `-sC <target_ip_or_hostname>`: This command runs Nmap's default vulnerability scripts against the target system to identify potential vulnerabilities.

### 4. More deep scaning if needed:

- If you need to perform a more aggressive scan, you can use the `-A` option to enable aggressive scan options, which include OS detection, version detection, script scanning, and traceroute. This will provide you with a comprehensive overview of the target system and its potential vulnerabilities. The command for this would be:
  - `-A <target_ip_or_hostname>`: This command enables aggressive scan options for a comprehensive assessment of the target system.
  - `-T4 <target_ip_or_hostname>`: This command sets the timing template to 4 (aggressive) for faster scanning, which can be useful when you need to quickly gather information about a target system.
  - `--script vuln <target_ip_or_hostname>`: This command runs Nmap's vulnerability scripts against the target system to identify potential vulnerabilities.
- Always ask for permission before performing aggressive scans, as they can be intrusive and may trigger security alerts on the target system.

## Best Practices

- Use appropriate scanning options based on the level of detail you need and the potential impact on the target system.
- Consider the network environment and potential security measures in place that may affect the scan results.
- Review the Nmap documentation for additional options and best practices to optimize your scanning strategy.
- It is recommended to ask the user for confirmation before performing aggressive scans, as they can be intrusive and may trigger security alerts on the target system. Always ensure you have proper authorization before conducting any scans to avoid legal issues.

## Useful documentation and resources

It is recommended to refer to the following resources for more information and guidance on using Nmap effectively when performing network reconnaissance and port scanning:

- https://nmap.org/book/man-port-scanning-techniques.html
- https://hackertarget.com/nmap-cheatsheet-a-quick-reference-guide/
- https://github.com/ekol-x9/nmap-cheatsheet
- https://nmap.org/book/man-host-discovery.html

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

# Conclusion

The Nmap Tool Skill is a powerful resource for conducting professional network reconnaissance and port scanning. By utilizing the various options and techniques available with Nmap, you can gather valuable information about target systems.
