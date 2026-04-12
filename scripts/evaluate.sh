#!/usr/bin/env bash
# evaluate.sh — Evaluate a single article for signal log inclusion.
#
# Usage:
#   ./scripts/evaluate.sh <url>
#   ./scripts/evaluate.sh <url> --write   # append to log if relevant
#
# Without --write, prints the evaluation to stdout only.
# With --write, appends a log entry to news/signal-log.md if the article is relevant.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: evaluate.sh <url> [--write]" >&2
  exit 1
fi

WRITE=false
if [[ "${2:-}" == "--write" ]]; then
  WRITE=true
fi

WRITE_INSTRUCTION=""
if $WRITE; then
  WRITE_INSTRUCTION="If the article is relevant, append the formatted log entry to news/signal-log.md using today's date heading (## YYYY-MM-DD). Create the heading if it does not exist."
else
  WRITE_INSTRUCTION="Do not write to any files. Print the evaluation and, if relevant, the formatted log entry to stdout only."
fi

AGENT_SPEC=$(cat "$REPO/.claude/agents/signal-monitor.md")

echo "▶ Evaluating: $URL"
echo ""

claude -p "$AGENT_SPEC

Evaluate a single article rather than running a broad search pass.

Fetch and read this article: $URL

Answer in this order:

1. RELEVANT: yes / no
2. INDICATORS MOVED: which specific watch list indicators does this advance (exact language from news/watch-list.md)
3. SECTIONS: which project sections are affected
4. ESCALATION: does this hit any immediate escalation trigger from the decision tree? (list which ones, or 'none')
5. LOG ENTRY: if relevant, the complete formatted entry ready for news/signal-log.md
6. REASONING: 2–3 sentences on why this clears or fails the relevance threshold

$WRITE_INSTRUCTION" \
  --allowedTools "WebFetch,Read$(if $WRITE; then echo ',Edit'; fi)"
