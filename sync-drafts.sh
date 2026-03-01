#!/bin/bash
# Sync Obsidian drafts → repo _drafts/
# Copies files from Obsidian Vault/Xitnode/drafts/ into _drafts/
# Then commits and pushes. GitHub Action handles date-based publishing.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRAFTS_DIR="$SCRIPT_DIR/_drafts"
OBSIDIAN_DRAFTS="${OBSIDIAN_ROOT:-$HOME/dev/Projects/obsidian/Obsidian Vault/Xitnode/drafts}"

if [ ! -d "$OBSIDIAN_DRAFTS" ]; then
  echo "❌ Obsidian drafts not found: $OBSIDIAN_DRAFTS"
  exit 1
fi

mkdir -p "$DRAFTS_DIR"

COUNT=0
for f in "$OBSIDIAN_DRAFTS"/*.md; do
  [ -f "$f" ] || continue
  BASENAME=$(basename "$f")
  cp "$f" "$DRAFTS_DIR/$BASENAME"
  echo "📝 $BASENAME"
  COUNT=$((COUNT + 1))
done

if [ "$COUNT" -eq 0 ]; then
  echo "Nessun draft da sincronizzare."
  exit 0
fi

echo "✅ $COUNT drafts sincronizzati in _drafts/"

cd "$SCRIPT_DIR"
git add _drafts/
if ! git diff --staged --quiet; then
  git commit -m "Sync drafts from Obsidian ($COUNT files)"
  git push origin main
  echo "🚀 Push completato"
else
  echo "Nessuna modifica da committare."
fi
