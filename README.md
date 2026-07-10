# AgentVCS

![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Agents](https://img.shields.io/badge/agents-first-purple.svg)
![GitHub Actions Status](https://github.com/live-by-unix/AgentVCS/actions/workflows/main.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/agentvcs.svg)

The world's first agentic version control system — a git-like VCS (version control system) built for agents where humans are second priority and agents are first.

<img width="1264" height="1264" alt="AgentVCS Robot Open Source Logo" src="https://github.com/user-attachments/assets/fc15622c-7194-4812-8628-a16a668f01e3" />


## Overview

AgentVCS is a semantic, agent-native version control system designed for autonomous AI workflows. Unlike traditional VCS tools built for human collaboration, AgentVCS prioritizes agent autonomy with:

- **Semantic commits** with intent, risk levels, and reasoning traces
- **Multi-agent review swarms** for security, performance, and architecture
- **Predictive merge engine** that simulates and resolves conflicts before they occur
- **Machine-first permissions** and policy enforcement
- **Intent-aware history** queries for understanding change rationale
- **Continuous risk monitoring** with sentinel agents
- **Event streaming** for real-time awareness
- **Semantic repository graphs** for dependency and impact analysis
- **Remote repository support** with Git-compatible push/pull operations
- **Backup and restore** capabilities for data safety

## Why AgentVCS
AgentVCS, as the name suggested was made for agents.      
There are many reasons to use AgentVCS for your agents.    
One of them are the fact that with the normal Git VCS, the AI has to invesigate diffs, find intent, then work. With AgentVCS, the intent is already defined, so it uses less tokens.    
Another use case is AgentVCS's risk levels, allowing for autonomous agents like Devin to analyze and see if the commit should be reversed.    


## Installation

1. Using PIP install from PyPi index
To install, run this
```bash
pip install agentvcs
```
Then run
```bash
agentvcs --version
```
If it outputs a number, hooray!

2. Install from source code
This is for advanced purposes only.
Clone source code:

```bash
git clone https://github.com/live-by-unix/agentvcs.git
```
OR 
Download latest release & unzip. 
Then `cd` into your downloaded version of AgentVCS and run:

```bash
pip install -e . 
```
Switch pip for pip3 if you need to.

## Quick Start

```bash
# Initialize a new agent-native repository
agentvcs init --name my-project

# Add a remote repository (Git-compatible)
agentvcs remote add origin https://github.com/user/repo --type git --set-default

# Make a semantic commit with full context
agentvcs commit --intent "fix authentication bug" \
                --risk medium \
                --subsystem auth \
                --reasoning "JWT validation was failing due to clock skew" \
                --tags security,auth

# Push to remote repository
agentvcs push

# View repository status
agentvcs status --all

# Query intent-aware history
agentvcs history --format detailed

# Launch multi-agent review
agentvcs review --commit abc123 --agents security,performance,architecture

# Analyze repository
agentvcs analyze --type risk
```

## Complete Command Reference

### Repository Management

#### `agentvcs init`
Initialize a new agent-native repository with semantic metadata and agent policies.

**Options:**
- `--git-migrate`: Migrate from existing Git repository
- `--name`: Repository name

**Example:**
```bash
agentvcs init --name my-project --git-migrate
```

#### `agentvcs status`
Show repository status including remote information and commit counts.

**Options:**
- `--all`: Show all remotes including Git remotes

**Example:**
```bash
agentvcs status --all
```

#### `agentvcs remote add`
Add a remote repository for push/pull operations.

**Options:**
- `--name`: Remote name (default: origin)
- `--url`: Remote URL (required)
- `--type`: Remote type (agentvcs, git, custom)
- `--set-default`: Set as default remote

**Example:**
```bash
agentvcs remote add origin https://github.com/user/repo --type git --set-default
```

#### `agentvcs remote remove`
Remove a remote repository.

**Options:**
- `--name`: Remote name (removes all if not specified)

**Example:**
```bash
agentvcs remote remove origin
```

#### `agentvcs remote list`
List all configured remote repositories.

**Example:**
```bash
agentvcs remote list
```

#### `agentvcs push`
Push commits and semantic metadata to remote repository.

**Options:**
- `--remote`: Remote name (uses default if not specified)
- `--force`: Force push even if remote has newer commits
- `--dry-run`: Show what would be pushed without actually pushing

**Example:**
```bash
agentvcs push --dry-run
agentvcs push --force
```

#### `agentvcs pull`
Pull commits and semantic metadata from remote repository.

**Options:**
- `--remote`: Remote name (uses default if not specified)
- `--force`: Force pull even if local has unpushed changes
- `--dry-run`: Show what would be pulled without actually pulling

**Example:**
```bash
agentvcs pull
agentvcs pull --remote upstream
```

#### `agentvcs fetch`
Fetch updates from remote without merging.

**Options:**
- `--remote`: Remote name (uses default if not specified)

**Example:**
```bash
agentvcs fetch
```

### Commit Operations

#### `agentvcs commit`
Create a semantic commit with intent, risk level, and reasoning trace.

**Options:**
- `--intent`: Intent behind the change (required)
- `--risk`: Risk level (low, medium, high, critical)
- `--subsystem`: Affected subsystem
- `--type`: Change type (bugfix, feature, refactor, perf, security, docs, test, chore)
- `--reasoning`: Reasoning trace for the change (required)
- `--bug-id`: Bug ID if this is a fix
- `--author`: Author of the commit
- `--files`: Files affected by this commit
- `--tags`: Tags for the commit
- `--dependencies`: Dependencies for this commit (format: target:type)
- `--metadata`: Additional metadata (format: key=value)

**Example:**
```bash
agentvcs commit --intent "fix authentication bug" \
                --risk medium \
                --subsystem auth \
                --type bugfix \
                --reasoning "JWT validation was failing due to clock skew" \
                --bug-id CVE-2024-1234 \
                --tags security,critical \
                --files src/auth.py
```

#### `agentvcs propose`
Agents propose autonomous changes for human or agent review.

**Options:**
- `--type`: Change type (bugfix, feature, refactor, perf, security)
- `--target`: Target file or subsystem (required)
- `--agent`: Agent proposing the change
- `--reasoning`: Agent's reasoning (required)
- `--risk`: Risk level
- `--impact`: Estimated impact

**Example:**
```bash
agentvcs propose --type refactor --target src/auth.py \
                --agent refactor-bot \
                --reasoning "Extract token validation into separate method" \
                --risk low
```

#### `agentvcs merge`
Predictive merge engine with conflict simulation and resolution.

**Options:**
- `--branch`: Branch to merge (required)
- `--simulate`: Simulate merge without applying
- `--strategy`: Merge strategy (auto, manual, agent)

**Example:**
```bash
agentvcs merge --branch feature/new-auth --simulate --strategy auto
```

#### `agentvcs history`
Query intent-aware history with advanced filtering.

**Options:**
- `--query`: Natural language query about history
- `--commit`: Specific commit to query
- `--agent`: Filter by agent
- `--limit`: Number of results
- `--risk`: Filter by risk level
- `--type`: Filter by change type
- `--subsystem`: Filter by subsystem
- `--since`: Show commits since (YYYY-MM-DD)
- `--format`: Output format (table, json, detailed)

**Example:**
```bash
agentvcs history --query "authentication" --format detailed
agentvcs history --agent security-bot --risk high --limit 20
agentvcs history --since 2024-01-01 --type security
```

### Agent Operations

#### `agentvcs review`
Launch a multi-agent review swarm to evaluate a commit.

**Options:**
- `--commit`: Commit hash to review (required)
- `--agents`: Comma-separated list of agent roles (security, performance, architecture)

**Example:**
```bash
agentvcs review --commit abc123 --agents security,performance,architecture
```

#### `agentvcs refactor`
Autonomous refactor pipeline with structural improvement proposals.

**Options:**
- `--target`: Target file or directory (required)
- `--pattern`: Refactor pattern (e.g., extract-method, simplify-logic)
- `--agent`: Agent performing the refactor

**Example:**
```bash
agentvcs refactor --target src/auth.py --pattern extract-method --agent refactor-bot
```

#### `agentvcs sentinel`
Continuous risk monitoring for vulnerabilities, dependency drift, and regressions.

**Options:**
- `--watch`: Watch continuously
- `--interval`: Check interval in seconds

**Example:**
```bash
agentvcs sentinel --watch --interval 60
```

#### `agentvcs swarm`
Coordinate multi-agent collaboration with negotiation and consensus.

**Options:**
- `--task`: Task description for swarm (required)
- `--agents`: Comma-separated list of agents (required)
- `--timeout`: Timeout in seconds

**Example:**
```bash
agentvcs swarm --task "optimize database queries" \
               --agents performance,architecture \
               --timeout 300
```

### Management Operations

#### `agentvcs policy`
Define machine-first permissions and agent policies.

**Options:**
- `--add-rule`: Add a policy rule (format: 'agent_pattern:action:condition')
- `--list-rules`: List all policy rules
- `--remove-rule`: Remove a policy rule by ID

**Example:**
```bash
agentvcs policy --list-rules
agentvcs policy --add-rule "security-bot:*:always"
agentvcs policy --remove-rule rule-1
```

#### `agentvcs events`
Subscribe to event streams and view recent events.

**Options:**
- `--subscribe`: Comma-separated event types to subscribe
- `--tail`: Number of recent events to show

**Example:**
```bash
agentvcs events --tail 10
agentvcs events --subscribe commit,merge,review
```

#### `agentvcs graph`
Query the semantic repository graph.

**Options:**
- `--query`: Graph query (e.g., 'dependencies of src/auth.py')
- `--node-type`: Filter by node type (file, function, class, commit, agent)
- `--export`: Export graph to file (format: json, dot)

**Example:**
```bash
agentvcs graph --query "dependencies of src/auth.py"
agentvcs graph --export json
```

#### `agentvcs analyze`
Repository analytics and insights.

**Options:**
- `--type`: Analysis type (overview, risk, agents, commits, trends)
- `--format`: Output format (table, json, text)
- `--days`: Time period in days for trend analysis

**Example:**
```bash
agentvcs analyze --type overview
agentvcs analyze --type risk --format json
agentvcs analyze --type trends --days 90
```

#### `agentvcs backup`
Backup repository with semantic metadata.

**Options:**
- `--output`: Output file path for backup
- `--include-git`: Include Git data if available

**Example:**
```bash
agentvcs backup --output my-backup.tar.gz --include-git
```

#### `agentvcs restore`
Restore repository from backup.

**Options:**
- `--input`: Backup file to restore (required)
- `--force`: Force restore without confirmation

**Example:**
```bash
agentvcs restore --input my-backup.tar.gz --force
```

#### `agentvcs export`
Export repository data to various formats.

**Options:**
- `--format`: Export format (json, yaml, csv)
- `--output`: Output file path
- `--data`: Data to export (commits, events, proposals, graph, all)

**Example:**
```bash
agentvcs export --format json --data commits
agentvcs export --format yaml --output export.yaml
```

#### `agentvcs import`
Import repository data from exported file.

**Options:**
- `--input`: Import file (required)
- `--format`: Import format (auto-detected if not specified)

**Example:**
```bash
agentvcs import --input export.json
```

#### `agentvcs --version` / `agentvcs -v`
Output the current AgentVCS version.

## Git Integration

AgentVCS provides seamless Git integration for hybrid workflows:

### Adding Git Remotes

```bash
# Add a Git remote
agentvcs remote add origin https://github.com/user/repo --type git --set-default
```

### Git-Compatible Operations

When using Git-type remotes, AgentVCS automatically:

- **Push**: Runs `git push` to the Git remote alongside AgentVCS metadata push
- **Pull**: Runs `git pull` from the Git remote alongside AgentVCS metadata pull
- **Fetch**: Runs `git fetch` to get updates without merging

### Hybrid Workflow Example

```bash
# Initialize with Git compatibility
agentvcs init --git-migrate

# Add Git remote
agentvcs remote add origin https://github.com/user/repo --type git --set-default

# Make semantic commits
agentvcs commit --intent "add feature" --reasoning "..." --risk low

# Push to both Git and AgentVCS
agentvcs push

# Pull from both Git and AgentVCS
agentvcs pull
```

### Git Compatibility Features

- **Migration**: `--git-migrate` flag preserves existing Git history
- **Coexistence**: Git and AgentVCS commands work side-by-side
- **Storage**: Semantic metadata stored in `.agentvcs/` (separate from `.git/`)
- **Status**: `--all` flag shows both AgentVCS and Git remotes

## Architecture

AgentVCS is built with a modular, pluggable architecture:

```
agentvcs/
├── cli.py              # Main CLI entry point with 24 commands
├── models.py           # Pydantic data models for semantic data
├── core/
│   └── storage.py      # JSON-based storage layer
├── agents/
│   ├── base.py         # Base agent + 4 built-in agents
│   └── registry.py     # Agent registration system
├── merge/
│   └── engine.py       # Predictive merge engine
├── graph/
│   └── builder.py      # Semantic graph builder
├── events/
│   └── stream.py        # Event streaming system
└── policy/
    └── engine.py       # Policy and permission engine
```

## Agent Plugin System

AgentVCS supports custom agents through a simple plugin interface:

```python
from agentvcs.agents.base import BaseAgent
from agentvcs.models import AgentRole

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.DEVELOPER, "custom-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        # Custom review logic
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": True,
            "findings": ["Custom finding"],
            "concerns": [],
            "suggestions": [],
            "score": 0.9
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        # Custom proposal logic
        pass
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        # Custom risk analysis
        pass
```

## Remote Repository Support

AgentVCS supports multiple remote repository types:

### AgentVCS Remotes
Native AgentVCS remotes for semantic metadata synchronization:
```bash
agentvcs remote add origin https://agentvcs.example.com/repo --type agentvcs
```

### Git Remotes
Git-compatible remotes for hybrid workflows:
```bash
agentvcs remote add origin https://github.com/user/repo --type git
```

### Custom Remotes
Custom remote implementations for specialized needs:
```bash
agentvcs remote add custom https://custom.example.com/repo --type custom
```

## Data Models

### Commit
Semantic commit with full agent context:
- `id`: Unique commit identifier
- `intent`: Intent behind the change
- `risk_level`: Risk assessment (low, medium, high, critical)
- `subsystem`: Affected subsystem
- `change_type`: Type of change (bugfix, feature, etc.)
- `reasoning`: Detailed reasoning trace
- `dependencies`: Dependency graph
- `metadata`: Additional metadata and tags

### Remote
Remote repository configuration:
- `name`: Remote name (e.g., origin)
- `url`: Remote URL
- `type`: Remote type (agentvcs, git, custom)
- `last_push`: Last push timestamp
- `last_pull`: Last pull timestamp

## Documentation

- [Developer Guide](docs/developer-guide.md) - Architecture and development
- [Agent API Reference](docs/agent-api.md) - Creating custom agents
- [Policy Configuration](docs/policy-config.md) - Machine-first permissions
- [Event Streaming](docs/event-streaming.md) - Real-time event monitoring

## License
MIT License - see [LICENSE](LICENSE) file for details.
