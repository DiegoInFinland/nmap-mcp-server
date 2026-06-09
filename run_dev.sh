#!/bin/sh
# Run the nmap tool in a Docker container, mounting the current directory's src folder to /src.
# Since the volume mount hides the image's .venv, we run uv sync at startup.
# It should be used for development purposes only.
docker run --rm -it \
  -v $(pwd)/src:/src \
  --entrypoint sh \
  nmap-mcp-server \
  -c "uv sync --no-dev && exec /src/.venv/bin/python server.py"   
  