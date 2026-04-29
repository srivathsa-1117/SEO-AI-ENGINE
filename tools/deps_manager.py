#!/usr/bin/env python3
"""
Dependency Manager
Centralized package installation and verification.
Eliminates duplicate try/except blocks across tools.

Usage:
    # In Python tools, replace try/except ImportError with:
    from deps_manager import ensure_deps
    ensure_deps(["playwright", "beautifulsoup4", "requests"])

    # From command line:
    python tools/deps_manager.py --install all
    python tools/deps_manager.py --check audit
    python tools/deps_manager.py --repair
"""

import sys
import subprocess
import importlib.util
from typing import List, Dict
from pathlib import Path

# Dependency profiles for different workflows
DEPENDENCY_PROFILES = {
    "audit": [
        "playwright",
        "beautifulsoup4",
        "lxml",
        "requests",
        "extruct",
        "w3lib",
        "python-docx"
    ],
    "content": [
        "openai",
        "anthropic",
        "requests",
        "beautifulsoup4"
    ],
    "crawler": [
        "playwright",
        "beautifulsoup4",
        "lxml",
        "extruct",
        "w3lib",
        "requests"
    ],
    "schema": [
        "extruct",
        "w3lib",
        "requests"
    ],
    "serp": [
        "requests",
        "beautifulsoup4",
        "lxml"
    ],
    "all": [
        "playwright",
        "beautifulsoup4",
        "lxml",
        "requests",
        "extruct",
        "w3lib",
        "python-docx",
        "openai",
        "anthropic"
    ]
}

# Package name mapping (pip name → import name)
PACKAGE_IMPORT_MAP = {
    "python-docx": "docx",
    "beautifulsoup4": "bs4",
}

class DependencyManager:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.missing = []
        self.installed = []

    def normalize_package_name(self, pkg: str, for_import: bool = False) -> str:
        """
        Normalize package name for pip or import

        Args:
            pkg: Package name
            for_import: True if for import, False if for pip

        Returns:
            Normalized package name
        """
        if for_import:
            return PACKAGE_IMPORT_MAP.get(pkg, pkg.replace("-", "_"))
        else:
            return pkg

    def is_installed(self, package: str) -> bool:
        """Check if a package is installed"""
        import_name = self.normalize_package_name(package, for_import=True)

        try:
            spec = importlib.util.find_spec(import_name)
            return spec is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            return False

    def install_package(self, package: str) -> bool:
        """
        Install a single package via pip

        Args:
            package: Package name (pip format)

        Returns:
            True if successful, False if failed
        """
        print(f"[INSTALL] {package}...", end=" ", flush=True)

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print("✓")
                return True
            else:
                print(f"✗ ({result.stderr.strip()[:50]})")
                return False

        except subprocess.TimeoutExpired:
            print("✗ (timeout)")
            return False
        except Exception as e:
            print(f"✗ ({str(e)[:50]})")
            return False

    def install_playwright_browsers(self) -> bool:
        """Install Playwright browsers if Playwright is installed"""
        if not self.is_installed("playwright"):
            return False

        print("[INSTALL] Playwright browsers...", end=" ", flush=True)

        try:
            result = subprocess.run(
                ["playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("✓")
                return True
            else:
                print(f"✗ ({result.stderr.strip()[:50]})")
                return False

        except FileNotFoundError:
            # Playwright CLI not in PATH, try python -m
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "playwright", "install", "chromium"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                if result.returncode == 0:
                    print("✓")
                    return True
                else:
                    print(f"✗ ({result.stderr.strip()[:50]})")
                    return False

            except Exception as e:
                print(f"✗ ({str(e)[:50]})")
                return False

        except Exception as e:
            print(f"✗ ({str(e)[:50]})")
            return False

    def check_dependencies(self, profile: str = "all") -> Dict:
        """
        Check which dependencies are installed

        Args:
            profile: Dependency profile to check

        Returns:
            Dict with "installed", "missing", and "total" keys
        """
        packages = DEPENDENCY_PROFILES.get(profile, DEPENDENCY_PROFILES["all"])

        self.installed = []
        self.missing = []

        for pkg in packages:
            if self.is_installed(pkg):
                self.installed.append(pkg)
            else:
                self.missing.append(pkg)

        return {
            "installed": self.installed,
            "missing": self.missing,
            "total": len(packages)
        }

    def ensure_dependencies(self, profile: str = "all", auto_install: bool = True) -> bool:
        """
        Ensure all dependencies are installed

        Args:
            profile: Dependency profile to ensure
            auto_install: Automatically install missing packages

        Returns:
            True if all dependencies satisfied, False if any missing
        """
        result = self.check_dependencies(profile)

        if not result["missing"]:
            if self.verbose:
                print(f"[OK] All {result['total']} dependencies installed")
            return True

        print(f"[MISSING] {len(result['missing'])} packages need installation:")
        for pkg in result["missing"]:
            print(f"  - {pkg}")

        if not auto_install:
            print(f"\nRun: pip install {' '.join(result['missing'])}")
            return False

        print(f"\nInstalling missing packages...\n")

        success_count = 0
        for pkg in result["missing"]:
            if self.install_package(pkg):
                success_count += 1

        # Install Playwright browsers if Playwright was just installed
        if "playwright" in result["missing"] and success_count > 0:
            self.install_playwright_browsers()

        if success_count == len(result["missing"]):
            print(f"\n[SUCCESS] All {success_count} packages installed")
            return True
        else:
            print(f"\n[WARNING] {success_count}/{len(result['missing'])} packages installed")
            failed = [pkg for pkg in result["missing"] if not self.is_installed(pkg)]
            print(f"Failed: {', '.join(failed)}")
            return False


# Convenience function for use in other tools
def ensure_deps(packages: List[str], auto_install: bool = True) -> bool:
    """
    Ensure specific packages are installed (for use in other tools)

    Args:
        packages: List of package names (pip format)
        auto_install: Automatically install if missing

    Returns:
        True if all packages available, False if any missing

    Example:
        from deps_manager import ensure_deps
        ensure_deps(["playwright", "beautifulsoup4", "requests"])
    """
    manager = DependencyManager(verbose=False)

    missing = []
    for pkg in packages:
        if not manager.is_installed(pkg):
            missing.append(pkg)

    if not missing:
        return True

    if not auto_install:
        print(f"[ERROR] Missing packages: {', '.join(missing)}")
        print(f"Fix: pip install {' '.join(missing)}")
        sys.exit(1)

    print(f"[AUTO-INSTALL] Installing {len(missing)} missing packages...")

    for pkg in missing:
        manager.install_package(pkg)

    # Verify all installed
    still_missing = [pkg for pkg in packages if not manager.is_installed(pkg)]

    if still_missing:
        print(f"[ERROR] Failed to install: {', '.join(still_missing)}")
        sys.exit(1)

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Dependency manager for SEO AI OS")
    parser.add_argument("--install", choices=list(DEPENDENCY_PROFILES.keys()),
                       help="Install dependencies for a profile")
    parser.add_argument("--check", choices=list(DEPENDENCY_PROFILES.keys()),
                       help="Check dependencies for a profile")
    parser.add_argument("--repair", action="store_true",
                       help="Repair broken installations")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose output")
    args = parser.parse_args()

    manager = DependencyManager(verbose=args.verbose)

    if args.check:
        result = manager.check_dependencies(args.check)

        print(f"\n{'='*70}")
        print(f"DEPENDENCY CHECK — {args.check.upper()}")
        print(f"{'='*70}\n")
        print(f"Installed: {len(result['installed'])}/{result['total']}")

        if result['installed']:
            print("\n✓ Installed:")
            for pkg in result['installed']:
                print(f"  - {pkg}")

        if result['missing']:
            print("\n✗ Missing:")
            for pkg in result['missing']:
                print(f"  - {pkg}")

            print(f"\nTo install: python tools/deps_manager.py --install {args.check}")

        print()
        sys.exit(0 if not result['missing'] else 1)

    elif args.install:
        success = manager.ensure_dependencies(args.install, auto_install=True)
        sys.exit(0 if success else 1)

    elif args.repair:
        print("Repairing all dependencies...\n")
        success = manager.ensure_dependencies("all", auto_install=True)
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
