FROM kalilinux/kali-rolling AS python-deps

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONWARNINGS=ignore \
    UV_QUIET=1

RUN apt update && apt install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/* && apt clean

WORKDIR /app
COPY pyproject.toml uv.lock /app/
COPY src/ /app/src/
RUN uv sync --compile-bytecode --no-dev

FROM python-deps AS dev
COPY tests/ /app/tests/
RUN uv sync --group dev
ENTRYPOINT ["uv", "run", "pytest", "-v", "tests/"]

FROM python-deps AS prod
ENTRYPOINT ["uv", "run", "-q", "src/server.py"] 

