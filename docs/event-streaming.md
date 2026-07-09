# Event Streaming Guide

AgentVCS provides a real-time event streaming system for monitoring repository activity, agent actions, and system events.

## Event Types

AgentVCS generates events for various activities:

- **commit**: New semantic commit created
- **merge**: Merge operation performed
- **review**: Agent review completed
- **proposal**: Change proposal created
- **sentinel-check**: Sentinel monitoring check
- **swarm**: Multi-agent swarm activity
- **policy**: Policy rule changes

## Event Structure

Each event contains:

```python
{
    "id": "evt-abc123",
    "event_type": "commit",
    "timestamp": "2024-01-01T12:00:00",
    "source": "agent-name",
    "data": {
        "commit_id": "abc123",
        "intent": "fix bug",
        "risk": "medium"
    },
    "severity": "info"
}
```

## Viewing Events

### View Recent Events

```bash
agentvcs events --tail 10
```

### Subscribe to Event Types

```bash
agentvcs events --subscribe commit,merge,review
```

This starts a real-time stream of matching events.

## Event Data by Type

### Commit Events

```json
{
  "event_type": "commit",
  "data": {
    "commit_id": "abc123",
    "intent": "Add authentication",
    "risk": "medium",
    "author": "security-bot"
  }
}
```

### Merge Events

```json
{
  "event_type": "merge",
  "data": {
    "branch": "feature/new-auth",
    "strategy": "auto",
    "conflicts_resolved": 2
  }
}
```

### Review Events

```json
{
  "event_type": "review",
  "data": {
    "commit_id": "abc123",
    "agent": "security-agent",
    "approved": true,
    "score": 0.9
  }
}
```

### Sentinel Events

```json
{
  "event_type": "sentinel-check",
  "data": {
    "check": "Vulnerability scan",
    "status": "passed"
  }
}
```

### Swarm Events

```json
{
  "event_type": "swarm",
  "data": {
    "task_id": "task-123",
    "consensus": "approve",
    "agents": ["security", "performance"]
  }
}
```

## Programmatic Event Access

### Using Python API

```python
from pathlib import Path
from agentvcs.core.storage import Storage
from agentvcs.events.stream import EventStream

# Initialize
repo_path = Path.cwd()
storage = Storage(repo_path)
event_stream = EventStream(storage)

# Get recent events
recent_events = event_stream.get_recent_events("commit", limit=10)

# Subscribe to events
def handle_event(event):
    print(f"Event: {event.event_type} from {event.source}")

event_stream.subscribe("commit", handle_event)

# Create custom event
event_stream.create_event(
    event_type="custom",
    source="my-script",
    data={"message": "Custom event"}
)
```

### Async Event Streaming

```python
import asyncio

async def monitor_events():
    event_types = ["commit", "merge", "review"]
    async for event in event_stream.stream(event_types):
        print(f"Received: {event['event_type']}")

asyncio.run(monitor_events())
```

## Event Filtering

### Filter by Type

```bash
# Only commit events
agentvcs events --subscribe commit

# Multiple types
agentvcs events --subscribe commit,merge,review
```

### Filter by Severity

Events have severity levels: info, warning, error, critical.

```python
# In Python
events = storage.load_events()
critical_events = [e for e in events if e.get("severity") == "critical"]
```

### Filter by Source

```python
events = storage.load_events()
agent_events = [e for e in events if e.get("source") == "security-bot"]
```

## Event-Based Workflows

### Trigger Actions on Events

```python
def on_commit(event):
    if event.data.get("risk") == "critical":
        # Trigger additional review
        print("Critical commit detected - triggering review")

event_stream.subscribe("commit", on_commit)
```

### Monitor for Failures

```python
def on_sentinel_check(event):
    if event.data.get("status") == "failed":
        # Send alert
        print(f"Sentinel check failed: {event.data['check']}")

event_stream.subscribe("sentinel-check", on_sentinel_check)
```

### Track Agent Activity

```python
def on_any_event(event):
    # Log all agent activity
    print(f"{event.source}: {event.event_type}")

for event_type in ["commit", "review", "proposal"]:
    event_stream.subscribe(event_type, on_any_event)
```

## Event Retention

Events are stored in `.agentvcs/events.json`. To manage retention:

```python
# Keep only last 1000 events
events = storage.load_events()
events = events[-1000:]
# Write back to storage
```

## Custom Event Types

Create custom events for your workflows:

```python
event_stream.create_event(
    event_type="deployment",
    source="deploy-bot",
    data={
        "environment": "production",
        "version": "1.2.3",
        "status": "success"
    }
)
```

## Event Integration

### Webhook Integration

```python
import requests

def webhook_handler(event):
    webhook_url = "https://your-webhook.example.com"
    requests.post(webhook_url, json=event.model_dump())

event_stream.subscribe("commit", webhook_handler)
```

### Database Logging

```python
import sqlite3

def db_logger(event):
    conn = sqlite3.connect("events.db")
    conn.execute(
        "INSERT INTO events (type, source, data) VALUES (?, ?, ?)",
        (event.event_type, event.source, str(event.data))
    )
    conn.commit()

event_stream.subscribe("*", db_logger)
```

## Monitoring Dashboards

Use event streams to power monitoring dashboards:

```python
from collections import Counter

def get_event_stats():
    events = storage.load_events()
    types = Counter(e["event_type"] for e in events)
    sources = Counter(e["source"] for e in events)
    return {"types": types, "sources": sources}
```

## Best Practices

1. **Subscribe to Specific Types**: Only subscribe to event types you need
2. **Handle Errors**: Always add error handling in event callbacks
3. **Rate Limiting**: For high-volume events, implement rate limiting
4. **Event Schema**: Document custom event schemas for your team
5. **Retention Policy**: Implement event retention to manage storage

## Troubleshooting

### No Events Appearing

Check:
- Repository is initialized (`agentvcs init`)
- Events are being generated (try creating a commit)
- Event types match subscription

### Event Stream Not Updating

Check:
- Subscription is active
- Event file is being written
- No file permission issues

### High Memory Usage

Implement event filtering and retention:

```python
# Process events in batches
events = storage.load_events()
for batch in [events[i:i+100] for i in range(0, len(events), 100)]:
    process_batch(batch)
```
