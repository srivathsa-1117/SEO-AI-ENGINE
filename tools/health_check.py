#!/usr/bin/env python3
"""
System Health Check Dashboard
Single command to check entire system status.

Usage:
    python tools/health_check.py
    python tools/health_check.py --verbose
    python tools/health_check.py --fix-all
"""

import argparse
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta

# Color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

class HealthChecker:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.checks = {
            "passed": [],
            "warnings": [],
            "errors": []
        }

    def check_python_version(self):
        """Check Python version"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            self.checks["passed"].append(f"Python {version.major}.{version.minor}.{version.micro}")
        else:
            self.checks["errors"].append(f"Python 3.10+ required (found {version.major}.{version.minor})")

    def check_dependencies(self):
        """Check critical dependencies"""
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from deps_manager import DependencyManager

            manager = DependencyManager()
            result = manager.check_dependencies("all")

            if not result["missing"]:
                self.checks["passed"].append(f"All {result['total']} dependencies installed")
            elif len(result["missing"]) <= 3:
                self.checks["warnings"].append(f"{len(result['missing'])} packages missing: {', '.join(result['missing'][:3])}")
            else:
                self.checks["errors"].append(f"{len(result['missing'])} packages missing (run: python tools/deps_manager.py --install all)")

        except Exception as e:
            self.checks["errors"].append(f"Dependency check failed: {str(e)[:50]}")

    def check_tmp_directory(self):
        """Check .tmp directory health"""
        tmp_dir = Path(".tmp")

        if not tmp_dir.exists():
            self.checks["warnings"].append(".tmp directory missing (will be created automatically)")
            return

        # Count files
        files = list(tmp_dir.glob("*"))
        file_count = len([f for f in files if f.is_file()])

        if file_count == 0:
            self.checks["passed"].append(".tmp directory clean")
        elif file_count <= 20:
            self.checks["passed"].append(f".tmp directory has {file_count} files")
        elif file_count <= 50:
            self.checks["warnings"].append(f".tmp directory has {file_count} files (consider cleanup)")
        else:
            self.checks["warnings"].append(f".tmp directory has {file_count} files (run: python tools/cleanup_tmp.py)")

        # Check for stale files
        import time
        stale_count = 0
        for file in files:
            if file.is_file():
                age_days = (time.time() - file.stat().st_mtime) / 86400
                if age_days > 7:
                    stale_count += 1

        if stale_count > 0:
            self.checks["warnings"].append(f"{stale_count} stale files >7 days old (run: python tools/cleanup_tmp.py --older-than 7)")

    def check_client_folders(self):
        """Check client folders"""
        clients_dir = Path("clients")

        if not clients_dir.exists():
            self.checks["warnings"].append("No client folders found (run /add_client to onboard first client)")
            return

        clients = [d for d in clients_dir.iterdir() if d.is_dir() and d.name != "_template"]

        if not clients:
            self.checks["warnings"].append("No clients onboarded (run /add_client)")
        elif len(clients) == 1:
            self.checks["passed"].append(f"1 client configured: {clients[0].name}")
        else:
            self.checks["passed"].append(f"{len(clients)} clients configured")

        # Check for invalid client folders (missing brand_kit.json)
        invalid = []
        for client in clients:
            brand_kit = client / "brand_kit.json"
            if not brand_kit.exists():
                invalid.append(client.name)

        if invalid:
            self.checks["warnings"].append(f"{len(invalid)} clients missing brand_kit.json: {', '.join(invalid[:3])}")

    def check_workflows(self):
        """Check workflow files"""
        workflows_dir = Path("workflows")

        if not workflows_dir.exists():
            self.checks["errors"].append("workflows/ directory missing (critical system files)")
            return

        workflows = list(workflows_dir.glob("*.md"))

        if len(workflows) < 20:
            self.checks["warnings"].append(f"Only {len(workflows)} workflows found (expected 24+)")
        else:
            self.checks["passed"].append(f"{len(workflows)} workflows available")

    def check_tools(self):
        """Check tool scripts"""
        tools_dir = Path("tools")

        if not tools_dir.exists():
            self.checks["errors"].append("tools/ directory missing (critical system files)")
            return

        tools = list(tools_dir.glob("*.py"))

        if len(tools) < 20:
            self.checks["warnings"].append(f"Only {len(tools)} tools found (expected 25+)")
        else:
            self.checks["passed"].append(f"{len(tools)} tools available")

        # Check critical tools exist
        critical_tools = [
            "utils.py",
            "framework_detector.py",
            "seo_crawler.py",
            "chat_to_report.py"
        ]

        missing_critical = []
        for tool in critical_tools:
            if not (tools_dir / tool).exists():
                missing_critical.append(tool)

        if missing_critical:
            self.checks["errors"].append(f"Critical tools missing: {', '.join(missing_critical)}")

    def check_env_file(self):
        """Check .env configuration"""
        env_path = Path(".env")

        if not env_path.exists():
            self.checks["warnings"].append(".env file missing (API integrations won't work)")
            self.checks["warnings"].append("Fix: Copy .env.example to .env and add API keys")
            return

        with open(env_path) as f:
            env_content = f.read()

        # Check for critical keys
        required_keys = ["GOOGLE_API_KEY", "ANTHROPIC_API_KEY"]
        empty_keys = []

        for key in required_keys:
            if key not in env_content:
                empty_keys.append(key)
            elif f"{key}=" in env_content:
                value = env_content.split(f"{key}=")[1].split("\n")[0].strip()
                if not value or value == '""' or value == "''":
                    empty_keys.append(key)

        if not empty_keys:
            self.checks["passed"].append(".env configured with API keys")
        else:
            self.checks["warnings"].append(f"Empty API keys in .env: {', '.join(empty_keys)}")

    def check_mcp_servers(self):
        """Check MCP server configuration"""
        # Check if Claude Desktop config exists
        claude_config_paths = [
            Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",  # Windows
            Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",  # Mac
            Path.home() / ".config" / "claude" / "claude_desktop_config.json"  # Linux
        ]

        config_found = False
        for path in claude_config_paths:
            if path.exists():
                config_found = True

                try:
                    with open(path) as f:
                        config = json.load(f)

                    servers = config.get("mcpServers", {})

                    if not servers:
                        self.checks["warnings"].append("No MCP servers configured")
                    else:
                        self.checks["passed"].append(f"{len(servers)} MCP servers configured: {', '.join(servers.keys())}")

                except Exception as e:
                    self.checks["warnings"].append(f"MCP config exists but couldn't parse: {str(e)[:50]}")

                break

        if not config_found:
            self.checks["warnings"].append("Claude Desktop config not found (MCP servers not configured)")

    def check_recent_activity(self):
        """Check for recent system activity"""
        tmp_dir = Path(".tmp")
        reports_dir = Path("reports")

        # Check last file in .tmp
        if tmp_dir.exists():
            files = sorted(
                [f for f in tmp_dir.glob("*") if f.is_file()],
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )

            if files:
                last_modified = datetime.fromtimestamp(files[0].stat().st_mtime)
                days_ago = (datetime.now() - last_modified).days

                if days_ago == 0:
                    self.checks["passed"].append("System used today")
                elif days_ago <= 7:
                    self.checks["passed"].append(f"Last activity {days_ago} days ago")
                else:
                    self.checks["warnings"].append(f"No activity in {days_ago} days")

        # Check recent reports
        if reports_dir.exists():
            reports = sorted(
                reports_dir.glob("*.docx"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )

            if reports:
                last_report = datetime.fromtimestamp(reports[0].stat().st_mtime)
                days_ago = (datetime.now() - last_report).days

                if days_ago <= 7:
                    self.checks["passed"].append(f"Last report generated {days_ago} days ago")

    def run_all_checks(self):
        """Run all health checks"""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}SYSTEM HEALTH CHECK — SEO AI OS{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Run checks
        self.check_python_version()
        self.check_dependencies()
        self.check_tmp_directory()
        self.check_client_folders()
        self.check_workflows()
        self.check_tools()
        self.check_env_file()
        self.check_mcp_servers()
        self.check_recent_activity()

        # Print results
        if self.checks["passed"]:
            print(f"{GREEN}✓ PASSED ({len(self.checks['passed'])}){RESET}")
            for msg in self.checks["passed"]:
                print(f"  {GREEN}✓{RESET} {msg}")

        if self.checks["warnings"]:
            print(f"\n{YELLOW}⚠ WARNINGS ({len(self.checks['warnings'])}){RESET}")
            for msg in self.checks["warnings"]:
                print(f"  {YELLOW}⚠{RESET} {msg}")

        if self.checks["errors"]:
            print(f"\n{RED}✗ ERRORS ({len(self.checks['errors'])}){RESET}")
            for msg in self.checks["errors"]:
                print(f"  {RED}✗{RESET} {msg}")

        # Overall status
        print(f"\n{BLUE}{'='*70}{RESET}")

        if not self.checks["errors"] and not self.checks["warnings"]:
            print(f"{GREEN}[HEALTHY] System is fully operational{RESET}")
            health_score = 100
        elif not self.checks["errors"]:
            print(f"{YELLOW}[FUNCTIONAL] System works but has minor issues{RESET}")
            health_score = 80 - (len(self.checks["warnings"]) * 5)
        else:
            print(f"{RED}[DEGRADED] Critical issues found{RESET}")
            health_score = 50 - (len(self.checks["errors"]) * 10)

        print(f"Health Score: {max(0, health_score)}/100")
        print()

        return len(self.checks["errors"]) == 0


def main():
    parser = argparse.ArgumentParser(description="System health check")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--fix-all", action="store_true", help="Attempt to fix all issues")
    args = parser.parse_args()

    checker = HealthChecker(verbose=args.verbose)
    healthy = checker.run_all_checks()

    if args.fix_all:
        print(f"{BLUE}Running automated fixes...{RESET}\n")

        # Install missing dependencies
        if any("packages missing" in msg for msg in checker.checks.get("errors", []) + checker.checks.get("warnings", [])):
            print("[FIX] Installing missing dependencies...")
            subprocess.run([sys.executable, "tools/deps_manager.py", "--install", "all"])

        # Clean up .tmp
        if any("stale files" in msg for msg in checker.checks.get("warnings", [])):
            print("[FIX] Cleaning up .tmp directory...")
            subprocess.run([sys.executable, "tools/cleanup_tmp.py", "--older-than", "7"])

        print(f"\n{GREEN}[DONE] Automated fixes complete. Re-run health check to verify.{RESET}\n")

    sys.exit(0 if healthy else 1)


if __name__ == "__main__":
    main()
