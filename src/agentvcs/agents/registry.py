"""Agent registry for managing available agents."""

from typing import Dict, Optional
from agentvcs.models import AgentRole
from agentvcs.agents.base import (
    BaseAgent, SecurityAgent, PerformanceAgent, 
    ArchitectureAgent, RefactorAgent
)


class AgentRegistry:
    """Registry for managing available agents."""
    
    def __init__(self):
        self._agents: Dict[AgentRole, BaseAgent] = {
            AgentRole.SECURITY: SecurityAgent(),
            AgentRole.PERFORMANCE: PerformanceAgent(),
            AgentRole.ARCHITECTURE: ArchitectureAgent(),
            AgentRole.REFACTOR: RefactorAgent(),
        }
    
    def register_agent(self, role: AgentRole, agent: BaseAgent) -> None:
        """Register a new agent."""
        self._agents[role] = agent
    
    def get_agent(self, role: AgentRole) -> Optional[BaseAgent]:
        """Get an agent by role."""
        return self._agents.get(role)
    
    def list_agents(self) -> Dict[AgentRole, str]:
        """List all registered agents."""
        return {role: agent.name for role, agent in self._agents.items()}
    
    def get_all_agents(self) -> Dict[AgentRole, BaseAgent]:
        """Get all registered agents."""
        return self._agents.copy()
