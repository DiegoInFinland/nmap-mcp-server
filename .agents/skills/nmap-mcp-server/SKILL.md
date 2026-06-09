---
name: nmap-mcp-server
description: Professional network reconnaissance and port scanning. Use when you need to identify open ports, service versions, OS fingerprints among other details on a target IP or hostname.
---

# Nmap Tool Skill

The Nmap Tool Skill is designed for professional network reconnaissance and port scanning. It allows you to identify open ports, service versions, and OS fingerprints on a target IP or hostname. This skill is essential for security assessments, penetration testing, and network inventory management.

## Usage

To use the Nmap Tool Skill, simply provide a target IP address or hostname along with any specific scanning options you want to use. For example:
`nmap -sV -O  target_ip_or_hostname`  
This command will perform a service version detection and OS fingerprinting scan on the specified target.

## Options

It is important to note that all this options are optional and can be used in combination to customize your scan based on your specific needs.
For better understanding of the available options and their usage, it is recommended to refer to the Nmap documentation in Useful documentation and resources or use the `nmap --help` command to explore the various scanning techniques and options that can be utilized with this skill.

Some commonly used options include:

- `-sV`: Enables service version detection.
- `-O`: Enables OS detection.
- `-p`: Specify ports to scan (e.g., `-p 80,443`).
- `-A`: Enables aggressive scan options, including OS detection, version detection, script scanning, and traceroute.
- `-T4`: Sets the timing template to 4 (aggressive) for faster scanning.

## Best Practices

- Use appropriate scanning options based on the level of detail you need and the potential impact on the target system.
- Consider the network environment and potential security measures in place that may affect the scan results.
- Review the Nmap documentation for additional options and best practices to optimize your scanning strategy.

## Useful documentation and resources

It is recommended to refer to the following resources for more information and guidance on using Nmap effectively when performing network reconnaissance and port scanning:

- https://nmap.org/book/man-port-scanning-techniques.html
- https://hackertarget.com/nmap-cheatsheet-a-quick-reference-guide/
- https://github.com/ekol-x9/nmap-cheatsheet
- https://nmap.org/book/man-host-discovery.html

# Conclusion

The Nmap Tool Skill is a powerful resource for conducting professional network reconnaissance and port scanning. By utilizing the various options and techniques available with Nmap, you can gather valuable information about target systems.
