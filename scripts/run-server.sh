#!/bin/bash
cd "$(dirname "$0")/.."
export PYTHONPATH=src
exec uv run council_of_translation
