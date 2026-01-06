#!/bin/bash
cd "$(dirname "$0")/.."

# Run pi-nocchio using uv
uv run python -m pinocchio
