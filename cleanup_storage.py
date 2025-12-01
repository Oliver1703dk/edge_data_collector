#!/usr/bin/env python3
"""
Remove generated capture artifacts (frames and simulated images).

The main data-producing location is:
- edge_data_collector/camera/images : frames saved by main.py and main_video.py

By default this script prompts before deleting. Use --yes to skip confirmation
or --dry-run to see what would be removed without deleting anything.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, Tuple


def human_size(num_bytes: int) -> str:
    """Convert a byte count to a readable string."""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def directory_size(path: Path) -> int:
    """Return the total size of all files under a directory."""
    if not path.exists():
        return 0
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def purge_directory_contents(path: Path, dry_run: bool) -> Tuple[int, int]:
    """
    Delete all files and subdirectories inside a directory.

    Returns:
        tuple: (bytes_removed, items_removed)
    """
    if not path.exists():
        return 0, 0

    bytes_removed = 0
    items_removed = 0

    for child in path.iterdir():
        if child.is_dir():
            if dry_run:
                bytes_removed += directory_size(child)
                items_removed += 1
            else:
                bytes_removed += directory_size(child)
                shutil.rmtree(child)
                items_removed += 1
        else:
            if dry_run:
                bytes_removed += child.stat().st_size
                items_removed += 1
            else:
                bytes_removed += child.stat().st_size
                child.unlink()
                items_removed += 1

    return bytes_removed, items_removed


def cleanup(paths: Iterable[Tuple[Path, str]], dry_run: bool) -> None:
    """Perform cleanup across the given targets."""
    for target_path, description in paths:
        size_before = directory_size(target_path)
        if not target_path.exists():
            print(f"[skip] {target_path} (missing) - {description}")
            continue

        bytes_removed, items_removed = purge_directory_contents(target_path, dry_run)
        action = "Would remove" if dry_run else "Removed"
        print(
            f"[done] {action} {items_removed} item(s) "
            f"from {target_path} ({human_size(bytes_removed)}). {description}"
        )
        size_after = directory_size(target_path) if not dry_run else size_before
        print(
            f"       Size before: {human_size(size_before)} | "
            f"after: {human_size(size_after)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Delete generated captures (frames and images) to free disk space."
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Do not prompt for confirmation; proceed immediately.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without removing anything.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    targets = [
        (
            project_root / "edge_data_collector" / "camera" / "images",
            "Frames and simulated images saved by main.py/main_video.py.",
        ),
    ]

    if not args.yes:
        proceed = input(
            "This will delete generated captures (frames and images). Continue? [y/N]: "
        ).strip().lower()
        if proceed not in ("y", "yes"):
            print("Aborted.")
            return

    cleanup(targets, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
