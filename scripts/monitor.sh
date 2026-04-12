#!/usr/bin/env bash
# monitor.sh — Run a Signal Monitor pass against the watch list.
#
# Usage:
#   ./scripts/monitor.sh              # standard pass (last 24–48hrs)
#   ./scripts/monitor.sh --since 72h  # extend lookback window
#   ./scripts/monitor.sh --section "Armed Conflict"  # single section only

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

SINCE="24-48 hours"
SECTION="all sections"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    --section) SECTION="$2"; shift 2 ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

AGENT_SPEC=$(awk 'BEGIN{n=0} /^---/{n++; next} n>=2{print}' "$REPO/.claude/agents/signal-monitor.md")

echo "▶ Signal Monitor — $(date '+%Y-%m-%d %H:%M')"
echo "  Lookback: $SINCE | Scope: $SECTION"
echo ""

claude -p "$AGENT_SPEC

Run a monitoring pass covering: $SECTION
Lookback window: $SINCE" \
  --allowedTools "WebSearch,Read,Edit"
