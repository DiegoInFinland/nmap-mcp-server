---
name: nmap-scan-skill
description: Professional network reconnaissance and port scanning. Use when you need to identify open ports, service versions, OS fingerprints among other details on a target IP or hostname. Or when the user explicitly asks for it.
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

# Conclusion

The Nmap Tool Skill is a powerful resource for conducting professional network reconnaissance and port scanning. By utilizing the various options and techniques available with Nmap, you can gather valuable information about target systems.
