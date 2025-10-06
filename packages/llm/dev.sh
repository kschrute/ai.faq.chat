#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
