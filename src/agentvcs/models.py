"""Core data models for AgentVCS."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk levels for commits and changes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ChangeType(str, Enum):
    """Types of changes."""
    BUGFIX = "bugfix"
    FEATURE = "feature"
    REFACTOR = "refactor"
    PERF = "perf"
    SECURITY = "security"
    DOCS = "docs"
    TEST = "test"
    CHORE = "chore"


class AgentRole(str, Enum):
    """Agent roles in the system."""
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    REFACTOR = "refactor"
    SENTINEL = "sentinel"
    COORDINATOR = "coordinator"


class Commit(BaseModel):
    """Semantic commit with full agent context."""
    id: str = Field(..., description="Commit hash/ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    author: str = Field(..., description="Agent or human author")
    intent: str = Field(..., description="Intent behind the change")
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM)
    subsystem: Optional[str] = Field(None, description="Affected subsystem")
    change_type: ChangeType = Field(default=ChangeType.FEATURE)
    reasoning: str = Field(..., description="Reasoning trace for the change")
    files: List[str] = Field(default_factory=list)
    dependencies: Dict[str, List[str]] = Field(default_factory=dict)
    bug_fixed: Optional[str] = Field(None, description="Bug ID if this is a fix")
    approved_by: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Proposal(BaseModel):
    """Autonomous change proposal."""
    id: str = Field(..., description="Proposal ID")
    agent: str = Field(..., description="Agent proposing the change")
    change_type: ChangeType
    target: str = Field(..., description="Target file or subsystem")
    diff: str = Field(..., description="Proposed diff")
    reasoning: str = Field(..., description="Agent's reasoning")
    risk_level: RiskLevel = Field(default=RiskLevel.MEDIUM)
    estimated_impact: str = Field(..., description="Estimated impact")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending", description="pending, approved, rejected")


class ReviewResult(BaseModel):
    """Result from an agent review."""
    agent: str
    agent_role: AgentRole
    commit_id: str
    approved: bool
    findings: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MergeConflict(BaseModel):
    """Predicted merge conflict."""
    file: str
    line_start: int
    line_end: int
    our_content: str
    their_content: str
    resolution: Optional[str] = None
    reasoning: Optional[str] = None


class MergeSimulation(BaseModel):
    """Result of merge simulation."""
    can_merge: bool
    conflicts: List[MergeConflict] = Field(default_factory=list)
    resolved_conflicts: List[MergeConflict] = Field(default_factory=list)
    risk_level: RiskLevel
    reasoning: str
    suggested_resolution: Optional[str] = None


class PolicyRule(BaseModel):
    """Policy rule for agent permissions."""
    id: str
    agent_pattern: str = Field(..., description="Pattern to match agents")
    action: str = Field(..., description="merge, commit, review, propose")
    condition: str = Field(..., description="Condition for the rule")
    requires_human_review: bool = Field(default=False)
    restricted_subsystems: List[str] = Field(default_factory=list)
    allowed_subsystems: List[str] = Field(default_factory=list)


class Remote(BaseModel):
    """Remote repository configuration."""
    name: str = Field(..., description="Remote name (e.g., 'origin')")
    url: str = Field(..., description="Remote URL")
    type: str = Field(default="agentvcs", description="Remote type: agentvcs, git, or custom")
    last_push: Optional[datetime] = Field(None, description="Last push timestamp")
    last_pull: Optional[datetime] = Field(None, description="Last pull timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RepositoryConfig(BaseModel):
    """Repository configuration."""
    name: str
    initialized_at: datetime = Field(default_factory=datetime.utcnow)
    default_risk_level: RiskLevel = RiskLevel.MEDIUM
    require_review_for_high_risk: bool = Field(True)
    policies: List[PolicyRule] = Field(default_factory=list)
    enabled_agents: List[str] = Field(default_factory=list)
    git_compatible: bool = Field(True)
    remotes: List[Remote] = Field(default_factory=list)
    default_remote: Optional[str] = Field(None, description="Default remote name")


class Event(BaseModel):
    """System event."""
    id: str
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str
    data: Dict[str, Any] = Field(default_factory=dict)
    severity: str = Field(default="info")


class GraphNode(BaseModel):
    """Node in the semantic repository graph."""
    id: str
    type: str = Field(..., description="file, function, class, commit, agent")
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Edge in the semantic repository graph."""
    source: str
    target: str
    relationship: str = Field(..., description="depends_on, modifies, reviewed_by, etc.")
    properties: Dict[str, Any] = Field(default_factory=dict)


class SwarmTask(BaseModel):
    """Multi-agent collaboration task."""
    id: str
    task: str
    agents: List[str]
    status: str = Field(default="pending")
    votes: Dict[str, str] = Field(default_factory=dict)
    consensus: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
