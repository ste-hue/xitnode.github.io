#!/usr/bin/env python3
"""
Automated Obsidian to Jekyll Posts Converter
Converts all .md files from Obsidian vault to Jekyll _posts format
"""

import os
import glob
import re
import shutil
from datetime import datetime, timedelta
import argparse
import sys
from pathlib import Path

# Configuration
JEKYLL_POSTS_DIR = "_posts"
DEFAULT_CATEGORIES = ["xitnode"]
DEFAULT_TAGS = ["xitnode", "ossessione"]


def find_obsidian_root(cli_arg=None):
    """Find Obsidian vault root directory with intelligent path resolution"""
    # 1) CLI flag wins
    if cli_arg:
        p = Path(cli_arg).expanduser()
        if p.exists():
            return p
        print(f"❌ Provided --obsidian-path not found: {p}", file=sys.stderr)
        sys.exit(1)

    # 2) ENV wins next
    env = os.environ.get("OBSIDIAN_ROOT")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p

    # 3) Common candidates (Documents + iCloud Drive)
    candidates = [
        "~/Documents/Obsidian Vault/Xitnode",
        "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Obsidian Vault/Xitnode",
        "~/iCloud Drive/Documents/Obsidian Vault/Xitnode",  # alcuni mac mostrano così
    ]
    for c in candidates:
        p = Path(c).expanduser()
        if p.exists():
            return p

    print("❌ Obsidian directory not found in any known location.", file=sys.stderr)
    print("   Searched paths:", file=sys.stderr)
    for c in candidates:
        print(f"   - {Path(c).expanduser()}", file=sys.stderr)
    sys.exit(1)


def fix_apostrophes(title):
    """Fix common Italian apostrophe patterns"""
    apostrophe_fixes = {
        # Common Italian contractions
        r"\bL\s+([AEIOU])\w+": r"L'\1",  # L + vowel -> L'
        r"\bDell\s+([AEIOU])\w+": r"dell'\1",  # Dell + vowel -> dell'
        r"\bNell\s+([AEIOU])\w+": r"nell'\1",  # Nell + vowel -> nell'
        r"\bSull\s+([AEIOU])\w+": r"sull'\1",  # Sull + vowel -> sull'
        r"\bAll\s+([AEIOU])\w+": r"all'\1",  # All + vowel -> all'
        # Specific common cases
        r"\bL\s+Italia\b": "L'Italia",
        r"\bL\s+Inganno\b": "L'Inganno",
        r"\bL\s+([aeiou])\w*": r"l'\1",  # lowercase l + vowel
        r"\bDell\s+([aeiou])\w*": r"dell'\1",
        r"\bNell\s+([aeiou])\w*": r"nell'\1",
    }

    import re

    fixed_title = title
    for pattern, replacement in apostrophe_fixes.items():
        fixed_title = re.sub(pattern, replacement, fixed_title, flags=re.IGNORECASE)

    return fixed_title


def extract_clean_title(filename):
    """Extract clean title from filename, removing date prefix if present"""
    import re

    # Remove .md extension
    title = filename.replace(".md", "")

    # Check if filename starts with date pattern (YYYY-MM-DD-)
    date_pattern = r"^\d{4}-\d{2}-\d{2}-"
    if re.match(date_pattern, title):
        # Remove the date prefix
        title = re.sub(date_pattern, "", title)
        # Convert dashes back to spaces and clean up
        title = title.replace("-", " ").strip()
        # Capitalize first letter of each word
        title = " ".join(word.capitalize() for word in title.split())
        # Fix apostrophes
        title = fix_apostrophes(title)

    return title


def sanitize_title(title):
    """Convert title to URL-safe slug"""
    return (
        title.replace(
            """, "")
        .replace(""",
            "",
        )
        .replace("'", "")
        .replace("'", "")
        .replace(",", "")
        .replace("–", "-")
        .replace("—", "-")
        .replace(".", "")
        .replace(":", "")
        .replace(";", "")
        .replace("?", "")
        .replace("!", "")
        .replace("(", "")
        .replace(")", "")
        .replace("[", "")
        .replace("]", "")
        .replace("{", "")
        .replace("}", "")
        .replace("/", "-")
        .replace("\\", "-")
        .replace(" ", "-")
        .replace("--", "-")
        .replace("---", "-")
        .strip("-")
        .lower()
    )


def is_already_converted(obsidian_file, target_dir):
    """Check if an Obsidian file has already been converted to Jekyll format"""
    filename = os.path.basename(obsidian_file)
    clean_title = extract_clean_title(filename)
    safe_title = sanitize_title(clean_title)

    # Check if any file in target directory matches this title
    if not os.path.exists(target_dir):
        return False

    pattern = os.path.join(target_dir, f"*-{safe_title}.md")
    existing_files = glob.glob(pattern)

    return len(existing_files) > 0


def get_obsidian_files(obsidian_root, target_dir=None, skip_converted=False):
    """Get all .md files from Obsidian directory"""
    if not obsidian_root.exists():
        print(f"❌ Obsidian directory not found: {obsidian_root}")
        sys.exit(1)

    pattern = os.path.join(str(obsidian_root), "*.md")
    all_files = glob.glob(pattern)

    if not all_files:
        print(f"❌ No .md files found in {obsidian_root}")
        sys.exit(1)

    files = []
    skipped = []

    for file in all_files:
        if skip_converted and target_dir and is_already_converted(file, target_dir):
            skipped.append(file)
        else:
            files.append(file)

    print(f"📁 Found {len(all_files)} files in Obsidian vault:")

    if files:
        print(f"   📝 Files to convert ({len(files)}):")
        for file in files:
            print(f"      • {os.path.basename(file)}")

    if skipped:
        print(f"   ⏭️  Files already converted ({len(skipped)}):")
        for file in skipped:
            print(f"      • {os.path.basename(file)}")

    if not files:
        print(f"❌ No files to convert (all {len(skipped)} files already converted)")
        sys.exit(0)

    return files


def generate_dates(num_files, mode="retroactive"):
    """Generate dates for posts"""
    today = datetime.now()
    dates = []

    if mode == "retroactive":
        # Start from today and go backwards
        for i in range(num_files):
            date = today - timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        print(f"📅 Using retroactive dates (starting from today going backwards)")

    elif mode == "progressive":
        # Start from today and go forwards
        for i in range(num_files):
            date = today + timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        print(f"📅 Using progressive dates (starting from today going forwards)")

    else:
        raise ValueError("Mode must be 'retroactive' or 'progressive'")

    return dates


ASSETS_DIR = "assets/images"

# Extensions treated as images/embeds by Obsidian
IMAGE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


def convert_obsidian_embeds(content, obsidian_file, target_dir):
    """Convert Obsidian ![[file]] embeds to Jekyll markdown and copy assets"""
    obsidian_dir = Path(obsidian_file).parent
    copied_files = []

    def replace_embed(match):
        raw_name = match.group(1)
        # Strip .excalidraw suffix if present (Excalidraw exports)
        clean_name = re.sub(r"\.excalidraw(\.\w+)$", r"\1", raw_name)
        ext = Path(clean_name).suffix.lower()

        if ext not in IMAGE_EXTENSIONS:
            return match.group(0)  # leave non-image embeds unchanged

        # Search for the source file in the Obsidian vault
        source = None
        for candidate in obsidian_dir.rglob(raw_name):
            source = candidate
            break
        if source is None:
            # Try clean name too
            for candidate in obsidian_dir.rglob(clean_name):
                source = candidate
                break

        # Determine project root from target_dir
        project_root = Path(target_dir).parent
        dest_dir = project_root / ASSETS_DIR
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / clean_name

        if source and source.exists() and not dest.exists():
            shutil.copy2(source, dest)
            copied_files.append(clean_name)
            print(f"   📎 Copied {raw_name} → {ASSETS_DIR}/{clean_name}")

        alt_text = Path(clean_name).stem.replace("_", " ").replace("-", " ").title()
        return f"![{alt_text}](/{ASSETS_DIR}/{clean_name})"

    converted = re.sub(r"!\[\[([^\]]+)\]\]", replace_embed, content)
    return converted, copied_files


def create_jekyll_post(obsidian_file, date, target_dir):
    """Convert single Obsidian file to Jekyll post"""

    # Read original file
    try:
        with open(obsidian_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {obsidian_file}: {e}")
        return False

    # Extract title from filename
    filename = os.path.basename(obsidian_file)
    raw_title = extract_clean_title(filename)

    # Create Jekyll filename
    safe_title = sanitize_title(raw_title)
    jekyll_filename = f"{date}-{safe_title}.md"
    target_path = os.path.join(target_dir, jekyll_filename)

    # Convert Obsidian embeds to Jekyll markdown
    content, copied = convert_obsidian_embeds(content, obsidian_file, target_dir)

    # Create front matter if not exists
    if not content.strip().startswith("---"):
        categories_yaml = "[" + ", ".join(DEFAULT_CATEGORIES) + "]"
        tags_yaml = "[" + ", ".join(DEFAULT_TAGS) + "]"
        front_matter = f"""---
layout: post
title: "{raw_title}"
date: {date}
categories: {categories_yaml}
tags: {tags_yaml}
---

"""
        content = front_matter + content

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Write Jekyll post
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {filename} → {jekyll_filename}")
        return True
    except Exception as e:
        print(f"❌ Error writing {target_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert Obsidian files to Jekyll posts"
    )
    parser.add_argument(
        "--mode",
        choices=["retroactive", "progressive"],
        default="retroactive",
        help="Date assignment mode: retroactive (today backwards) or progressive (today forwards)",
    )
    parser.add_argument(
        "--target-dir",
        default=JEKYLL_POSTS_DIR,
        help=f"Target directory for Jekyll posts (default: {JEKYLL_POSTS_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually converting files",
    )
    parser.add_argument(
        "--skip-converted",
        action="store_true",
        help="Skip files that have already been converted to Jekyll format",
    )
    parser.add_argument(
        "--obsidian-path", help="Path to Obsidian vault (folder containing notes)"
    )

    args = parser.parse_args()

    print("🚀 Obsidian to Jekyll Converter")
    print("=" * 40)

    # Resolve Obsidian vault path
    obsidian_root = find_obsidian_root(args.obsidian_path)
    print(f"📁 Using Obsidian vault: {obsidian_root}")

    # Get Obsidian files
    obsidian_files = get_obsidian_files(
        obsidian_root, args.target_dir, args.skip_converted
    )

    # Generate dates
    dates = generate_dates(len(obsidian_files), args.mode)

    # Show conversion plan
    print(f"\n📋 Conversion Plan:")
    for i, (file, date) in enumerate(zip(obsidian_files, dates)):
        filename = os.path.basename(file)
        clean_title = extract_clean_title(filename)
        safe_title = sanitize_title(clean_title)
        jekyll_name = f"{date}-{safe_title}.md"
        print(f"   {i + 1}. {filename} → {jekyll_name}")
        print(f'      Title: "{clean_title}"')

    if args.dry_run:
        print(
            f"\n🔍 Dry run complete. Use without --dry-run to actually convert files."
        )
        return

    # Confirm conversion
    response = input(
        f"\n❓ Convert {len(obsidian_files)} files to {args.target_dir}? [y/N]: "
    )
    if response.lower() not in ["y", "yes"]:
        print("❌ Conversion cancelled.")
        return

    # Convert files
    print(f"\n🔄 Converting files...")
    successful = 0

    for obsidian_file, date in zip(obsidian_files, dates):
        if create_jekyll_post(obsidian_file, date, args.target_dir):
            successful += 1

    print(f"\n🎉 Conversion complete!")
    print(f"   ✅ {successful}/{len(obsidian_files)} files converted successfully")

    if successful < len(obsidian_files):
        print(f"   ⚠️  {len(obsidian_files) - successful} files had errors")


if __name__ == "__main__":
    main()
