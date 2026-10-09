# Nmap MCP Server

## What This Is

- Single Python MCP stdio server in `src/server.py`; it registers `FastMCP('nmap-scanner')` tools for `local_ip`, `ping_scan`, `ping6_scan`, `nmap_scan`, and `curl_request`.
- Runtime image is Kali Linux (`kalilinux/kali-rolling`) with `nmap`, `curl`, and `uv`; production entrypoint is `uv run -q src/server.py`.

## Commands

- Install local dependencies: `uv sync`.
- Run server directly: `uv run src/server.py`.
- Build prod image: `docker build -t nmap-mcp-server .`.
- Run prod MCP server: `docker run --rm --network host -i nmap-mcp-server`.
- Run dev server with source mounted: `./run_dev.sh`; it runs `uv sync --no-dev` inside the container because the bind mount hides the image `.venv`.
- Run full tests locally: `uv run pytest -v tests/`.
- Run one test file or test: `uv run pytest -v tests/test_server.py` or `uv run pytest -v tests/test_server.py::test_name`.
- Run tests in Docker: `docker build --target dev -t nmap-mcp-server-dev .` then `docker run --rm nmap-mcp-server-dev`.

## Code Constraints

- Dependencies are only in `pyproject.toml`; keep `uv.lock` in sync after dependency changes.
- Tests import `server` via `tests/conftest.py`, which prepends `src/` to `sys.path`; do not convert imports blindly without updating tests.
- Command execution must stay list-based with `shell=False`; user-provided Nmap flags are currently whitespace-split before execution.
- Preserve scan safety checks in `nmap_scan`: `DENY_FLAGS` blocks file output flags and `validate_ports` allows only ports/ranges within `1-65535`.
- `ping_scan` intentionally uses `-sn -R --disable-arp-ping -PE`; `ping6_scan` intentionally uses `-6 -sn -R`.

## Operational Gotchas

- The MCP transport is stdio; logs go to stderr and should stay quiet enough not to corrupt protocol output.
- Docker examples use `--network host`; on macOS/Windows this can still reflect Docker VM networking, not the host LAN. Ask for an explicit authorized target/subnet before broad scans.
- Repo-local scan guidance lives in `.agents/skills/nmap-scan-skill/SKILL.md`; it requires pausing after discovery before targeted port/service scans.
