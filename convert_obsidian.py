#!/usr/bin/env python3
"""
Automated Obsidian to Jekyll Posts Converter
Converts all .md files from Obsidian vault to Jekyll _posts format
"""

import os
import glob
from datetime import datetime, timedelta
import argparse
import sys

# Configuration
OBSIDIAN_DIR = "/Users/stefanodellapietra/Documents/Obsidian Vault/Xitnode"
JEKYLL_POSTS_DIR = "_posts"
DEFAULT_CATEGORIES = ["xitnode"]
DEFAULT_TAGS = ["xitnode", "ossessione"]

def extract_clean_title(filename):
    """Extract clean title from filename, removing date prefix if present"""
    import re

    # Remove .md extension
    title = filename.replace(".md", "")

    # Check if filename starts with date pattern (YYYY-MM-DD-)
    date_pattern = r'^\d{4}-\d{2}-\d{2}-'
    if re.match(date_pattern, title):
        # Remove the date prefix
        title = re.sub(date_pattern, '', title)
        # Convert dashes back to spaces and clean up
        title = title.replace('-', ' ').strip()
        # Capitalize first letter of each word
        title = ' '.join(word.capitalize() for word in title.split())

    return title

def sanitize_title(title):
    """Convert title to URL-safe slug"""
    return (
        title.replace(""", "")
        .replace(""", "")
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

def get_obsidian_files(target_dir=None, skip_converted=False):
    """Get all .md files from Obsidian directory"""
    if not os.path.exists(OBSIDIAN_DIR):
        print(f"❌ Obsidian directory not found: {OBSIDIAN_DIR}")
        sys.exit(1)

    pattern = os.path.join(OBSIDIAN_DIR, "*.md")
    all_files = glob.glob(pattern)

    if not all_files:
        print(f"❌ No .md files found in {OBSIDIAN_DIR}")
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
    parser = argparse.ArgumentParser(description="Convert Obsidian files to Jekyll posts")
    parser.add_argument(
        "--mode",
        choices=["retroactive", "progressive"],
        default="retroactive",
        help="Date assignment mode: retroactive (today backwards) or progressive (today forwards)"
    )
    parser.add_argument(
        "--target-dir",
        default=JEKYLL_POSTS_DIR,
        help=f"Target directory for Jekyll posts (default: {JEKYLL_POSTS_DIR})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually converting files"
    )
    parser.add_argument(
        "--skip-converted",
        action="store_true",
        help="Skip files that have already been converted to Jekyll format"
    )

    args = parser.parse_args()

    print("🚀 Obsidian to Jekyll Converter")
    print("=" * 40)

    # Get Obsidian files
    obsidian_files = get_obsidian_files(args.target_dir, args.skip_converted)

    # Generate dates
    dates = generate_dates(len(obsidian_files), args.mode)

    # Show conversion plan
    print(f"\n📋 Conversion Plan:")
    for i, (file, date) in enumerate(zip(obsidian_files, dates)):
        filename = os.path.basename(file)
        clean_title = extract_clean_title(filename)
        safe_title = sanitize_title(clean_title)
        jekyll_name = f"{date}-{safe_title}.md"
        print(f"   {i+1}. {filename} → {jekyll_name}")
        print(f"      Title: \"{clean_title}\"")

    if args.dry_run:
        print(f"\n🔍 Dry run complete. Use without --dry-run to actually convert files.")
        return

    # Confirm conversion
    response = input(f"\n❓ Convert {len(obsidian_files)} files to {args.target_dir}? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
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
