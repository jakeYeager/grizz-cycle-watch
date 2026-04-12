#!/usr/bin/env bash
# monitor.sh — Run a Signal Monitor pass against the watch list.
#
# Usage:
#   ./scripts/monitor.sh              # standard pass (last 24–48hrs)
#   ./scripts/monitor.sh --since 72h  # extend lookback window
#   ./scripts/monitor.sh --section "Armed Conflict"  # single section only
#
# The agent reads the watch list, searches for recent signals, and appends
# any relevant entries to news/log.md. Prints a summary when done.

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

echo "▶ Signal Monitor — $(date '+%Y-%m-%d %H:%M')"
echo "  Lookback: $SINCE | Scope: $SECTION"
echo ""

claude -p "Read .claude/agent-brief.md for project orientation and search query patterns.
Read news/log.md to see what has already been logged — do not duplicate entries from the last 48 hours.

Run a monitoring pass covering: $SECTION
Lookback window: $SINCE

For each section in scope, run 2–3 targeted web searches using the query patterns in the agent brief. Vary the phrasing across searches.

For each result that clearly advances a specific watch list indicator:
- Append a formatted log entry to news/log.md
- Use today's date heading (## YYYY-MM-DD); create it if it does not exist yet
- Follow the entry format exactly as defined in .claude/rules/signal-monitoring.md

Prioritize cross-cutting signals — events that move indicators across multiple sections.

After all searches are complete, print a summary:
- Sections covered
- Number of searches run
- Number of entries logged
- Whether any immediate escalation triggers were hit (and which ones)" \
  --allowedTools "WebSearch,Read,Edit"
