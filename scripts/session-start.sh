#!/bin/bash
# Installs the screenshot tool (Playwright) at the start of cloud sessions,
# so web-builder and critique can check sites visually.
set -euo pipefail

# Only run in Claude Code on the web / cloud sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}"

if [ ! -d node_modules/playwright ]; then
  npm install --no-audit --no-fund --loglevel=error
fi
