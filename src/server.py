from mcp.server.fastmcp import FastMCP 
import logging
import subprocess
import sys 
from typing import Dict, Any, List 

mcp = FastMCP('nmap-scanner')
logging.basicConfig(level=logging.WARNING, stream=sys.stderr) 
TIMEOUT = 300

# Deny list of file output flags (not needed since results are returned as JSON)
DENY_FLAGS = {
    "-oN", "-oX", "-oG", "-oS", "-oA", "--output-xml"
}

class CmdExec: 
    def __init__(self, cmd, timeout=TIMEOUT): 
        self.cmd = cmd
        self.timeout = timeout
        self.process = None
    
    def execute(self): 
        try:
            self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True)
            stdout, stderr = self.process.communicate(timeout=self.timeout)
            return {
                "stdout": stdout,
                "stderr": stderr,
                "returncode": self.process.returncode
            }
        except subprocess.TimeoutExpired:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if self.process:
                        self.process.kill()
            return {
                "stdout": "",
                "stderr": f"Nmap scan timed out after {self.timeout} seconds",
                "returncode": -1
            }

def nmap_execute(args: List[str]) -> Dict[str, Any]:
    nmap_cmd = ["nmap"] + args
    if not args or args[-1].strip() == "":
        return {"error": "No target specified for Nmap scan"}
    
    try:
        cmd_exec = CmdExec(nmap_cmd)
        return cmd_exec.execute()
    except Exception as e:
        return {"error": f"Error executing Nmap: {e}"}
    
     
def validate_ports(ports: str) -> bool:
    if not ports:
        return True
    try:
        for part in ports.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                if start < 1 or end > 65535 or start > end:
                    return False 
            else:
                port = int(part)
                if port < 1 or port > 65535:
                    return False
        return True
    except ValueError:
        return False

@mcp.tool()
def ping_scan(target: str) -> Dict[str, Any]:
    """Performs a ping scan on the specified target, returning the results as a JSON object.

    Args:
        target (str): The target to ping (e.g., IP address or hostname).
    Returns:
        Dict[str, Any]: A dictionary containing the results of the ping scan.
    """
    return nmap_execute(["-sn", "-R", "--disable-arp-ping", "-PE", target])

@mcp.tool()
def nmap_scan(target: str, flags: str="", ports: str="") -> Dict[str, Any]:
    """Executes an Nmap scan on the specified target with optional flags and ports, returning the results as a JSON object.

    Args:
        target (str): The target to scan (e.g., IP address or hostname).
        flags (str, optional): Additional Nmap flags to include in the scan. Defaults to "".
        ports (str, optional): Specific ports to scan (e.g., "80,443"). Defaults to "".

    Returns:
        Dict[str, Any]: A dictionary containing the results of the Nmap scan.
    """
    args = []
    if flags:
        flag_list = flags.split()
        # Check for dangerous flags
        for flag in flag_list:
            if flag in DENY_FLAGS:
                return {"error": f"Dangerous flag '{flag}' is not allowed"}
        args.extend(flag_list)
    if ports:
        if not validate_ports(ports):
            return {"error": "Invalid ports specified"}
        args.extend(["-p", ports])
    args.append(target)

    return nmap_execute(args) 

if __name__ == "__main__": 
    mcp.run(transport="stdio")  

    


