#!/usr/bin/env python3
"""
Example demonstration of all AgentVCS commands.
This script creates a demo repository and showcases all features.
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path


def run_command(cmd: str, cwd: Path) -> str:
    """Run a shell command and return output."""
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout


def main():
    """Run the complete AgentVCS demonstration."""
    # Create a temporary directory for the demo
    demo_dir = Path(tempfile.mkdtemp(prefix="agentvcs_demo_"))
    print(f"Creating demo repository in: {demo_dir}")
    
    try:
        # Install AgentVCS
        print("\n=== Installing AgentVCS ===")
        run_command("pip install -e .", Path.cwd())
        
        # Change to demo directory
        os.chdir(demo_dir)
        
        # 1. Initialize repository
        print("\n=== 1. Initializing AgentVCS Repository ===")
        run_command("agentvcs init --name demo-project", demo_dir)
        
        # 2. Create semantic commits
        print("\n=== 2. Creating Semantic Commits ===")
        run_command(
            'agentvcs commit --intent "Add authentication module" '
            '--risk medium --subsystem auth --type feature '
            '--reasoning "Initial implementation of JWT-based authentication" '
            '--author agent-dev --files src/auth.py',
            demo_dir
        )
        
        run_command(
            'agentvcs commit --intent "Fix SQL injection vulnerability" '
            '--risk critical --subsystem database --type security '
            '--reasoning "Parameterized queries implemented to prevent SQL injection" '
            '--bug-id CVE-2024-1234 --author security-bot --files src/db.py',
            demo_dir
        )
        
        run_command(
            'agentvcs commit --intent "Optimize query performance" '
            '--risk low --subsystem database --type perf '
            '--reasoning "Added database indexes for frequently queried columns" '
            '--author perf-bot --files src/db.py',
            demo_dir
        )
        
        # 3. Propose changes
        print("\n=== 3. Proposing Autonomous Changes ===")
        run_command(
            'agentvcs propose --type refactor --target src/auth.py '
            '--agent refactor-bot --reasoning "Extract token validation into separate method" '
            '--risk low --impact "Improved code maintainability"',
            demo_dir
        )
        
        # 4. Merge simulation
        print("\n=== 4. Predictive Merge Simulation ===")
        run_command(
            'agentvcs merge --branch feature/new-auth --simulate --strategy auto',
            demo_dir
        )
        
        # 5. Multi-agent review
        print("\n=== 5. Multi-Agent Review Swarm ===")
        # Get the first commit ID for review
        commits_output = run_command("agentvcs history --limit 1", demo_dir)
        commit_id = commits_output.split()[1] if commits_output.split() else "unknown"
        
        run_command(
            f'agentvcs review --commit {commit_id} --agents security,performance,architecture',
            demo_dir
        )
        
        # 6. Refactor pipeline
        print("\n=== 6. Autonomous Refactor Pipeline ===")
        run_command(
            'agentvcs refactor --target src/auth.py --pattern extract-method --agent refactor-bot',
            demo_dir
        )
        
        # 7. Sentinel monitoring
        print("\n=== 7. Continuous Risk Monitoring ===")
        run_command('agentvcs sentinel --interval 30', demo_dir)
        
        # 8. Intent-aware history
        print("\n=== 8. Intent-Aware History Queries ===")
        run_command('agentvcs history --query "authentication"', demo_dir)
        run_command('agentvcs history --agent security-bot', demo_dir)
        run_command('agentvcs history --limit 5', demo_dir)
        
        # 9. Policy management
        print("\n=== 9. Machine-First Permissions ===")
        run_command('agentvcs policy --list-rules', demo_dir)
        run_command(
            'agentvcs policy --add-rule "security-bot:*:always"',
            demo_dir
        )
        run_command('agentvcs policy --list-rules', demo_dir)
        
        # 10. Event streaming
        print("\n=== 10. Event Streaming ===")
        run_command('agentvcs events --tail 5', demo_dir)
        
        # 11. Graph queries
        print("\n=== 11. Semantic Repository Graph ===")
        run_command('agentvcs graph --export json', demo_dir)
        run_command('agentvcs graph --query "dependencies of src/auth.py"', demo_dir)
        
        # 12. Swarm coordination
        print("\n=== 12. Multi-Agent Swarm Coordination ===")
        run_command(
            'agentvcs swarm --task "Optimize database queries for production" '
            '--agents performance,architecture --timeout 120',
            demo_dir
        )
        
        # 13. Version check
        print("\n=== 13. Version Information ===")
        run_command('agentvcs --version', demo_dir)
        run_command('agentvcs -v', demo_dir)
        
        print("\n=== Demo Complete ===")
        print(f"Demo repository created at: {demo_dir}")
        print("You can explore the .agentvcs directory to see semantic metadata.")
        
    except Exception as e:
        print(f"Error during demo: {e}")
    finally:
        # Optionally clean up
        # shutil.rmtree(demo_dir)
        print(f"\nDemo directory preserved at: {demo_dir}")
        print("To clean up, run: rm -rf", demo_dir)


if __name__ == "__main__":
    main()
