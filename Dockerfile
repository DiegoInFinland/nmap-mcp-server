FROM kalilinux/kali-rolling AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Clean up ENV: Remove redundant compile flags and set the path
ENV UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONWARNINGS=ignore \
    UV_QUIET=1

RUN apt update && apt install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/* && apt clean

WORKDIR /src
COPY ./src /src

# 1. Sync and compile everything NOW so nothing happens at runtime
RUN uv sync --compile-bytecode --no-dev

# 2. Use the virtualenv's python directly to avoid 'uv run' noise
ENTRYPOINT ["uv", "run", "-q", "server.py"]

FROM base AS dev
RUN uv sync --group dev
ENTRYPOINT ["uv", "run", "pytest", "-v"]
