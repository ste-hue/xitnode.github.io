#!/bin/bash
# Publish an Obsidian draft to _posts/
# Usage: ./publish.sh [draft-filename.md]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRAFTS_DIR="$SCRIPT_DIR/_drafts"
POSTS_DIR="$SCRIPT_DIR/_posts"

# Pick draft
if [ -n "$1" ]; then
  DRAFT="$DRAFTS_DIR/$1"
else
  # List available drafts
  DRAFTS=($(ls "$DRAFTS_DIR"/*.md 2>/dev/null | xargs -I{} basename {}))
  if [ ${#DRAFTS[@]} -eq 0 ]; then
    echo "No drafts found in _drafts/"
    exit 1
  fi

  echo "Available drafts:"
  for i in "${!DRAFTS[@]}"; do
    echo "  $((i+1)). ${DRAFTS[$i]}"
  done

  read -p "Pick a draft [1-${#DRAFTS[@]}]: " CHOICE
  if [ -z "$CHOICE" ] || [ "$CHOICE" -lt 1 ] || [ "$CHOICE" -gt ${#DRAFTS[@]} ]; then
    echo "Invalid choice."
    exit 1
  fi

  DRAFT="$DRAFTS_DIR/${DRAFTS[$((CHOICE-1))]}"
fi

if [ ! -f "$DRAFT" ]; then
  echo "Draft not found: $DRAFT"
  exit 1
fi

BASENAME=$(basename "$DRAFT")
echo "Publishing: $BASENAME"

# Convert Obsidian embeds and copy assets
python3 "$SCRIPT_DIR/convert_obsidian.py" "$DRAFT"

# Move to _posts
mkdir -p "$POSTS_DIR"
mv "$DRAFT" "$POSTS_DIR/$BASENAME"
echo "Moved to _posts/$BASENAME"

# Stage changes
cd "$SCRIPT_DIR"
git add "_posts/$BASENAME" assets/images/
echo ""
echo "Done. Review and push:"
echo "  git status"
echo "  git commit -m 'publish: $BASENAME'"
echo "  git push"
