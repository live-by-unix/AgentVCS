"""Storage layer for AgentVCS semantic data."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from agentvcs.models import Commit, Proposal, RepositoryConfig, PolicyRule, Event


class Storage:
    """Storage backend for AgentVCS semantic data."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.agentvcs_dir = repo_path / ".agentvcs"
        self.commits_file = self.agentvcs_dir / "commits.json"
        self.proposals_file = self.agentvcs_dir / "proposals.json"
        self.config_file = self.agentvcs_dir / "config.json"
        self.events_file = self.agentvcs_dir / "events.json"
        self.graph_file = self.agentvcs_dir / "graph.json"
        
    def initialize(self) -> None:
        """Initialize storage structure."""
        self.agentvcs_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            config = RepositoryConfig(name=self.repo_path.name)
            self.save_config(config)
        
        for file in [self.commits_file, self.proposals_file, self.events_file, self.graph_file]:
            if not file.exists():
                file.write_text("[]")
    
    def is_initialized(self) -> bool:
        """Check if repository is initialized."""
        return self.agentvcs_dir.exists() and self.config_file.exists()
    
    def save_config(self, config: RepositoryConfig) -> None:
        """Save repository configuration."""
        self.config_file.write_text(config.model_dump_json(indent=2))
    
    def load_config(self) -> RepositoryConfig:
        """Load repository configuration."""
        data = json.loads(self.config_file.read_text())
        return RepositoryConfig(**data)
    
    def save_commit(self, commit: Commit) -> None:
        """Save a commit to storage."""
        commits = self.load_commits()
        commits.append(commit.model_dump())
        self.commits_file.write_text(json.dumps(commits, indent=2, default=str))
    
    def load_commits(self) -> List[Dict[str, Any]]:
        """Load all commits."""
        if not self.commits_file.exists():
            return []
        return json.loads(self.commits_file.read_text())
    
    def get_commit(self, commit_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific commit by ID."""
        commits = self.load_commits()
        for commit in commits:
            if commit["id"] == commit_id:
                return commit
        return None
    
    def save_proposal(self, proposal: Proposal) -> None:
        """Save a proposal to storage."""
        proposals = self.load_proposals()
        proposals.append(proposal.model_dump())
        self.proposals_file.write_text(json.dumps(proposals, indent=2, default=str))
    
    def load_proposals(self) -> List[Dict[str, Any]]:
        """Load all proposals."""
        if not self.proposals_file.exists():
            return []
        return json.loads(self.proposals_file.read_text())
    
    def update_proposal_status(self, proposal_id: str, status: str) -> None:
        """Update proposal status."""
        proposals = self.load_proposals()
        for proposal in proposals:
            if proposal["id"] == proposal_id:
                proposal["status"] = status
                break
        self.proposals_file.write_text(json.dumps(proposals, indent=2, default=str))
    
    def save_event(self, event: Event) -> None:
        """Save an event to storage."""
        events = self.load_events()
        events.append(event.model_dump())
        self.events_file.write_text(json.dumps(events, indent=2, default=str))
    
    def load_events(self) -> List[Dict[str, Any]]:
        """Load all events."""
        if not self.events_file.exists():
            return []
        return json.loads(self.events_file.read_text())
    
    def save_graph(self, graph_data: Dict[str, Any]) -> None:
        """Save graph data."""
        self.graph_file.write_text(json.dumps(graph_data, indent=2))
    
    def load_graph(self) -> Dict[str, Any]:
        """Load graph data."""
        if not self.graph_file.exists():
            return {"nodes": [], "edges": []}
        return json.loads(self.graph_file.read_text())
    
    def add_policy_rule(self, rule: PolicyRule) -> None:
        """Add a policy rule."""
        config = self.load_config()
        config.policies.append(rule)
        self.save_config(config)
    
    def get_policy_rules(self) -> List[PolicyRule]:
        """Get all policy rules."""
        config = self.load_config()
        return config.policies
