# Publish Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One command that publishes an Obsidian draft to Jekyll — copies assets, rewrites embeds, moves to `_posts/` — and a newsletter fix so file-referenced SVGs get converted to PNG in emails.

**Architecture:** A new `publish.sh` script replaces the manual workflow. It calls a rewritten `convert_obsidian.py` (scoped to drafts) for embed rewriting + asset copying, then moves the post. `newsletter/send.js` gets a second conversion pass for `<img src="...svg">` tags.

**Tech Stack:** Python 3 (convert), Bash (publish), Node.js/sharp (newsletter SVG→PNG)

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `publish.sh` | **Create** | Single entry point: picks draft, runs convert, moves to `_posts/`, stages git |
| `convert_obsidian.py` | **Modify** | Rewrite to: scan `_drafts/` for embeds, search Obsidian `assets/svg/` and `assets/images/` for source files, copy to `assets/images/`, rewrite `![[]]` → `![alt](/assets/images/)` |
| `newsletter/send.js` | **Modify** | Add handler for `<img src="...svg">`: read SVG from disk, convert via sharp, save PNG to `assets/email/`, replace src |

---

### Task 1: Rewrite `convert_obsidian.py` to handle drafts and asset resolution

**Files:**
- Modify: `convert_obsidian.py` (full rewrite of `convert_obsidian_embeds` function and `main`)

The current script searches for `*.md` in the Obsidian root and uses `rglob` from the file's parent dir. This doesn't work because:
1. Drafts are in `Xitnode/drafts/` (symlink to `_drafts/`), not the Obsidian root
2. `rglob` from `_drafts/` never finds files in `Xitnode/assets/svg/` or `Xitnode/assets/images/`

The rewrite makes the script work on a single draft file, searching the correct Obsidian asset directories.

- [ ] **Step 1: Rewrite `convert_obsidian.py`**

Replace the entire file with:

```python
#!/usr/bin/env python3
"""
Convert Obsidian embeds in a draft to Jekyll markdown and copy assets.
Usage: python convert_obsidian.py <draft-file.md> [--dry-run]
"""

import os
import re
import shutil
import sys
from pathlib import Path

# Project root (where this script lives)
PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DEST = PROJECT_ROOT / "assets" / "images"

# Obsidian asset source directories
OBSIDIAN_ROOT = Path(
    os.environ.get(
        "OBSIDIAN_ROOT",
        os.path.expanduser("~/dev/Projects/obsidian/Obsidian Vault/Xitnode"),
    )
)
OBSIDIAN_ASSET_DIRS = [
    OBSIDIAN_ROOT / "assets" / "svg",
    OBSIDIAN_ROOT / "assets" / "images",
]

IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


def find_asset(filename):
    """Search Obsidian asset directories for a file."""
    for asset_dir in OBSIDIAN_ASSET_DIRS:
        candidate = asset_dir / filename
        if candidate.exists():
            return candidate
    return None


def convert_embeds(content, dry_run=False):
    """Convert ![[file]] embeds to ![alt](/assets/images/file) and copy assets."""
    copied = []
    missing = []

    def replace_embed(match):
        raw_name = match.group(1)
        # Strip .excalidraw suffix if present
        clean_name = re.sub(r"\.excalidraw(\.\w+)$", r"\1", raw_name)
        ext = Path(clean_name).suffix.lower()

        if ext not in IMAGE_EXTENSIONS:
            return match.group(0)

        source = find_asset(raw_name) or find_asset(clean_name)

        if source is None:
            missing.append(raw_name)
            print(f"  WARNING: asset not found: {raw_name}")
            # Still convert the syntax so Jekyll doesn't break
        elif not dry_run:
            dest = ASSETS_DEST / clean_name
            ASSETS_DEST.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(source, dest)
                copied.append(clean_name)
                print(f"  Copied: {raw_name} -> assets/images/{clean_name}")
            else:
                print(f"  Up to date: assets/images/{clean_name}")
        else:
            print(f"  Would copy: {raw_name} -> assets/images/{clean_name}")

        alt_text = Path(clean_name).stem.replace("_", " ").replace("-", " ").title()
        return f"![{alt_text}](/assets/images/{clean_name})"

    converted = re.sub(r"!\[\[([^\]]+)\]\]", replace_embed, content)
    return converted, copied, missing


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_obsidian.py <draft-file.md> [--dry-run]")
        sys.exit(1)

    draft_path = Path(sys.argv[1]).resolve()
    dry_run = "--dry-run" in sys.argv

    if not draft_path.exists():
        print(f"File not found: {draft_path}")
        sys.exit(1)

    print(f"Processing: {draft_path.name}")

    content = draft_path.read_text(encoding="utf-8")
    converted, copied, missing = convert_embeds(content, dry_run=dry_run)

    if converted != content and not dry_run:
        draft_path.write_text(converted, encoding="utf-8")
        print(f"Rewrote embeds in {draft_path.name}")
    elif converted == content:
        print("No embeds to convert.")

    if missing:
        print(f"\nWARNING: {len(missing)} asset(s) not found:")
        for m in missing:
            print(f"  - {m}")

    if dry_run:
        print("\nDry run complete. No files modified.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with dry run on the existing draft**

Run: `cd /Users/stefanodellapietra/dev/Projects/xitnode && python convert_obsidian.py _drafts/2026-04-06-dove-si-chiude-il-loop.md --dry-run`

Expected: Script runs, reports "No embeds to convert." (this draft has no `![[]]` embeds), exits cleanly.

- [ ] **Step 3: Test with a synthetic embed**

Create a temporary test:
```bash
echo '![[test.svg]]' > /tmp/test-embed.md
cd /Users/stefanodellapietra/dev/Projects/xitnode && python convert_obsidian.py /tmp/test-embed.md --dry-run
```

Expected: Reports "WARNING: asset not found: test.svg" and shows the converted markdown syntax.

- [ ] **Step 4: Commit**

```bash
git add convert_obsidian.py
git commit -m "refactor: rewrite convert_obsidian.py for draft-based asset pipeline"
```

---

### Task 2: Create `publish.sh` — single publish command

**Files:**
- Create: `publish.sh`

This script is the one command you run to publish. It:
1. Lists drafts and lets you pick one (or accepts a filename argument)
2. Runs `convert_obsidian.py` to handle embeds + copy assets
3. Moves the draft from `_drafts/` to `_posts/`

- [ ] **Step 1: Create `publish.sh`**

```bash
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
```

- [ ] **Step 2: Make executable**

```bash
chmod +x /Users/stefanodellapietra/dev/Projects/xitnode/publish.sh
```

- [ ] **Step 3: Test dry run (read the output, don't actually publish the real draft)**

```bash
cd /Users/stefanodellapietra/dev/Projects/xitnode
# Just verify the script parses and lists drafts
bash -x publish.sh nonexistent.md 2>&1 | head -20
```

Expected: "Draft not found" error — confirms the script runs and path logic works.

- [ ] **Step 4: Commit**

```bash
git add publish.sh
git commit -m "feat: add publish.sh — single command to publish drafts"
```

---

### Task 3: Fix `newsletter/send.js` — handle file-referenced SVGs

**Files:**
- Modify: `newsletter/send.js:101-144` (the `convertSvgsForEmail` function)

The current function only matches inline `<svg>` tags. After `marked` renders `![alt](/assets/images/file.svg)` to `<img src="/assets/images/file.svg">`, the SVG regex doesn't match. We need a second pass that:
1. Finds `<img src="...svg">` tags
2. Reads the SVG file from disk (`assets/images/`)
3. Converts to PNG via sharp
4. Saves to `assets/email/`
5. Replaces the src with the PNG URL

- [ ] **Step 1: Add `convertSvgImgsForEmail` function after the existing `convertSvgsForEmail` function**

Add this new function at line 145 (after `convertSvgsForEmail` closes):

```javascript
async function convertSvgImgsForEmail(html, postUrl) {
  fs.mkdirSync(EMAIL_ASSETS_DIR, { recursive: true });

  const imgRegex = /<img\s+src="(\/assets\/images\/[^"]+\.svg)"[^>]*>/gi;
  const matches = [...html.matchAll(imgRegex)];

  if (matches.length === 0) return { html, generatedFiles: [] };

  const generatedFiles = [];

  for (let i = 0; i < matches.length; i++) {
    const imgTag = matches[i][0];
    const svgPath = matches[i][1]; // e.g. /assets/images/diagram.svg
    const localPath = path.join(__dirname, "..", svgPath);

    if (!fs.existsSync(localPath)) {
      console.warn(`  SVG file not found: ${localPath}, using fallback link`);
      const fallback = `<p style="padding:16px;background:#f5f5f5;border:1px solid #ddd;border-radius:4px;text-align:center;color:#666;font-size:14px;">[Diagramma — <a href="${postUrl}" style="color:#007acc;">vedi sul sito</a>]</p>`;
      html = html.replace(imgTag, fallback);
      continue;
    }

    const svgContent = fs.readFileSync(localPath, "utf-8");
    const hash = crypto.createHash("md5").update(svgContent).digest("hex").slice(0, 10);
    const filename = `diagram-${hash}.png`;
    const filepath = path.join(EMAIL_ASSETS_DIR, filename);

    try {
      const pngBuffer = await sharp(Buffer.from(svgContent))
        .png()
        .resize({ width: 1080, withoutEnlargement: true })
        .toBuffer();

      fs.writeFileSync(filepath, pngBuffer);
      generatedFiles.push(filepath);

      const imgUrl = `${SITE_URL}/assets/email/${filename}`;
      const newImgTag = `<img src="${imgUrl}" alt="Diagramma" style="max-width:100%;height:auto;border:1px solid #eee;border-radius:4px;" />`;
      html = html.replace(imgTag, newImgTag);

      console.log(`  SVG img ${i + 1}/${matches.length} → ${filename} (${(pngBuffer.length / 1024).toFixed(1)}KB)`);
    } catch (err) {
      console.warn(`  SVG img ${i + 1}/${matches.length} conversion failed:`, err.message);
      const fallback = `<p style="padding:16px;background:#f5f5f5;border:1px solid #ddd;border-radius:4px;text-align:center;color:#666;font-size:14px;">[Diagramma — <a href="${postUrl}" style="color:#007acc;">vedi sul sito</a>]</p>`;
      html = html.replace(imgTag, fallback);
    }
  }

  return { html, generatedFiles };
}
```

- [ ] **Step 2: Update `renderEmail` to call both conversion functions**

In `renderEmail` (line 146-155), change:

```javascript
const { html: content, generatedFiles } = await convertSvgsForEmail(post.content, post.postUrl);
```

to:

```javascript
const { html: inlineConverted, generatedFiles: inlineFiles } = await convertSvgsForEmail(post.content, post.postUrl);
const { html: content, generatedFiles: imgFiles } = await convertSvgImgsForEmail(inlineConverted, post.postUrl);
const generatedFiles = [...inlineFiles, ...imgFiles];
```

- [ ] **Step 3: Test with dry run on the latest post (which has file-referenced SVGs)**

```bash
cd /Users/stefanodellapietra/dev/Projects/xitnode/newsletter
npm install
node send.js --slug non-stai-facendo-bi --dry-run
```

Expected output should show:
```
SVG img 1/3 → diagram-HASH.png (XXX.XKB)
SVG img 2/3 → diagram-HASH.png (XXX.XKB)
SVG img 3/3 → diagram-HASH.png (XXX.XKB)
Generated 3 PNG(s) in assets/email/
```

Verify PNGs were created:
```bash
ls -la ../assets/email/
```

- [ ] **Step 4: Commit**

```bash
git add newsletter/send.js
git commit -m "fix: convert file-referenced SVGs to PNG in newsletter emails"
```

---

### Task 4: End-to-end test with a real draft

**Files:** No new files — integration test of the full pipeline.

- [ ] **Step 1: Create a test SVG in Obsidian assets**

```bash
cat > "/Users/stefanodellapietra/dev/Projects/obsidian/Obsidian Vault/Xitnode/assets/svg/test-pipeline.svg" << 'EOF'
<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg" style="font-family:system-ui,sans-serif">
  <rect width="200" height="100" fill="#f5f5f5" stroke="#333" rx="8"/>
  <text x="100" y="55" text-anchor="middle" font-size="16" fill="#333">Pipeline Test</text>
</svg>
EOF
```

- [ ] **Step 2: Create a test draft with an Obsidian embed**

```bash
cat > "/Users/stefanodellapietra/dev/Projects/xitnode/_drafts/2026-04-07-test-pipeline.md" << 'EOF'
---
layout: post
title: "Test Pipeline"
date: 2026-04-07
categories: [xitnode]
tags: [test]
---

Test post with SVG embed:

![[test-pipeline.svg]]

End of test.
EOF
```

- [ ] **Step 3: Run publish.sh on the test draft**

```bash
cd /Users/stefanodellapietra/dev/Projects/xitnode
./publish.sh 2026-04-07-test-pipeline.md
```

Expected:
- `test-pipeline.svg` copied to `assets/images/test-pipeline.svg`
- Embed rewritten to `![Test Pipeline](/assets/images/test-pipeline.svg)`
- File moved to `_posts/2026-04-07-test-pipeline.md`

Verify:
```bash
grep "assets/images/test-pipeline.svg" _posts/2026-04-07-test-pipeline.md
ls assets/images/test-pipeline.svg
```

- [ ] **Step 4: Run newsletter dry run on the test post**

```bash
cd newsletter && node send.js --slug test-pipeline --dry-run
```

Expected: SVG img converted to PNG, dry run output shows the conversion.

- [ ] **Step 5: Clean up test artifacts**

```bash
cd /Users/stefanodellapietra/dev/Projects/xitnode
rm _posts/2026-04-07-test-pipeline.md
rm assets/images/test-pipeline.svg
rm -f assets/email/diagram-*.png  # only new test ones — check hash first
rm "/Users/stefanodellapietra/dev/Projects/obsidian/Obsidian Vault/Xitnode/assets/svg/test-pipeline.svg"
```

- [ ] **Step 6: Final commit of any remaining changes**

```bash
git add -A
git diff --staged --quiet || git commit -m "chore: pipeline integration verified"
```
