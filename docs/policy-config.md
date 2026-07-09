# Policy Configuration Guide

AgentVCS uses a machine-first permission system to control agent actions. This guide explains how to configure and manage policies.

## Policy Rules

Policy rules define which agents can perform which actions under what conditions.

### Rule Structure

```python
PolicyRule(
    id="rule-1",
    agent_pattern="security-bot",
    action="merge",
    condition="always",
    requires_human_review=False,
    restricted_subsystems=["core"],
    allowed_subsystems=["auth", "utils"]
)
```

### Fields

- **id**: Unique identifier for the rule
- **agent_pattern**: Pattern to match agent names (supports wildcards)
- **action**: Action to control (merge, commit, review, propose, or *)
- **condition**: Condition for the rule (always, or specific conditions)
- **requires_human_review**: Whether human review is required
- **restricted_subsystems**: Subsystems the agent cannot modify
- **allowed_subsystems**: Subsystems the agent can modify (empty = all)

## Default Policies

When you initialize a repository, AgentVCS creates default policies:

```yaml
- id: default-1
  agent_pattern: "*"
  action: commit
  condition: always
  requires_human_review: false

- id: default-2
  agent_pattern: "*"
  action: merge
  condition: risk_level == 'high' or risk_level == 'critical'
  requires_human_review: true
```

## Managing Policies via CLI

### List All Policies

```bash
agentvcs policy --list-rules
```

### Add a New Policy

```bash
agentvcs policy --add-rule "security-bot:merge:always"
```

Format: `agent_pattern:action:condition`

### Remove a Policy

```bash
agentvcs policy --remove-rule rule-1
```

## Common Policy Patterns

### Allow Specific Agent to Merge Without Review

```bash
agentvcs policy --add-rule "trusted-bot:merge:always"
```

### Require Review for High-Risk Changes

```bash
agentvcs policy --add-rule "*:merge:risk_level == 'high'"
```

### Restrict Access to Core Subsystem

```bash
agentvcs policy --add-rule "*:commit:subsystem == 'core'"
# Then manually set requires_human_review: true in config
```

### Allow Security Agent Full Access

```bash
agentvcs policy --add-rule "security-bot:*:always"
```

### Restrict New Agents

```bash
agentvcs policy --add-rule "new-*:*:always"
# Set requires_human_review: true
```

## Condition Syntax

Conditions support simple expressions:

- `always`: Always matches
- `risk_level == 'high'`: Matches high risk changes
- `risk_level == 'critical'`: Matches critical risk changes
- `subsystem == 'auth'`: Matches auth subsystem changes

## Risk-Based Policies

Configure policies based on risk levels:

```bash
# Low risk - no review
agentvcs policy --add-rule "*:commit:risk_level == 'low'"

# Medium risk - optional review
agentvcs policy --add-rule "*:commit:risk_level == 'medium'"

# High risk - require review
agentvcs policy --add-rule "*:commit:risk_level == 'high'"

# Critical risk - require review and restrict
agentvcs policy --add-rule "*:commit:risk_level == 'critical'"
```

## Subsystem-Based Policies

Control access to specific subsystems:

```bash
# Auth subsystem - require security review
agentvcs policy --add-rule "*:commit:subsystem == 'auth'"

# Core subsystem - restrict access
agentvcs policy --add-rule "*:commit:subsystem == 'core'"

# Test subsystem - allow any agent
agentvcs policy --add-rule "*:commit:subsystem == 'test'"
```

## Agent-Specific Policies

Create policies for specific agents:

```bash
# Security bot - full access
agentvcs policy --add-rule "security-bot:*:always"

# Performance bot - read-only access
agentvcs policy --add-rule "performance-bot:review:always"

# Refactor bot - limited access
agentvcs policy --add-rule "refactor-bot:propose:always"
```

## Policy Evaluation Order

Policies are evaluated in order:

1. First matching rule wins
2. More specific patterns should come first
3. Wildcard patterns (*) should come last

Example configuration order:

```yaml
- id: rule-1
  agent_pattern: "security-bot"
  action: "*"
  condition: "always"

- id: rule-2
  agent_pattern: "perf-bot"
  action: "merge"
  condition: "always"

- id: rule-3
  agent_pattern: "*"
  action: "merge"
  condition: "risk_level == 'high'"
```

## Editing Policies Directly

Policies are stored in `.agentvcs/config.json`. You can edit this file directly:

```json
{
  "name": "my-project",
  "policies": [
    {
      "id": "custom-1",
      "agent_pattern": "my-agent",
      "action": "merge",
      "condition": "always",
      "requires_human_review": false
    }
  ]
}
```

## Policy Examples

### Example 1: Strict Security

```bash
# All agents require human review for merges
agentvcs policy --add-rule "*:merge:always"

# Security bot can merge without review
agentvcs policy --add-rule "security-bot:merge:always"
```

### Example 2: Autonomous Development

```bash
# Developer agents can commit freely
agentvcs policy --add-rule "dev-*:commit:always"

# High-risk changes require review
agentvcs policy --add-rule "*:commit:risk_level == 'high'"
```

### Example 3: Subsystem Isolation

```bash
# Only auth agents can modify auth subsystem
agentvcs policy --add-rule "auth-*:commit:subsystem == 'auth'"

# Restrict core to specific agents
agentvcs policy --add-rule "core-maintainer:commit:subsystem == 'core'"
```

## Testing Policies

Test policies by attempting actions:

```bash
# Try a commit
agentvcs commit --intent "test" --reasoning "test" --risk low

# Check if review is required
agentvcs policy --list-rules
```

## Best Practices

1. **Start Conservative**: Begin with restrictive policies, then loosen as needed
2. **Document Policies**: Keep a policy document explaining rules
3. **Review Regularly**: Periodically review and update policies
4. **Use Specific Patterns**: Prefer specific agent patterns over wildcards
5. **Monitor Events**: Use `agentvcs events` to monitor policy violations
6. **Test Changes**: Test policy changes in a safe environment first

## Troubleshooting

### Agent Cannot Commit

Check if:
- Policy rule exists for the agent
- Condition matches the action
- Subsystem is not restricted

### Unexpected Review Required

Check if:
- Risk level triggers review requirement
- Subsystem is restricted
- Policy requires human review

### Policy Not Applied

Check:
- Policy order (more specific first)
- Pattern matching (use correct agent name)
- Condition syntax
