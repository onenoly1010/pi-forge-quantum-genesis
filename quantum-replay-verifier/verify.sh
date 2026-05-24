#!/usr/bin/env bash
set -euo pipefail

node scripts/generate_fixtures.js
node src/verify.js
