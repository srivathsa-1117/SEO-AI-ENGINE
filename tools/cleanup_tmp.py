#!/usr/bin/env python3
"""
.tmp Directory Cleanup Tool
Automatically removes stale temporary files to prevent disk bloat and stale data bugs.

Features:
- Remove files older than N days
- Archive important files before deletion
- Smart detection: keeps files referenced in recent reports
- Dry-run mode to preview deletions

Usage:
    python tools/cleanup_tmp.py --older-than 7                    # Remove files >7 days old
    python tools/cleanup_tmp.py --older-than 30 --archive         # Archive before deleting
    python tools/cleanup_tmp.py --dry-run                          # Preview only
    python tools/cleanup_tmp.py --force-all                        # Delete everything (dangerous!)
"""

import argparse
import time
import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta

class TmpCleaner:
    def __init__(self, tmp_dir: str = ".tmp", archive_dir: str = ".tmp_archive"):
        self.tmp_dir = Path(tmp_dir)
        self.archive_dir = Path(archive_dir)
        self.deleted_count = 0
        self.archived_count = 0
        self.kept_count = 0
        self.bytes_freed = 0

    def get_file_age_days(self, file_path: Path) -> float:
        """Get file age in days"""
        return (time.time() - file_path.stat().st_mtime) / 86400

    def is_file_referenced(self, file_path: Path) -> bool:
        """
        Check if file is referenced in recent reports or workflows.
        Files actively being used should not be deleted.
        """
        # Check if file was modified in last 24 hours (actively being used)
        if self.get_file_age_days(file_path) < 1:
            return True

        # Check if file is referenced in recent reports
        reports_dir = Path("reports")
        if reports_dir.exists():
            recent_reports = sorted(
                reports_dir.glob("*.docx"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )[:5]  # Check last 5 reports

            file_slug = file_path.stem.split("_")[0]  # Extract client slug

            for report in recent_reports:
                if file_slug in report.stem:
                    return True

        return False

    def archive_file(self, file_path: Path) -> bool:
        """Archive file before deletion"""
        try:
            # Create archive directory structure by month
            file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
            month_dir = self.archive_dir / file_date.strftime("%Y-%m")
            month_dir.mkdir(parents=True, exist_ok=True)

            # Copy file to archive
            archive_path = month_dir / file_path.name
            shutil.copy2(file_path, archive_path)

            self.archived_count += 1
            return True

        except Exception as e:
            print(f"[WARNING] Failed to archive {file_path.name}: {e}")
            return False

    def cleanup(self, older_than_days: int = 7, archive: bool = False, dry_run: bool = False, force_all: bool = False):
        """
        Clean up .tmp directory

        Args:
            older_than_days: Remove files older than this many days
            archive: Archive files before deletion
            dry_run: Preview only, don't actually delete
            force_all: Delete everything (ignores age check)
        """
        if not self.tmp_dir.exists():
            print(f"[INFO] .tmp directory doesn't exist. Nothing to clean.")
            return

        print(f"\n{'='*70}")
        print(f".TMP CLEANUP TOOL")
        print(f"{'='*70}\n")
        print(f"Mode:     {'DRY RUN (preview only)' if dry_run else 'LIVE DELETION'}")
        print(f"Age:      {older_than_days if not force_all else 'ALL FILES'} days")
        print(f"Archive:  {'Yes' if archive else 'No'}")
        print()

        files_to_delete = []
        files_to_keep = []

        # Scan .tmp directory
        for file_path in self.tmp_dir.glob("*"):
            if not file_path.is_file():
                continue

            age_days = self.get_file_age_days(file_path)
            size_mb = file_path.stat().st_size / 1024 / 1024

            # Determine if file should be deleted
            should_delete = False

            if force_all:
                should_delete = True
            elif age_days > older_than_days:
                # Check if file is actively referenced
                if not self.is_file_referenced(file_path):
                    should_delete = True
                else:
                    files_to_keep.append((file_path, age_days, size_mb, "Referenced in recent reports"))

            if should_delete:
                files_to_delete.append((file_path, age_days, size_mb))
            elif not should_delete and age_days <= older_than_days:
                files_to_keep.append((file_path, age_days, size_mb, "Too recent"))

        # Print summary
        print(f"Files to DELETE: {len(files_to_delete)}")
        if files_to_delete:
            print()
            for file_path, age_days, size_mb in sorted(files_to_delete, key=lambda x: x[1], reverse=True):
                print(f"  [DELETE] {file_path.name:40s} {age_days:6.1f} days old | {size_mb:8.2f} MB")

        print(f"\nFiles to KEEP: {len(files_to_keep)}")
        if files_to_keep:
            print()
            for file_path, age_days, size_mb, reason in files_to_keep[:10]:  # Show first 10
                print(f"  [KEEP]   {file_path.name:40s} {age_days:6.1f} days old | {reason}")
            if len(files_to_keep) > 10:
                print(f"  ... and {len(files_to_keep) - 10} more")

        # Calculate space to be freed
        total_size_mb = sum(size_mb for _, _, size_mb in files_to_delete)

        print(f"\n{'='*70}")
        print(f"Space to free: {total_size_mb:.2f} MB")

        # Perform deletion (if not dry run)
        if not dry_run and files_to_delete:
            confirm = input(f"\nProceed with deletion of {len(files_to_delete)} files? [y/N]: ")

            if confirm.lower() != 'y':
                print("[CANCELLED] No files were deleted.")
                return

            print()
            for file_path, age_days, size_mb in files_to_delete:
                try:
                    # Archive if requested
                    if archive:
                        self.archive_file(file_path)

                    # Delete file
                    file_path.unlink()
                    self.deleted_count += 1
                    self.bytes_freed += file_path.stat().st_size if file_path.exists() else int(size_mb * 1024 * 1024)

                    print(f"[DELETED] {file_path.name}")

                except Exception as e:
                    print(f"[ERROR] Failed to delete {file_path.name}: {e}")

            print(f"\n{'='*70}")
            print(f"[DONE] Deleted {self.deleted_count} files ({self.bytes_freed / 1024 / 1024:.2f} MB freed)")
            if archive:
                print(f"[ARCHIVED] {self.archived_count} files saved to {self.archive_dir}")

        elif dry_run:
            print(f"\n[DRY RUN] No files were actually deleted.")
            print(f"Run without --dry-run to perform deletion.")

        print()


def main():
    parser = argparse.ArgumentParser(description=".tmp directory cleanup tool")
    parser.add_argument("--older-than", type=int, default=7,
                       help="Delete files older than N days (default: 7)")
    parser.add_argument("--archive", action="store_true",
                       help="Archive files before deletion")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview only, don't actually delete")
    parser.add_argument("--force-all", action="store_true",
                       help="Delete ALL files (dangerous!)")
    args = parser.parse_args()

    cleaner = TmpCleaner()
    cleaner.cleanup(
        older_than_days=args.older_than,
        archive=args.archive,
        dry_run=args.dry_run,
        force_all=args.force_all
    )


if __name__ == "__main__":
    main()
