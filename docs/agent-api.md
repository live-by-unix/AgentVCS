# Agent API Reference

This document describes the AgentVCS agent API for creating custom agents.

## Base Agent Interface

All agents must extend the `BaseAgent` class:

```python
from agentvcs.agents.base import BaseAgent
from agentvcs.models import AgentRole

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.DEVELOPER, "my-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        pass
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        pass
```

## Required Methods

### review_commit

Review a commit and return assessment.

**Parameters:**
- `commit` (Dict[str, Any]): Commit data including intent, risk, files, etc.

**Returns:**
```python
{
    "agent": str,           # Agent name
    "role": str,            # Agent role
    "approved": bool,       # Whether commit is approved
    "findings": List[str],  # Positive findings
    "concerns": List[str],  # Concerns or issues
    "suggestions": List[str],  # Suggestions for improvement
    "score": float          # Approval score (0.0-1.0)
}
```

### propose_change

Propose a change based on context.

**Parameters:**
- `context` (Dict[str, Any]): Context including target, subsystem, etc.

**Returns:**
- `Proposal`: Proposal object with diff, reasoning, and impact assessment

### analyze_risk

Analyze risk level of a change.

**Parameters:**
- `change` (Dict[str, Any]): Change data

**Returns:**
```python
{
    "risk_level": str,      # low, medium, high, critical
    "reasoning": str,       # Risk assessment reasoning
    "mitigations": List[str]  # Suggested mitigations
}
```

## Agent Roles

Available agent roles:

- `DEVELOPER`: General development agent
- `REVIEWER`: Code review agent
- `SECURITY`: Security-focused agent
- `PERFORMANCE`: Performance optimization agent
- `ARCHITECTURE`: Architecture review agent
- `REFACTOR`: Code refactoring agent
- `SENTINEL`: Monitoring agent
- `COORDINATOR`: Multi-agent coordination

## Example: Custom Security Agent

```python
from agentvcs.agents.base import BaseAgent
from agentvcs.models import AgentRole, Proposal, ChangeType, RiskLevel
import hashlib

class CustomSecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentRole.SECURITY, "custom-security")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        findings = []
        concerns = []
        
        # Check for security-sensitive files
        for file in commit.get("files", []):
            if "auth" in file.lower() or "password" in file.lower():
                findings.append(f"Security-sensitive file modified: {file}")
        
        # Check risk level
        if commit.get("risk_level") == "critical":
            concerns.append("Critical risk requires additional review")
        
        # Calculate score
        score = 0.9 if not concerns else 0.5
        
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": len(concerns) == 0,
            "findings": findings,
            "concerns": concerns,
            "suggestions": ["Add security tests", "Review access controls"],
            "score": score
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        proposal_id = hashlib.sha256(
            f"security-{context['target']}".encode()
        ).hexdigest()[:12]
        
        return Proposal(
            id=proposal_id,
            agent=self.name,
            change_type=ChangeType.SECURITY,
            target=context.get("target", "unknown"),
            diff="# Security improvements\n# Add input validation",
            reasoning="Security analysis identified vulnerabilities",
            risk_level=RiskLevel.HIGH,
            estimated_impact="Improved security posture"
        )
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        subsystem = change.get("subsystem", "").lower()
        
        if "auth" in subsystem or "security" in subsystem:
            return {
                "risk_level": "high",
                "reasoning": "Security-sensitive subsystem",
                "mitigations": ["Security review", "Penetration testing"]
            }
        
        return {
            "risk_level": "medium",
            "reasoning": "Standard change",
            "mitigations": ["Code review"]
        }
```

## Registering Custom Agents

```python
from agentvcs.agents.registry import AgentRegistry

# Create registry instance
registry = AgentRegistry()

# Register custom agent
custom_agent = CustomSecurityAgent()
registry.register_agent(AgentRole.SECURITY, custom_agent)

# Use the agent
agent = registry.get_agent(AgentRole.SECURITY)
result = agent.review_commit(commit_data)
```

## Agent Lifecycle

1. **Initialization**: Agent is created and registered
2. **Review**: Agent reviews commits when requested
3. **Proposal**: Agent proposes changes based on analysis
4. **Risk Analysis**: Agent assesses risk for changes
5. **Coordination**: Agents participate in swarm collaboration

## Best Practices

1. **Specific Focus**: Each agent should have a specific focus area
2. **Clear Reasoning**: Always provide clear reasoning for decisions
3. **Score Consistency**: Use consistent scoring (0.0-1.0)
4. **Actionable Suggestions**: Provide actionable suggestions
5. **Risk Awareness**: Always consider risk in recommendations

## Integration with CLI

Custom agents are automatically available through the CLI:

```bash
# Use custom agent in review
agentvcs review --commit abc123 --agents custom-security,performance

# Use custom agent in swarm
agentvcs swarm --task "security audit" --agents custom-security
```
