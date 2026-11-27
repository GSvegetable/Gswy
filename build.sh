#!/usr/bin/env bash
# Gswy Serif 一键构建：UFO + TTF + OTF + WOFF2
set -euo pipefail
cd "$(dirname "$0")"
python3 -m sources.gswy.build
