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
