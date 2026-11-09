
import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    print(f"\n>>> {' '.join(command)}")
    return subprocess.run(command, cwd=cwd).returncode == 0

def check_environment():
    if not shutil.which("node") or not shutil.which("npm"):
        print("ERROR: Node.js and npm must be installed first.")
        sys.exit(1)

    run_command(["node", "-v"])
    run_command(["npm", "-v"])

def setup_nest_project(project_name):
    base_dir = Path.cwd()
    project_dir = base_dir / project_name

    if project_dir.exists():
        print(f"ERROR: Folder already exists: {project_dir}")
        return

    print("\n[1/5] Creating NestJS project...")

    success = run_command([
        "npx", "--yes", "@nestjs/cli", "new",
        project_name,
        "--package-manager", "npm",
        "--skip-git",
        "--skip-install"
    ], cwd=base_dir)

    if not success or not project_dir.exists():
        print("ERROR: NestJS project creation failed.")
        return

    print("\n[2/5] Installing npm dependencies...")

    installed = run_command(["npm", "install"], cwd=project_dir)

    if not installed:
        print("\n[3/5] Installation failed. Cleaning npm cache...")

        node_modules = project_dir / "node_modules"
        package_lock = project_dir / "package-lock.json"

        if node_modules.exists():
            shutil.rmtree(node_modules)

        if package_lock.exists():
            package_lock.unlink()

        run_command(["npm", "cache", "clean", "--force"])

        print("\n[4/5] Retrying npm installation...")

        installed = run_command(["npm", "install"], cwd=project_dir)

    if not installed:
        print("\nERROR: npm installation failed again.")
        print("Check npm debug logs for the actual error.")
        return

    print("\n[5/5] NestJS setup completed!")

    print(f"\nProject location: {project_dir}")
    print("\nStarting NestJS development server...")

    subprocess.run(
        ["npm", "run", "start:dev"],
        cwd=project_dir
    )

if __name__ == "__main__":
    print("===================================")
    print("       NestJS Project Setup")
    print("===================================")

    check_environment()

    name = sys.argv[1] if len(sys.argv) > 1 else input(
        "\nEnter your project name: "
    ).strip()

    if not name or not all(
        c.isalnum() or c in "-_" for c in name
    ):
        print("Invalid project name.")
        sys.exit(1)

    setup_nest_project(name)

# // python setup_nest.py
# python setup_nest.py projectname

# Check Node.js & npm
#         |
#         v
# Create NestJS Project
#         |
#         v
# Install Dependencies
#         |
#         v
# Installation Failed?
#      /       \
#    Yes        No
#     |          |
# Clear Cache    |
# Remove Lock    |
# Retry npm      |
#      \        /
#        v
#   Setup Complete
#        |
#        v
#   Start Server
#        |
#        v
#  localhost:3000