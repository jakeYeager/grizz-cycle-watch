#!/usr/bin/env bash
# housekeeping.sh — Run structural integrity checks and invoke the Housekeeping Agent.
#
# Usage:
#   ./scripts/housekeeping.sh             # run checks + agent
#   ./scripts/housekeeping.sh --dry-run   # print findings report only, no agent

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

DRY_RUN=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

echo "▶ Housekeeping — $(date '+%Y-%m-%d %H:%M')"
echo ""

FINDINGS=""

# ─── 1. Signal log entry count ───────────────────────────────────────────────

LOG_FILE="news/signal-log.md"
if [[ -f "$LOG_FILE" ]]; then
  ENTRY_COUNT=$(grep -c "^### " "$LOG_FILE" 2>/dev/null || echo 0)
  if [[ $ENTRY_COUNT -ge 100 ]]; then
    FINDINGS="${FINDINGS}\n[LOG ARCHIVING NEEDED]\n  news/signal-log.md has ${ENTRY_COUNT} entries (threshold: 100)\n"
  else
    echo "  Signal log: ${ENTRY_COUNT} entries (threshold: 100)"
  fi
else
  FINDINGS="${FINDINGS}\n[MISSING FILE]\n  news/signal-log.md not found\n"
fi

# ─── 2. _quarto.yml: registered files that don't exist ───────────────────────

MISSING_FILES=""
while IFS= read -r path; do
  path=$(echo "$path" | tr -d ' ')
  [[ -z "$path" ]] && continue
  [[ -f "$path" ]] || MISSING_FILES="${MISSING_FILES}    $path\n"
done < <(grep -E "^\s+- [a-z_-].*\.md" _quarto.yml | sed 's/.*- //')

if [[ -n "$MISSING_FILES" ]]; then
  FINDINGS="${FINDINGS}\n[QUARTO SIDEBAR — FILES NOT FOUND]\n${MISSING_FILES}"
else
  echo "  _quarto.yml: all registered files exist"
fi

# ─── 3. Content files not registered in _quarto.yml ─────────────────────────

UNREGISTERED=""
CONTENT_DIRS="theory market-behavior global-debt armed-conflict news-convergence news"
for dir in $CONTENT_DIRS; do
  [[ -d "$dir" ]] || continue
  for f in "$dir"/*.md; do
    [[ -f "$f" ]] || continue
    # Skip watch-list and signal-log — they're living docs, always registered
    fname="${f#./}"
    if ! grep -q "$fname" _quarto.yml 2>/dev/null; then
      UNREGISTERED="${UNREGISTERED}    $fname\n"
    fi
  done
done

if [[ -n "$UNREGISTERED" ]]; then
  FINDINGS="${FINDINGS}\n[UNREGISTERED CONTENT FILES]\n${UNREGISTERED}"
else
  echo "  Content files: all registered in _quarto.yml"
fi

# ─── 4. Frontmatter validation ───────────────────────────────────────────────

FRONTMATTER_ISSUES=""
REQUIRED_FIELDS="title date description categories"
for dir in theory market-behavior global-debt armed-conflict news-convergence news; do
  [[ -d "$dir" ]] || continue
  for f in "$dir"/*.md; do
    [[ -f "$f" ]] || continue
    # Skip living-documents — operational files, not categorized content articles
    grep -q "^status: living-document" "$f" 2>/dev/null && continue
    for field in $REQUIRED_FIELDS; do
      if ! grep -q "^${field}:" "$f" 2>/dev/null; then
        FRONTMATTER_ISSUES="${FRONTMATTER_ISSUES}    $f: missing '${field}'\n"
      fi
    done
  done
done

if [[ -n "$FRONTMATTER_ISSUES" ]]; then
  FINDINGS="${FINDINGS}\n[FRONTMATTER ISSUES]\n${FRONTMATTER_ISSUES}"
else
  echo "  Frontmatter: all required fields present"
fi

# ─── 5. Stale working-documents (>30 days since last git commit) ─────────────

STALE_DOCS=""
while IFS= read -r f; do
  last_commit=$(git log -1 --format="%ct" -- "$f" 2>/dev/null || echo "")
  if [[ -n "$last_commit" ]]; then
    now=$(date +%s)
    days_ago=$(( (now - last_commit) / 86400 ))
    if [[ $days_ago -gt 30 ]]; then
      STALE_DOCS="${STALE_DOCS}    $f (${days_ago} days since last commit)\n"
    fi
  fi
done < <(grep -rl "^status: working-document" --include="*.md" . 2>/dev/null | grep -v "\.git" | sort)

if [[ -n "$STALE_DOCS" ]]; then
  FINDINGS="${FINDINGS}\n[STALE WORKING-DOCUMENTS (>30 days)]\n${STALE_DOCS}"
else
  echo "  Working-documents: none stale"
fi

# ─── 6. Orphaned / empty directory trees ────────────────────────────────────
# A directory whose entire subtree contains no regular files is cruft — usually
# a stale Quarto <name>_files/ render artifact left behind when a source file
# was renamed or moved. A .gitkeep counts as a regular file, so a tree kept
# intentionally (e.g. assets/) is exempt automatically. Quarto build outputs
# (_site, _book, _freeze, .quarto) are excluded. In --dry-run trees are
# reported but not removed.

EMPTY_TREES=""
LAST_TREE=""
while IFS= read -r d; do
  [[ -z "$d" ]] && continue
  # skip anything nested under a tree already collected
  [[ -n "$LAST_TREE" && "$d" == "$LAST_TREE/"* ]] && continue
  if [[ -z "$(find "$d" -type f 2>/dev/null)" ]]; then
    EMPTY_TREES="${EMPTY_TREES}${d}\n"
    LAST_TREE="$d"
  fi
done < <(find . -mindepth 1 \
           \( -name .git -o -name _site -o -name _book -o -name _freeze -o -name .quarto \) -prune \
           -o -type d -print | sort)

if [[ -n "$EMPTY_TREES" ]]; then
  TREE_REPORT=""
  while IFS= read -r d; do
    [[ -z "$d" ]] && continue
    if ! $DRY_RUN && [[ -d "$d" ]]; then
      rm -rf "$d"
    fi
    TREE_REPORT="${TREE_REPORT}    ${d}\n"
  done < <(printf '%b' "$EMPTY_TREES")
  if $DRY_RUN; then
    FINDINGS="${FINDINGS}\n[EMPTY DIRECTORY TREES — would prune]\n${TREE_REPORT}"
  else
    FINDINGS="${FINDINGS}\n[EMPTY DIRECTORY TREES — pruned]\n${TREE_REPORT}"
  fi
else
  echo "  Directory trees: no empty/orphaned trees found"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────

echo ""
if [[ -z "$FINDINGS" ]]; then
  echo "  Pre-flight: all checks passed — no issues found"
  if $DRY_RUN; then exit 0; fi
  echo "  Running agent for internal link validation..."
  echo ""
else
  echo "  Pre-flight findings:"
  echo -e "$FINDINGS"
fi

if $DRY_RUN; then
  echo "(dry-run: skipping agent invocation)"
  exit 0
fi

# ─── Agent invocation ─────────────────────────────────────────────────────────

# Strip YAML frontmatter before passing to claude -p (frontmatter starts with ---
# which the claude CLI argument parser mistakes for a flag)
AGENT_SPEC=$(awk 'BEGIN{n=0} /^---/{n++; next} n>=2{print}' "$REPO/.claude/agents/housekeeping.md")

PREFLIGHT_REPORT="Pre-flight findings from housekeeping.sh:"
if [[ -z "$FINDINGS" ]]; then
  PREFLIGHT_REPORT="${PREFLIGHT_REPORT}\n  All script checks passed. No issues detected by pre-flight."
else
  PREFLIGHT_REPORT="${PREFLIGHT_REPORT}\n${FINDINGS}"
fi

claude -p "$AGENT_SPEC

$PREFLIGHT_REPORT

Work through the findings above, then run internal link validation across all content files." \
  --allowedTools "Read,Edit,Glob,Grep"
