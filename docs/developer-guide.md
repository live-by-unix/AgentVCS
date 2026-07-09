# AgentVCS Developer Guide

## Architecture Overview

AgentVCS is built with a modular, agent-first architecture designed for autonomous AI workflows.

### Core Components

```
agentvcs/
├── cli.py              # Main CLI entry point with all commands
├── models.py           # Pydantic data models for semantic data
├── core/
│   └── storage.py      # Storage layer for semantic metadata
├── agents/
│   ├── base.py         # Base agent class and built-in agents
│   └── registry.py     # Agent registration and management
├── merge/
│   └── engine.py       # Predictive merge engine
├── graph/
│   └── builder.py      # Semantic repository graph builder
├── events/
│   └── stream.py       # Event streaming system
└── policy/
    └── engine.py       # Policy and permission engine
```

## Data Models

All semantic data is defined in `models.py` using Pydantic for validation:

- **Commit**: Semantic commit with intent, risk, reasoning, and agent context
- **Proposal**: Autonomous change proposals from agents
- **ReviewResult**: Results from agent reviews
- **MergeSimulation**: Predictive merge conflict analysis
- **PolicyRule**: Machine-first permission rules
- **Event**: System events for streaming
- **GraphNode/GraphEdge**: Semantic graph components
- **SwarmTask**: Multi-agent collaboration tasks
- **Remote**: Remote repository configuration with URL, type, and sync timestamps

## Storage Layer

The storage layer (`core/storage.py`) manages all semantic data in JSON format within the `.agentvcs/` directory:

- `commits.json`: All semantic commits
- `proposals.json`: Change proposals from agents
- `config.json`: Repository configuration and policies
- `events.json`: Event log
- `graph.json`: Semantic repository graph

## Remote Repository Support

AgentVCS supports remote repository synchronization similar to Git's origin system.

### Remote Configuration

Remotes are stored in the repository configuration (`config.json`) with the following structure:

```python
class Remote(BaseModel):
    name: str              # Remote name (e.g., 'origin')
    url: str               # Remote URL
    type: str              # Remote type: agentvcs, git, or custom
    last_push: Optional[datetime]  # Last push timestamp
    last_pull: Optional[datetime]  # Last pull timestamp
    metadata: Dict[str, Any]       # Additional remote metadata
```

### Remote Types

1. **AgentVCS Remotes**: Native AgentVCS servers for semantic metadata synchronization
2. **Git Remotes**: Git-compatible remotes for hybrid workflows
3. **Custom Remotes**: Custom implementations for specialized needs

### Git Integration

When using Git-type remotes, AgentVCS integrates with Git operations:

```python
# Push operation flow
if remote.type == "git":
    # 1. Run git push
    subprocess.run(["git", "push", remote.name, "main"])
    # 2. Push AgentVCS semantic metadata
    upload_semantic_data(remote.url)
```

### Remote Commands

The CLI provides the following remote management commands:

- `agentvcs remote add`: Add a new remote
- `agentvcs remote remove`: Remove a remote
- `agentvcs remote list`: List all remotes
- `agentvcs push`: Push to remote
- `agentvcs pull`: Pull from remote
- `agentvcs fetch`: Fetch without merging
- `agentvcs status`: Show remote status

### Implementing Custom Remote Types

To implement a custom remote type, extend the push/pull logic:

```python
# In cli.py or a separate remote module
def push_to_custom_remote(remote: Remote, storage: Storage):
    """Custom push implementation for custom remote type."""
    # Implement custom upload logic
    pass

def pull_from_custom_remote(remote: Remote, storage: Storage):
    """Custom pull implementation for custom remote type."""
    # Implement custom download logic
    pass
```

## Agent Framework

### Built-in Agents

AgentVCS includes several built-in agents:

1. **SecurityAgent**: Reviews for vulnerabilities and security issues
2. **PerformanceAgent**: Analyzes performance impact
3. **ArchitectureAgent**: Evaluates architectural changes
4. **RefactorAgent**: Suggests code improvements

### Creating Custom Agents

To create a custom agent, extend the `BaseAgent` class:

```python
from agentvcs.agents.base import BaseAgent
from agentvcs.models import AgentRole, Proposal

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.DEVELOPER, "custom-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        # Implement review logic
        findings = ["Custom finding"]
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": True,
            "findings": findings,
            "concerns": [],
            "suggestions": [],
            "score": 0.9
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        # Implement proposal logic
        pass
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        # Implement risk analysis
        pass
```

### Registering Custom Agents

```python
from agentvcs.agents.registry import AgentRegistry

registry = AgentRegistry()
registry.register_agent(AgentRole.DEVELOPER, CustomAgent())
```

## CLI Commands

### Adding New Commands

To add a new CLI command:

1. Add the command function in `cli.py`
2. Use Click decorators for arguments and options
3. Implement the command logic using storage and other components

```python
@main.command()
@click.option("--example", help="Example option")
def new_command(example: str):
    """Command description."""
    storage = get_storage()
    # Implementation
```

## Merge Engine

The merge engine (`merge/engine.py`) provides:

- **Conflict Prediction**: Simulates merges before applying them
- **Automatic Resolution**: Proposes resolutions for detected conflicts
- **Risk Assessment**: Evaluates merge risk based on conflicts and branch context

## Graph Builder

The graph builder (`graph/builder.py`) constructs a semantic repository graph with:

- **Nodes**: Commits, files, agents, subsystems
- **Edges**: Relationships (modifies, authored, belongs_to, etc.)
- **Queries**: Dependency analysis, impact assessment, history tracking

## Event Streaming

The event system (`events/stream.py`) provides:

- **Event Publishing**: Real-time event distribution
- **Subscription System**: Subscribe to specific event types
- **Async Streaming**: Async generator for event consumption

## Policy Engine

The policy engine (`policy/engine.py`) enforces machine-first permissions:

- **Rule Matching**: Pattern-based agent and action matching
- **Condition Evaluation**: Context-aware permission checks
- **Human Review Triggers**: Automatic review requirement based on risk

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Development Setup

1. Clone the repository
2. Install in development mode:

```bash
pip install -e ".[dev]"
```

3. Run the demo:

```bash
python example_demo.py
```

## Git Compatibility

AgentVCS maintains Git compatibility:

- Semantic data stored in `.agentvcs/` (not in `.git/`)
- Can be used alongside Git commands
- `agentvcs init --git-migrate` enables compatibility mode

## Contributing

Contributions are welcome! Please:

1. Follow the existing code style (use black and ruff)
2. Add tests for new features
3. Update documentation
4. Ensure all CLI commands have proper help text
