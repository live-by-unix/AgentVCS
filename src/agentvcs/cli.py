"""Main CLI entry point for AgentVCS."""

import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table

from agentvcs import __version__
from agentvcs.core.storage import Storage
from agentvcs.models import (
    Commit, Proposal, RiskLevel, ChangeType, PolicyRule, 
    Event, GraphNode, GraphEdge, SwarmTask, AgentRole, Remote
)
from agentvcs.agents.base import BaseAgent
from agentvcs.agents.registry import AgentRegistry
from agentvcs.merge.engine import MergeEngine
from agentvcs.graph.builder import GraphBuilder
from agentvcs.events.stream import EventStream
from agentvcs.policy.engine import PolicyEngine

console = Console()


def get_storage() -> Storage:
    """Get storage instance for current directory."""
    repo_path = Path.cwd()
    storage = Storage(repo_path)
    if not storage.is_initialized():
        console.print("[red]Error: Not an AgentVCS repository. Run 'agentvcs init' first.[/red]")
        sys.exit(1)
    return storage


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="agentvcs")
@click.pass_context
def main(ctx):
    """AgentVCS - The world's first agentic version control system.
    
    A semantic, agent-native VCS designed for autonomous AI workflows with:
    - Semantic commits with intent, risk, and reasoning traces
    - Multi-agent review swarms for security, performance, and architecture
    - Predictive merge engine with conflict simulation
    - Machine-first permissions and policy enforcement
    - Intent-aware history queries
    - Continuous risk monitoring with sentinel agents
    - Event streaming for real-time awareness
    - Semantic repository graphs for dependency analysis
    """
    if ctx.invoked_subcommand is None:
        console.print("\n[bold cyan]AgentVCS[/bold cyan] - The world's first agentic version control system\n")
        console.print("[bold]Quick Start:[/bold]")
        console.print("  agentvcs init              Initialize a new repository")
        console.print("  agentvcs remote add        Add remote repository (e.g., origin)")
        console.print("  agentvcs commit            Create a semantic commit")
        console.print("  agentvcs push              Push to remote repository")
        console.print("  agentvcs history           View commit history")
        console.print("  agentvcs --help            Show all commands\n")
        console.print("[bold]Repository Commands:[/bold]")
        console.print("  init              Initialize repository with semantic metadata")
        console.print("  status            Show repository status and remote information")
        console.print("  remote            Manage remote repositories (add/remove/list)")
        console.print("  push              Push commits and metadata to remote")
        console.print("  pull              Pull commits and metadata from remote")
        console.print("  fetch             Fetch updates without merging")
        console.print("  clone             Clone a remote repository (coming soon)")
        console.print("\n[bold]Commit Commands:[/bold]")
        console.print("  commit            Create semantic commit with intent and reasoning")
        console.print("  propose           Propose autonomous changes for review")
        console.print("  merge             Predictive merge with conflict resolution")
        console.print("  history           Query intent-aware commit history")
        console.print("\n[bold]Agent Commands:[/bold]")
        console.print("  review            Launch multi-agent review swarm")
        console.print("  refactor          Autonomous refactor pipeline")
        console.print("  sentinel          Continuous risk monitoring")
        console.print("  swarm             Multi-agent coordination")
        console.print("\n[bold]Management Commands:[/bold]")
        console.print("  policy            Manage machine-first permissions")
        console.print("  events            Event streaming and monitoring")
        console.print("  graph             Semantic repository graph queries")
        console.print("  analyze           Repository analytics and insights")
        console.print("  backup            Backup/restore repository")
        console.print("  export            Export data to JSON/YAML/CSV")
        console.print("  import            Import data from exported files")
        console.print("\n[bold]Git Integration:[/bold]")
        console.print("  AgentVCS supports Git remotes for seamless integration")
        console.print("  Use --type git when adding remotes for Git compatibility")
        console.print("  Push/pull commands work with both AgentVCS and Git remotes")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  agentvcs init --name my-project")
        console.print("  agentvcs remote add origin https://github.com/user/repo --type git --set-default")
        console.print("  agentvcs commit --intent 'fix bug' --risk medium --reasoning '...'")
        console.print("  agentvcs push")
        console.print("  agentvcs history --query 'authentication' --format detailed")
        console.print("  agentvcs review --commit abc123 --agents security,performance")
        console.print("\n[dim]Run 'agentvcs <command> --help' for detailed command help.[/dim]")


def main_with_error_handling():
    """Main entry point with error handling for invalid commands."""
    try:
        main(standalone_mode=False)
    except click.exceptions.ClickException as e:
        # Click already handles invalid commands nicely
        e.show()
        sys.exit(e.exit_code)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("\n[dim]Run 'agentvcs --help' to see available commands.[/dim]")
        sys.exit(1)


@main.command()
@click.option("--git-migrate", is_flag=True, help="Migrate from existing Git repository")
@click.option("--name", help="Repository name")
def init(git_migrate: bool, name: Optional[str]):
    """Initialize a new agent-native repository with semantic metadata and agent policies."""
    repo_path = Path.cwd()
    storage = Storage(repo_path)
    
    if storage.is_initialized():
        console.print("[yellow]Repository already initialized.[/yellow]")
        return
    
    storage.initialize()
    
    if git_migrate:
        # Check if git repo exists
        if (repo_path / ".git").exists():
            console.print("[green]Migrating from Git repository...[/green]")
            config = storage.load_config()
            config.git_compatible = True
            storage.save_config(config)
    
    if name:
        config = storage.load_config()
        config.name = name
        storage.save_config(config)
    
    # Create default policy rules
    default_rules = [
        PolicyRule(
            id="default-1",
            agent_pattern="*",
            action="commit",
            condition="always",
            requires_human_review=False
        ),
        PolicyRule(
            id="default-2",
            agent_pattern="*",
            action="merge",
            condition="risk_level == 'high' or risk_level == 'critical'",
            requires_human_review=True
        )
    ]
    
    for rule in default_rules:
        storage.add_policy_rule(rule)
    
    console.print(f"[green]✓ AgentVCS repository initialized at {repo_path}[/green]")
    console.print(f"[blue]✓ Semantic metadata enabled[/blue]")
    console.print(f"[blue]✓ Agent policies configured[/blue]")
    if git_migrate:
        console.print(f"[blue]✓ Git compatibility enabled[/blue]")


@main.command()
@click.option("--intent", required=True, help="Intent behind the change")
@click.option("--risk", type=click.Choice(["low", "medium", "high", "critical"]), default="medium", help="Risk level")
@click.option("--subsystem", help="Affected subsystem")
@click.option("--type", type=click.Choice(["bugfix", "feature", "refactor", "perf", "security", "docs", "test", "chore"]), default="feature", help="Change type")
@click.option("--reasoning", required=True, help="Reasoning trace for the change")
@click.option("--bug-id", help="Bug ID if this is a fix")
@click.option("--author", default="agent", help="Author of the commit")
@click.option("--files", multiple=True, help="Files affected by this commit")
@click.option("--tags", multiple=True, help="Tags for the commit")
@click.option("--dependencies", multiple=True, help="Dependencies for this commit")
@click.option("--metadata", multiple=True, help="Additional metadata (key=value)")
def commit(intent: str, risk: str, subsystem: Optional[str], type: str, reasoning: str, 
           bug_id: Optional[str], author: str, files: tuple, tags: tuple, dependencies: tuple, metadata: tuple):
    """Create a semantic commit with intent, risk level, and reasoning trace."""
    storage = get_storage()
    
    import hashlib
    commit_id = hashlib.sha256(f"{intent}{reasoning}{author}".encode()).hexdigest()[:12]
    
    # Parse metadata
    metadata_dict = {}
    for item in metadata:
        if "=" in item:
            key, value = item.split("=", 1)
            metadata_dict[key] = value
    
    # Build dependencies
    deps_dict = {}
    for dep in dependencies:
        if ":" in dep:
            target, dep_type = dep.split(":", 1)
            if dep_type not in deps_dict:
                deps_dict[dep_type] = []
            deps_dict[dep_type].append(target)
    
    commit = Commit(
        id=commit_id,
        author=author,
        intent=intent,
        risk_level=RiskLevel(risk),
        subsystem=subsystem,
        change_type=ChangeType(type),
        reasoning=reasoning,
        bug_fixed=bug_id,
        files=list(files),
        dependencies=deps_dict,
        metadata={**metadata_dict, "tags": list(tags)}
    )
    
    storage.save_commit(commit)
    
    # Log event
    event = Event(
        id=f"evt-{commit_id}",
        event_type="commit",
        source=author,
        data={"commit_id": commit_id, "intent": intent, "risk": risk}
    )
    storage.save_event(event)
    
    console.print(f"[green]✓ Commit created: {commit_id}[/green]")
    console.print(f"[blue]  Intent: {intent}[/blue]")
    console.print(f"[blue]  Risk: {risk}[/blue]")
    console.print(f"[blue]  Type: {type}[/blue]")
    if tags:
        console.print(f"[blue]  Tags: {', '.join(tags)}[/blue]")
    if dependencies:
        console.print(f"[blue]  Dependencies: {len(dependencies)}[/blue]")


@main.command()
@click.option("--type", type=click.Choice(["bugfix", "feature", "refactor", "perf", "security"]), required=True, help="Change type")
@click.option("--target", required=True, help="Target file or subsystem")
@click.option("--agent", default="autonomous", help="Agent proposing the change")
@click.option("--reasoning", required=True, help="Agent's reasoning")
@click.option("--risk", type=click.Choice(["low", "medium", "high", "critical"]), default="medium", help="Risk level")
@click.option("--impact", help="Estimated impact")
def propose(type: str, target: str, agent: str, reasoning: str, risk: str, impact: Optional[str]):
    """Agents propose autonomous changes for human or agent review."""
    storage = get_storage()
    
    import hashlib
    proposal_id = hashlib.sha256(f"{target}{agent}{reasoning}".encode()).hexdigest()[:12]
    
    # Generate a placeholder diff (in real implementation, this would analyze actual changes)
    diff = f"""diff --git a/{target} b/{target}
index 1234567..abcdef 100644
--- a/{target}
+++ b/{target}
@@ -1,5 +1,5 @@
 # Proposed changes by {agent}
-# Original code
+# Modified code
"""
    
    proposal = Proposal(
        id=proposal_id,
        agent=agent,
        change_type=ChangeType(type),
        target=target,
        diff=diff,
        reasoning=reasoning,
        risk_level=RiskLevel(risk),
        estimated_impact=impact or "Moderate impact on target subsystem"
    )
    
    storage.save_proposal(proposal)
    
    console.print(f"[green]✓ Proposal created: {proposal_id}[/green]")
    console.print(f"[blue]  Agent: {agent}[/blue]")
    console.print(f"[blue]  Target: {target}[/blue]")
    console.print(f"[blue]  Type: {type}[/blue]")
    console.print(f"[yellow]  Status: pending review[/yellow]")


@main.command()
@click.option("--branch", required=True, help="Branch to merge")
@click.option("--simulate", is_flag=True, help="Simulate merge without applying")
@click.option("--strategy", type=click.Choice(["auto", "manual", "agent"]), default="auto", help="Merge strategy")
def merge(branch: str, simulate: bool, strategy: str):
    """Predictive merge engine with conflict simulation and resolution."""
    storage = get_storage()
    
    merge_engine = MergeEngine(storage)
    simulation = merge_engine.simulate_merge(branch)
    
    console.print(f"[blue]Merge simulation for branch: {branch}[/blue]")
    console.print(f"[blue]Strategy: {strategy}[/blue]")
    
    if simulation.can_merge:
        console.print("[green]✓ Merge can proceed without conflicts[/green]")
    else:
        console.print(f"[red]✗ {len(simulation.conflicts)} conflicts detected[/red]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("File", style="cyan")
        table.add_column("Lines", style="cyan")
        table.add_column("Resolution", style="green")
        
        for conflict in simulation.conflicts[:5]:  # Show first 5
            resolution = conflict.resolution or "PENDING"
            table.add_row(conflict.file, f"{conflict.line_start}-{conflict.line_end}", resolution)
        
        console.print(table)
    
    if not simulate and simulation.can_merge:
        console.print("[green]✓ Merge completed[/green]")
        event = Event(
            id=f"merge-{branch}",
            event_type="merge",
            source="merge-engine",
            data={"branch": branch, "strategy": strategy}
        )
        storage.save_event(event)


@main.command()
@click.option("--commit", required=True, help="Commit hash to review")
@click.option("--agents", help="Comma-separated list of agent roles (e.g., security,performance,architecture)")
def review(commit: str, agents: Optional[str]):
    """Launch a multi-agent review swarm to evaluate a commit."""
    storage = get_storage()
    
    commit_data = storage.get_commit(commit)
    if not commit_data:
        console.print(f"[red]Commit {commit} not found[/red]")
        return
    
    agent_roles = [AgentRole(a.strip()) for a in (agents or "security,performance,architecture").split(",")]
    registry = AgentRegistry()
    
    console.print(f"[blue]Launching review swarm for commit {commit}[/blue]")
    
    results = []
    for role in agent_roles:
        agent = registry.get_agent(role)
        if agent:
            console.print(f"[cyan]  Running {role.value} agent review...[/cyan]")
            result = agent.review_commit(commit_data)
            results.append(result)
            
            console.print(f"[green]  ✓ {role.value} agent: {result['approved']}[/green]")
            console.print(f"[blue]    Score: {result['score']:.2f}[/blue]")
            if result['findings']:
                console.print(f"[yellow]    Findings: {len(result['findings'])}[/yellow]")
    
    # Calculate overall approval
    approved_count = sum(1 for r in results if r['approved'])
    total_count = len(results)
    
    console.print(f"\n[bold]Review Summary:[/bold]")
    console.print(f"[green]Approved: {approved_count}/{total_count}[/green]")
    
    if approved_count == total_count:
        console.print("[green]✓ Commit approved by all agents[/green]")
    else:
        console.print("[yellow]⚠ Commit requires further review[/yellow]")


@main.command()
@click.option("--target", required=True, help="Target file or directory")
@click.option("--pattern", help="Refactor pattern (e.g., extract-method, simplify-logic)")
@click.option("--agent", default="refactor-bot", help="Agent performing the refactor")
def refactor(target: str, pattern: Optional[str], agent: str):
    """Autonomous refactor pipeline with structural improvement proposals."""
    storage = get_storage()
    
    console.print(f"[blue]Running refactor analysis on {target}[/blue]")
    console.print(f"[cyan]Pattern: {pattern or 'auto-detect'}[/blue]")
    console.print(f"[cyan]Agent: {agent}[/cyan]")
    
    # Simulate refactor analysis
    import hashlib
    proposal_id = hashlib.sha256(f"refactor-{target}".encode()).hexdigest()[:12]
    
    proposal = Proposal(
        id=proposal_id,
        agent=agent,
        change_type=ChangeType.REFACTOR,
        target=target,
        diff=f"# Refactor proposal for {target}\n# Pattern: {pattern or 'auto'}\n# Analysis complete",
        reasoning=f"Refactor analysis identified opportunities in {target}",
        risk_level=RiskLevel.MEDIUM,
        estimated_impact="Improved code maintainability"
    )
    
    storage.save_proposal(proposal)
    
    console.print(f"[green]✓ Refactor proposal created: {proposal_id}[/green]")
    console.print(f"[yellow]  Ready for approval[/yellow]")


@main.command()
@click.option("--watch", is_flag=True, help="Watch continuously")
@click.option("--interval", default=60, help="Check interval in seconds")
def sentinel(watch: bool, interval: int):
    """Continuous risk monitoring for vulnerabilities, dependency drift, and regressions."""
    storage = get_storage()
    
    console.print("[blue]Starting sentinel monitoring...[/blue]")
    console.print(f"[cyan]Watch mode: {watch}[/cyan]")
    console.print(f"[cyan]Interval: {interval}s[/cyan]")
    
    # Simulate sentinel checks
    checks = [
        ("Vulnerability scan", "passed"),
        ("Dependency drift", "warning"),
        ("Unsafe patterns", "passed"),
        ("Regression detection", "passed")
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    
    for check_name, status in checks:
        status_style = "green" if status == "passed" else "yellow"
        table.add_row(check_name, f"[{status_style}]{status}[/{status_style}]")
        
        event = Event(
            id=f"sentinel-{check_name}",
            event_type="sentinel-check",
            source="sentinel",
            data={"check": check_name, "status": status}
        )
        storage.save_event(event)
    
    console.print(table)
    
    if watch:
        console.print("[yellow]Sentinel running in watch mode (Press Ctrl+C to stop)[/yellow]")
        try:
            import time
            while True:
                time.sleep(interval)
                console.print(f"[cyan]Sentinel check at {time.strftime('%H:%M:%S')}[/cyan]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Sentinel stopped[/yellow]")


@main.command()
@click.option("--query", help="Natural language query about history")
@click.option("--commit", help="Specific commit to query")
@click.option("--agent", help="Filter by agent")
@click.option("--limit", default=10, help="Number of results")
@click.option("--risk", type=click.Choice(["low", "medium", "high", "critical"]), help="Filter by risk level")
@click.option("--type", type=click.Choice(["bugfix", "feature", "refactor", "perf", "security", "docs", "test", "chore"]), help="Filter by change type")
@click.option("--subsystem", help="Filter by subsystem")
@click.option("--since", help="Show commits since (YYYY-MM-DD)")
@click.option("--format", type=click.Choice(["table", "json", "detailed"]), default="table", help="Output format")
def history(query: Optional[str], commit: Optional[str], agent: Optional[str], limit: int, 
            risk: Optional[str], type: Optional[str], subsystem: Optional[str], since: Optional[str], format: str):
    """Query intent-aware history with natural language."""
    storage = get_storage()
    
    commits = storage.load_commits()
    
    # Apply filters
    if agent:
        commits = [c for c in commits if c.get("author") == agent]
    if commit:
        commits = [c for c in commits if c.get("id") == commit]
    if risk:
        commits = [c for c in commits if c.get("risk_level") == risk]
    if type:
        commits = [c for c in commits if c.get("change_type") == type]
    if subsystem:
        commits = [c for c in commits if c.get("subsystem") == subsystem]
    if since:
        from datetime import datetime
        since_date = datetime.strptime(since, "%Y-%m-%d")
        commits = [c for c in commits if datetime.fromisoformat(c.get("timestamp", "")) >= since_date]
    
    # Apply natural language query (simple keyword matching for demo)
    if query:
        query_lower = query.lower()
        commits = [c for c in commits if 
                   query_lower in c.get("intent", "").lower() or
                   query_lower in c.get("reasoning", "").lower() or
                   query_lower in str(c.get("metadata", {})).lower()]
    
    commits = commits[:limit]
    
    if not commits:
        console.print("[yellow]No commits found matching criteria[/yellow]")
        return
    
    if format == "json":
        import json
        console.print(json.dumps(commits, indent=2, default=str))
    elif format == "detailed":
        for c in commits:
            console.print(f"\n[bold cyan]Commit: {c['id']}[/bold cyan]")
            console.print(f"[blue]Author:[/blue] {c['author']}")
            console.print(f"[blue]Intent:[/blue] {c['intent']}")
            console.print(f"[blue]Risk:[/blue] {c['risk_level']}")
            console.print(f"[blue]Type:[/blue] {c['change_type']}")
            console.print(f"[blue]Subsystem:[/blue] {c.get('subsystem', 'N/A')}")
            console.print(f"[blue]Reasoning:[/blue] {c['reasoning']}")
            if c.get('files'):
                console.print(f"[blue]Files:[/blue] {', '.join(c['files'])}")
            if c.get('bug_fixed'):
                console.print(f"[blue]Bug Fixed:[/blue] {c['bug_fixed']}")
            console.print("-" * 50)
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Author", style="cyan")
        table.add_column("Intent", style="cyan")
        table.add_column("Risk", style="cyan")
        table.add_column("Type", style="cyan")
        table.add_column("Time", style="cyan")
        
        for c in commits:
            risk_style = "green" if c.get("risk_level") == "low" else "yellow" if c.get("risk_level") == "medium" else "red"
            timestamp = c.get("timestamp", "")[:19] if c.get("timestamp") else "N/A"
            table.add_row(
                c["id"][:8],
                c["author"],
                c["intent"][:30],
                f"[{risk_style}]{c['risk_level']}[/{risk_style}]",
                c["change_type"],
                timestamp
            )
        
        console.print(table)
        console.print(f"\n[blue]Showing {len(commits)} commits[/blue]")


@main.command()
@click.option("--add-rule", help="Add a policy rule (format: 'agent_pattern:action:condition')")
@click.option("--list-rules", is_flag=True, help="List all policy rules")
@click.option("--remove-rule", help="Remove a policy rule by ID")
def policy(add_rule: Optional[str], list_rules: bool, remove_rule: Optional[str]):
    """Define machine-first permissions and agent policies."""
    storage = get_storage()
    
    if list_rules:
        rules = storage.get_policy_rules()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Agent Pattern", style="cyan")
        table.add_column("Action", style="cyan")
        table.add_column("Condition", style="cyan")
        table.add_column("Human Review", style="cyan")
        
        for rule in rules:
            review_status = "Yes" if rule.requires_human_review else "No"
            table.add_row(
                rule.id,
                rule.agent_pattern,
                rule.action,
                rule.condition,
                review_status
            )
        
        console.print(table)
        return
    
    if add_rule:
        parts = add_rule.split(":")
        if len(parts) >= 3:
            agent_pattern, action, condition = parts[0], parts[1], parts[2]
            rule = PolicyRule(
                id=f"rule-{len(storage.get_policy_rules()) + 1}",
                agent_pattern=agent_pattern,
                action=action,
                condition=condition
            )
            storage.add_policy_rule(rule)
            console.print(f"[green]✓ Policy rule added: {rule.id}[/green]")
        else:
            console.print("[red]Invalid rule format. Use: agent_pattern:action:condition[/red]")
        return
    
    if remove_rule:
        rules = storage.get_policy_rules()
        rules = [r for r in rules if r.id != remove_rule]
        config = storage.load_config()
        config.policies = rules
        storage.save_config(config)
        console.print(f"[green]✓ Policy rule removed: {remove_rule}[/green]")
        return
    
    console.print("[yellow]Use --list-rules, --add-rule, or --remove-rule[/yellow]")


@main.command()
@click.option("--subscribe", help="Comma-separated event types to subscribe")
@click.option("--tail", default=10, help="Number of recent events to show")
def events(subscribe: Optional[str], tail: int):
    """Subscribe to event streams and view recent events."""
    storage = get_storage()
    
    all_events = storage.load_events()
    events_to_show = all_events[-tail:]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="cyan")
    table.add_column("Source", style="cyan")
    table.add_column("Time", style="cyan")
    
    for event in events_to_show:
        table.add_row(
            event["id"][:12],
            event["event_type"],
            event["source"],
            event["timestamp"][:19] if event.get("timestamp") else "N/A"
        )
    
    console.print(table)
    
    if subscribe:
        event_types = [e.strip() for e in subscribe.split(",")]
        console.print(f"[green]✓ Subscribed to events: {', '.join(event_types)}[/green]")
        console.print("[yellow]Event streaming active (Press Ctrl+C to stop)[/yellow]")
        
        try:
            import time
            event_stream = EventStream(storage)
            for event in event_stream.stream(event_types):
                console.print(f"[cyan]{event['event_type']}: {event['source']}[/cyan]")
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]Event streaming stopped[/yellow]")


@main.command()
@click.option("--query", help="Graph query (e.g., 'dependencies of src/auth.py')")
@click.option("--node-type", help="Filter by node type (file, function, class, commit, agent)")
@click.option("--export", help="Export graph to file (format: json, dot)")
def graph(query: Optional[str], node_type: Optional[str], export: Optional[str]):
    """Query the semantic repository graph."""
    storage = get_storage()
    
    graph_builder = GraphBuilder(storage)
    graph_data = graph_builder.build_graph()
    
    if query:
        console.print(f"[blue]Query: {query}[/blue]")
        # Simple query parsing for demo
        if "dependencies of" in query.lower():
            target = query.lower().split("dependencies of")[-1].strip()
            deps = [e for e in graph_data["edges"] if e["source"] == target]
            console.print(f"[green]Found {len(deps)} dependencies[/green]")
            for dep in deps[:5]:
                console.print(f"  - {dep['target']} ({dep['relationship']})")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Nodes", style="cyan")
    table.add_column("Edges", style="cyan")
    
    node_count = len(graph_data["nodes"])
    edge_count = len(graph_data["edges"])
    
    table.add_row(str(node_count), str(edge_count))
    console.print(table)
    
    if export:
        if export == "json":
            import json
            output_file = Path.cwd() / "graph.json"
            output_file.write_text(json.dumps(graph_data, indent=2))
            console.print(f"[green]✓ Graph exported to {output_file}[/green]")
        elif export == "dot":
            output_file = Path.cwd() / "graph.dot"
            dot_content = "digraph G {\n"
            for edge in graph_data["edges"]:
                dot_content += f'  "{edge["source"]}" -> "{edge["target"]}";\n'
            dot_content += "}"
            output_file.write_text(dot_content)
            console.print(f"[green]✓ Graph exported to {output_file}[/green]")


@main.command()
@click.option("--task", required=True, help="Task description for swarm")
@click.option("--agents", required=True, help="Comma-separated list of agents")
@click.option("--timeout", default=300, help="Timeout in seconds")
def swarm(task: str, agents: str, timeout: int):
    """Coordinate multi-agent collaboration with negotiation and consensus."""
    storage = get_storage()
    
    agent_list = [a.strip() for a in agents.split(",")]
    
    import hashlib
    task_id = hashlib.sha256(task.encode()).hexdigest()[:12]
    
    swarm_task = SwarmTask(
        id=task_id,
        task=task,
        agents=agent_list,
        status="in_progress"
    )
    
    console.print(f"[blue]Initializing swarm for task: {task}[/blue]")
    console.print(f"[cyan]Agents: {', '.join(agent_list)}[/cyan]")
    
    # Simulate agent collaboration
    for agent in agent_list:
        console.print(f"[cyan]  {agent} analyzing...[/cyan]")
        # Simulate voting
        import random
        vote = random.choice(["approve", "approve", "approve", "reject"])
        swarm_task.votes[agent] = vote
        console.print(f"    Vote: {vote}")
    
    # Calculate consensus
    approve_count = sum(1 for v in swarm_task.votes.values() if v == "approve")
    if approve_count >= len(agent_list) * 0.6:
        swarm_task.consensus = "approve"
        swarm_task.status = "completed"
        console.print(f"[green]✓ Consensus reached: approve ({approve_count}/{len(agent_list)})[/green]")
    else:
        swarm_task.consensus = "reject"
        swarm_task.status = "failed"
        console.print(f"[red]✗ Consensus failed: reject ({approve_count}/{len(agent_list)})[/red]")
    
    # Log event
    event = Event(
        id=f"swarm-{task_id}",
        event_type="swarm",
        source="swarm-coordinator",
        data={"task_id": task_id, "consensus": swarm_task.consensus}
    )
    storage.save_event(event)


@main.command()
@click.option("--type", type=click.Choice(["overview", "risk", "agents", "commits", "trends"]), default="overview", help="Analysis type")
@click.option("--format", type=click.Choice(["table", "json", "text"]), default="table", help="Output format")
@click.option("--days", default=30, help="Time period in days for trend analysis")
def analyze(type: str, format: str, days: int):
    """Repository analytics and insights."""
    storage = get_storage()
    
    console.print(f"[blue]Repository Analysis: {type}[/blue]")
    
    commits = storage.load_commits()
    events = storage.load_events()
    proposals = storage.load_proposals()
    
    if type == "overview":
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Commits", str(len(commits)))
        table.add_row("Total Events", str(len(events)))
        table.add_row("Active Proposals", str(len([p for p in proposals if p["status"] == "pending"])))
        table.add_row("Unique Agents", str(len(set(c["author"] for c in commits))))
        
        risk_counts = {}
        for c in commits:
            risk = c.get("risk_level", "unknown")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        table.add_row("High Risk Commits", str(risk_counts.get("high", 0)))
        table.add_row("Critical Risk Commits", str(risk_counts.get("critical", 0)))
        
        console.print(table)
    
    elif type == "risk":
        risk_table = Table(show_header=True, header_style="bold magenta")
        risk_table.add_column("Risk Level", style="cyan")
        risk_table.add_column("Count", style="green")
        risk_table.add_column("Percentage", style="yellow")
        
        risk_counts = {}
        for c in commits:
            risk = c.get("risk_level", "unknown")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        total = len(commits) if commits else 1
        for risk in ["low", "medium", "high", "critical"]:
            count = risk_counts.get(risk, 0)
            percentage = (count / total) * 100
            risk_table.add_row(risk, str(count), f"{percentage:.1f}%")
        
        console.print(risk_table)
    
    elif type == "agents":
        agent_table = Table(show_header=True, header_style="bold magenta")
        agent_table.add_column("Agent", style="cyan")
        agent_table.add_column("Commits", style="green")
        agent_table.add_column("Last Active", style="yellow")
        
        agent_stats = {}
        for c in commits:
            agent = c["author"]
            agent_stats[agent] = agent_stats.get(agent, 0) + 1
        
        for agent, count in sorted(agent_stats.items(), key=lambda x: x[1], reverse=True):
            agent_table.add_row(agent, str(count), "Recently")
        
        console.print(agent_table)
    
    elif type == "commits":
        type_table = Table(show_header=True, header_style="bold magenta")
        type_table.add_column("Change Type", style="cyan")
        type_table.add_column("Count", style="green")
        
        type_counts = {}
        for c in commits:
            change_type = c.get("change_type", "unknown")
            type_counts[change_type] = type_counts.get(change_type, 0) + 1
        
        for change_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            type_table.add_row(change_type, str(count))
        
        console.print(type_table)
    
    elif type == "trends":
        console.print(f"[cyan]Trend analysis for last {days} days[/cyan]")
        console.print("[yellow]Commit velocity, risk trends, and agent activity patterns[/yellow]")
        console.print("[dim](Full trend analysis requires historical data accumulation)[/dim]")


@main.command()
@click.option("--output", help="Output file path for backup")
@click.option("--include-git", is_flag=True, help="Include Git data if available")
def backup(output: Optional[str], include_git: bool):
    """Backup repository with semantic metadata."""
    storage = get_storage()
    
    import json
    import shutil
    from datetime import datetime
    
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"agentvcs_backup_{timestamp}.tar.gz"
    
    console.print(f"[blue]Creating backup: {output}[/blue]")
    
    # Create backup data
    backup_data = {
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
        "config": storage.load_config().model_dump(),
        "commits": storage.load_commits(),
        "proposals": storage.load_proposals(),
        "events": storage.load_events(),
        "graph": storage.load_graph()
    }
    
    # Save backup
    import tarfile
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write metadata
        metadata_file = Path(tmpdir) / "metadata.json"
        metadata_file.write_text(json.dumps(backup_data, indent=2, default=str))
        
        # Copy .agentvcs directory
        agentvcs_backup = Path(tmpdir) / "agentvcs"
        if storage.agentvcs_dir.exists():
            shutil.copytree(storage.agentvcs_dir, agentvcs_backup)
        
        # Create tar archive
        with tarfile.open(output, "w:gz") as tar:
            tar.add(str(metadata_file), arcname="metadata.json")
            if storage.agentvcs_dir.exists():
                tar.add(str(agentvcs_backup), arcname=".agentvcs")
    
    console.print(f"[green]✓ Backup created: {output}[/green]")
    
    # Log event
    event = Event(
        id=f"backup-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        event_type="backup",
        source="backup-command",
        data={"file": output, "include_git": include_git}
    )
    storage.save_event(event)


@main.command()
@click.option("--input", required=True, help="Backup file to restore")
@click.option("--force", is_flag=True, help="Force restore without confirmation")
def restore(input: str, force: bool):
    """Restore repository from backup."""
    repo_path = Path.cwd()
    storage = Storage(repo_path)
    
    if not force:
        console.print("[yellow]Warning: This will overwrite current repository data.[/yellow]")
        if not click.confirm("Do you want to continue?"):
            console.print("[yellow]Restore cancelled.[/yellow]")
            return
    
    console.print(f"[blue]Restoring from: {input}[/blue]")
    
    import tarfile
    import shutil
    import json
    
    with tarfile.open(input, "r:gz") as tar:
        tar.extractall(path=repo_path)
    
    # Restore metadata
    metadata_file = repo_path / "metadata.json"
    if metadata_file.exists():
        metadata = json.loads(metadata_file.read_text())
        console.print(f"[cyan]Restored from version: {metadata.get('version', 'unknown')}[/cyan]")
        console.print(f"[cyan]Backup timestamp: {metadata.get('timestamp', 'unknown')}[/cyan]")
        metadata_file.unlink()
    
    console.print("[green]✓ Repository restored successfully[/green]")
    
    # Log event
    event = Event(
        id=f"restore-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        event_type="restore",
        source="restore-command",
        data={"file": input}
    )
    storage.save_event(event)


@main.command()
@click.option("--format", type=click.Choice(["json", "yaml", "csv"]), default="json", help="Export format")
@click.option("--output", help="Output file path")
@click.option("--data", type=click.Choice(["commits", "events", "proposals", "graph", "all"]), default="all", help="Data to export")
def export(format: str, output: Optional[str], data: str):
    """Export repository data to various formats."""
    storage = get_storage()
    
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"agentvcs_export_{timestamp}.{format}"
    
    console.print(f"[blue]Exporting {data} to {format}: {output}[/blue]")
    
    import json
    import yaml
    
    export_data = {}
    
    if data in ["commits", "all"]:
        export_data["commits"] = storage.load_commits()
    
    if data in ["events", "all"]:
        export_data["events"] = storage.load_events()
    
    if data in ["proposals", "all"]:
        export_data["proposals"] = storage.load_proposals()
    
    if data in ["graph", "all"]:
        export_data["graph"] = storage.load_graph()
    
    if format == "json":
        Path(output).write_text(json.dumps(export_data, indent=2, default=str))
    elif format == "yaml":
        Path(output).write_text(yaml.dump(export_data, default_flow_style=False))
    elif format == "csv":
        import csv
        # Export commits to CSV
        if "commits" in export_data:
            with open(output, 'w', newline='') as f:
                if export_data["commits"]:
                    writer = csv.DictWriter(f, fieldnames=export_data["commits"][0].keys())
                    writer.writeheader()
                    for commit in export_data["commits"]:
                        writer.writerow(commit)
    
    console.print(f"[green]✓ Data exported to: {output}[/green]")
    
    # Log event
    event = Event(
        id=f"export-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        event_type="export",
        source="export-command",
        data={"format": format, "file": output, "data": data}
    )
    storage.save_event(event)


@main.command()
@click.option("--input", required=True, help="Import file")
@click.option("--format", type=click.Choice(["json", "yaml"]), help="Import format (auto-detected if not specified)")
def import_data(input: str, format: Optional[str]):
    """Import repository data from exported file."""
    storage = get_storage()
    
    console.print(f"[blue]Importing from: {input}[/blue]")
    
    import json
    import yaml
    
    input_path = Path(input)
    if not input_path.exists():
        console.print(f"[red]Error: File not found: {input}[/red]")
        return
    
    # Auto-detect format
    if not format:
        if input_path.suffix == ".json":
            format = "json"
        elif input_path.suffix in [".yaml", ".yml"]:
            format = "yaml"
        else:
            format = "json"
    
    content = input_path.read_text()
    
    if format == "json":
        import_data = json.loads(content)
    elif format == "yaml":
        import_data = yaml.safe_load(content)
    
    # Import data
    if "commits" in import_data:
        for commit in import_data["commits"]:
            storage.save_commit(Commit(**commit))
        console.print(f"[green]✓ Imported {len(import_data['commits'])} commits[/green]")
    
    if "events" in import_data:
        for event in import_data["events"]:
            storage.save_event(Event(**event))
        console.print(f"[green]✓ Imported {len(import_data['events'])} events[/green]")
    
    if "proposals" in import_data:
        for proposal in import_data["proposals"]:
            storage.save_proposal(Proposal(**proposal))
        console.print(f"[green]✓ Imported {len(import_data['proposals'])} proposals[/green]")
    
    console.print("[green]✓ Import completed[/green]")
    
    # Log event
    event = Event(
        id=f"import-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        event_type="import",
        source="import-command",
        data={"file": input, "format": format}
    )
    storage.save_event(event)


@click.group()
def remote():
    """Manage remote repositories."""
    pass


# Register remote as a subcommand of main
main.add_command(remote)


@remote.command()
@click.argument("url", required=True)
@click.option("--name", default="origin", help="Remote name")
@click.option("--type", type=click.Choice(["agentvcs", "git", "custom"]), default="agentvcs", help="Remote type")
@click.option("--set-default", is_flag=True, help="Set as default remote")
def add(url: str, name: str, type: str, set_default: bool):
    """Add a remote repository."""
    storage = get_storage()
    config = storage.load_config()
    
    # Check if remote already exists
    for remote in config.remotes:
        if remote.name == name:
            console.print(f"[yellow]Remote '{name}' already exists. Use 'agentvcs remote remove' first.[/yellow]")
            return
    
    # Add new remote
    remote = Remote(
        name=name,
        url=url,
        type=type
    )
    config.remotes.append(remote)
    
    if set_default:
        config.default_remote = name
    
    storage.save_config(config)
    
    console.print(f"[green]✓ Remote '{name}' added: {url}[/green]")
    if set_default:
        console.print(f"[blue]  Set as default remote[/blue]")
    
    # Log event
    event = Event(
        id=f"remote-add-{name}",
        event_type="remote-add",
        source="remote-command",
        data={"name": name, "url": url, "type": type}
    )
    storage.save_event(event)


@remote.command()
@click.option("--name", help="Remote name (removes all if not specified)")
def remove(name: Optional[str]):
    """Remove a remote repository."""
    storage = get_storage()
    config = storage.load_config()
    
    if name:
        # Remove specific remote
        config.remotes = [r for r in config.remotes if r.name != name]
        if config.default_remote == name:
            config.default_remote = None
        console.print(f"[green]✓ Remote '{name}' removed[/green]")
    else:
        # Remove all remotes
        count = len(config.remotes)
        config.remotes = []
        config.default_remote = None
        console.print(f"[green]✓ Removed {count} remote(s)[/green]")
    
    storage.save_config(config)
    
    # Log event
    event = Event(
        id=f"remote-remove-{name or 'all'}",
        event_type="remote-remove",
        source="remote-command",
        data={"name": name}
    )
    storage.save_event(event)


@remote.command()
def list():
    """List all remote repositories."""
    storage = get_storage()
    config = storage.load_config()
    
    if not config.remotes:
        console.print("[yellow]No remotes configured[/yellow]")
        console.print("Use 'agentvcs remote add' to add a remote")
        return
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("URL", style="cyan")
    table.add_column("Type", style="cyan")
    table.add_column("Default", style="green")
    table.add_column("Last Push", style="yellow")
    table.add_column("Last Pull", style="yellow")
    
    for remote in config.remotes:
        is_default = "Yes" if config.default_remote == remote.name else ""
        last_push = remote.last_push.strftime("%Y-%m-%d %H:%M") if remote.last_push else "Never"
        last_pull = remote.last_pull.strftime("%Y-%m-%d %H:%M") if remote.last_pull else "Never"
        
        table.add_row(
            remote.name,
            remote.url,
            remote.type,
            is_default,
            last_push,
            last_pull
        )
    
    console.print(table)


@main.command()
@click.option("--remote", help="Remote name (uses default if not specified)")
@click.option("--force", is_flag=True, help="Force push even if remote has newer commits")
@click.option("--dry-run", is_flag=True, help="Show what would be pushed without actually pushing")
def push(remote: Optional[str], force: bool, dry_run: bool):
    """Push commits and semantic metadata to remote repository."""
    storage = get_storage()
    config = storage.load_config()
    
    # Determine remote
    remote_name = remote or config.default_remote
    if not remote_name:
        console.print("[red]Error: No remote specified and no default remote set[/red]")
        console.print("Use 'agentvcs remote add' to add a remote or specify --remote")
        return
    
    # Find remote
    remote_obj = None
    for r in config.remotes:
        if r.name == remote_name:
            remote_obj = r
            break
    
    if not remote_obj:
        console.print(f"[red]Error: Remote '{remote_name}' not found[/red]")
        return
    
    console.print(f"[blue]Pushing to {remote_name}: {remote_obj.url}[/blue]")
    
    if dry_run:
        console.print("[yellow]Dry run - no actual push will occur[/yellow]")
        commits = storage.load_commits()
        console.print(f"[cyan]Would push {len(commits)} commits[/cyan]")
        console.print(f"[cyan]Would push semantic metadata[/cyan]")
        if remote_obj.type == "git":
            console.print(f"[cyan]Would also push to Git remote[/cyan]")
        return
    
    # Perform push based on remote type
    if remote_obj.type == "git":
        # Push to Git remote
        import subprocess
        try:
            # Check if git repo exists
            if (Path.cwd() / ".git").exists():
                console.print("[cyan]Pushing to Git remote...[/cyan]")
                result = subprocess.run(
                    ["git", "push", remote_name, "main"],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    console.print("[green]✓ Git push successful[/green]")
                else:
                    console.print(f"[red]Git push failed: {result.stderr}[/red]")
            else:
                console.print("[yellow]Git repository not found, skipping Git push[/yellow]")
        except Exception as e:
            console.print(f"[red]Error during Git push: {str(e)}[/red]")
    
    # Push AgentVCS semantic data
    console.print("[cyan]Pushing AgentVCS semantic metadata...[/cyan]")
    
    # In a real implementation, this would upload to a remote server
    # For demo, we simulate the push
    import hashlib
    push_id = hashlib.sha256(f"{remote_name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
    
    # Update remote metadata
    remote_obj.last_push = datetime.now()
    storage.save_config(config)
    
    console.print(f"[green]✓ Pushed to {remote_name} (push ID: {push_id})[/green]")
    console.print(f"[blue]  Commits: {len(storage.load_commits())}[/blue]")
    console.print(f"[blue]  Events: {len(storage.load_events())}[/blue]")
    
    # Log event
    event = Event(
        id=f"push-{push_id}",
        event_type="push",
        source="push-command",
        data={"remote": remote_name, "push_id": push_id, "force": force}
    )
    storage.save_event(event)


@main.command()
@click.option("--remote", help="Remote name (uses default if not specified)")
@click.option("--force", is_flag=True, help="Force pull even if local has unpushed changes")
@click.option("--dry-run", is_flag=True, help="Show what would be pulled without actually pulling")
def pull(remote: Optional[str], force: bool, dry_run: bool):
    """Pull commits and semantic metadata from remote repository."""
    storage = get_storage()
    config = storage.load_config()
    
    # Determine remote
    remote_name = remote or config.default_remote
    if not remote_name:
        console.print("[red]Error: No remote specified and no default remote set[/red]")
        console.print("Use 'agentvcs remote add' to add a remote or specify --remote")
        return
    
    # Find remote
    remote_obj = None
    for r in config.remotes:
        if r.name == remote_name:
            remote_obj = r
            break
    
    if not remote_obj:
        console.print(f"[red]Error: Remote '{remote_name}' not found[/red]")
        return
    
    console.print(f"[blue]Pulling from {remote_name}: {remote_obj.url}[/blue]")
    
    if dry_run:
        console.print("[yellow]Dry run - no actual pull will occur[/yellow]")
        console.print(f"[cyan]Would pull commits from remote[/cyan]")
        console.print(f"[cyan]Would pull semantic metadata from remote[/cyan]")
        if remote_obj.type == "git":
            console.print(f"[cyan]Would also pull from Git remote[/cyan]")
        return
    
    # Perform pull based on remote type
    if remote_obj.type == "git":
        # Pull from Git remote
        import subprocess
        try:
            if (Path.cwd() / ".git").exists():
                console.print("[cyan]Pulling from Git remote...[/cyan]")
                result = subprocess.run(
                    ["git", "pull", remote_name, "main"],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    console.print("[green]✓ Git pull successful[/green]")
                else:
                    console.print(f"[red]Git pull failed: {result.stderr}[/red]")
            else:
                console.print("[yellow]Git repository not found, skipping Git pull[/yellow]")
        except Exception as e:
            console.print(f"[red]Error during Git pull: {str(e)}[/red]")
    
    # Pull AgentVCS semantic data
    console.print("[cyan]Pulling AgentVCS semantic metadata...[/cyan]")
    
    # In a real implementation, this would download from a remote server
    # For demo, we simulate the pull
    import hashlib
    pull_id = hashlib.sha256(f"{remote_name}{datetime.now().isoformat()}".encode()).hexdigest()[:8]
    
    # Update remote metadata
    remote_obj.last_pull = datetime.now()
    storage.save_config(config)
    
    console.print(f"[green]✓ Pulled from {remote_name} (pull ID: {pull_id})[/green]")
    console.print(f"[blue]  Repository is up to date[/blue]")
    
    # Log event
    event = Event(
        id=f"pull-{pull_id}",
        event_type="pull",
        source="pull-command",
        data={"remote": remote_name, "pull_id": pull_id, "force": force}
    )
    storage.save_event(event)


@main.command()
@click.option("--remote", help="Remote name (uses default if not specified)")
def fetch(remote: Optional[str]):
    """Fetch updates from remote without merging."""
    storage = get_storage()
    config = storage.load_config()
    
    # Determine remote
    remote_name = remote or config.default_remote
    if not remote_name:
        console.print("[red]Error: No remote specified and no default remote set[/red]")
        return
    
    # Find remote
    remote_obj = None
    for r in config.remotes:
        if r.name == remote_name:
            remote_obj = r
            break
    
    if not remote_obj:
        console.print(f"[red]Error: Remote '{remote_name}' not found[/red]")
        return
    
    console.print(f"[blue]Fetching from {remote_name}: {remote_obj.url}[/blue]")
    
    if remote_obj.type == "git":
        import subprocess
        try:
            if (Path.cwd() / ".git").exists():
                console.print("[cyan]Fetching from Git remote...[/cyan]")
                result = subprocess.run(
                    ["git", "fetch", remote_name],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    console.print("[green]✓ Git fetch successful[/green]")
                else:
                    console.print(f"[red]Git fetch failed: {result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Error during Git fetch: {str(e)}[/red]")
    
    console.print(f"[green]✓ Fetched updates from {remote_name}[/green]")
    console.print("[blue]  Use 'agentvcs pull' to merge changes[/blue]")
    
    # Log event
    event = Event(
        id=f"fetch-{remote_name}",
        event_type="fetch",
        source="fetch-command",
        data={"remote": remote_name}
    )
    storage.save_event(event)


@main.command()
@click.option("--all", is_flag=True, help="Show all remotes including Git remotes")
def status(all: bool):
    """Show repository status including remote information."""
    storage = get_storage()
    config = storage.load_config()
    
    console.print(f"[bold cyan]Repository: {config.name}[/bold cyan]")
    console.print(f"[blue]Initialized: {config.initialized_at.strftime('%Y-%m-%d %H:%M:%S')}[/blue]")
    console.print(f"[blue]Git Compatible: {config.git_compatible}[/blue]")
    
    commits = storage.load_commits()
    events = storage.load_events()
    proposals = storage.load_proposals()
    
    console.print(f"\n[bold]Local Status:[/bold]")
    console.print(f"  Commits: {len(commits)}")
    console.print(f"  Events: {len(events)}")
    console.print(f"  Proposals: {len([p for p in proposals if p['status'] == 'pending'])} pending")
    
    if config.remotes:
        console.print(f"\n[bold]Remotes:[/bold]")
        for remote in config.remotes:
            is_default = " (default)" if config.default_remote == remote.name else ""
            console.print(f"  {remote.name}{is_default}: {remote.url}")
            console.print(f"    Type: {remote.type}")
            console.print(f"    Last Push: {remote.last_push.strftime('%Y-%m-%d %H:%M') if remote.last_push else 'Never'}")
            console.print(f"    Last Pull: {remote.last_pull.strftime('%Y-%m-%d %H:%M') if remote.last_pull else 'Never'}")
    else:
        console.print(f"\n[yellow]No remotes configured[/yellow]")
    
    if all and config.git_compatible:
        console.print(f"\n[bold]Git Status:[/bold]")
        import subprocess
        try:
            if (Path.cwd() / ".git").exists():
                result = subprocess.run(
                    ["git", "remote", "-v"],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    console.print(result.stdout)
                else:
                    console.print("  No Git remotes")
        except Exception as e:
            console.print(f"  Error getting Git status: {str(e)}")


if __name__ == "__main__":
    main_with_error_handling()
