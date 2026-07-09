"""Base agent class for AgentVCS."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from agentvcs.models import AgentRole, Commit, Proposal


class BaseAgent(ABC):
    """Base class for all AgentVCS agents."""
    
    def __init__(self, role: AgentRole, name: str):
        self.role = role
        self.name = name
    
    @abstractmethod
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Review a commit and return assessment."""
        pass
    
    @abstractmethod
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        """Propose a change based on context."""
        pass
    
    @abstractmethod
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk level of a change."""
        pass


class SecurityAgent(BaseAgent):
    """Security-focused agent for vulnerability detection."""
    
    def __init__(self):
        super().__init__(AgentRole.SECURITY, "security-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Review commit for security issues."""
        findings = []
        concerns = []
        
        # Simulate security analysis
        if "auth" in commit.get("subsystem", "").lower():
            findings.append("Authentication changes detected - review token handling")
        
        if commit.get("risk_level") == "critical":
            concerns.append("Critical risk changes require additional security review")
        
        score = 0.9 if not concerns else 0.6
        approved = len(concerns) == 0
        
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": approved,
            "findings": findings,
            "concerns": concerns,
            "suggestions": ["Consider adding security tests"],
            "score": score
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        """Propose security-related changes."""
        from agentvcs.models import Proposal, ChangeType, RiskLevel
        import hashlib
        
        proposal_id = hashlib.sha256(f"security-{context['target']}".encode()).hexdigest()[:12]
        
        return Proposal(
            id=proposal_id,
            agent=self.name,
            change_type=ChangeType.SECURITY,
            target=context.get("target", "unknown"),
            diff="# Security improvements\n# Add input validation\n# Update dependencies",
            reasoning="Security analysis identified potential vulnerabilities",
            risk_level=RiskLevel.HIGH,
            estimated_impact="Improved security posture"
        )
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security risk."""
        return {
            "risk_level": "high" if "auth" in change.get("subsystem", "") else "medium",
            "reasoning": "Security-sensitive component",
            "mitigations": ["Add security tests", "Review access controls"]
        }


class PerformanceAgent(BaseAgent):
    """Performance-focused agent for optimization."""
    
    def __init__(self):
        super().__init__(AgentRole.PERFORMANCE, "performance-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Review commit for performance impact."""
        findings = []
        concerns = []
        
        if commit.get("change_type") == "perf":
            findings.append("Performance change detected - benchmark recommended")
        
        if "database" in commit.get("subsystem", "").lower():
            findings.append("Database changes - review query performance")
        
        score = 0.85 if not concerns else 0.7
        approved = len(concerns) == 0
        
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": approved,
            "findings": findings,
            "concerns": concerns,
            "suggestions": ["Add performance benchmarks"],
            "score": score
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        """Propose performance-related changes."""
        from agentvcs.models import Proposal, ChangeType, RiskLevel
        import hashlib
        
        proposal_id = hashlib.sha256(f"perf-{context['target']}".encode()).hexdigest()[:12]
        
        return Proposal(
            id=proposal_id,
            agent=self.name,
            change_type=ChangeType.PERF,
            target=context.get("target", "unknown"),
            diff="# Performance optimizations\n# Add caching\n# Optimize queries",
            reasoning="Performance analysis identified optimization opportunities",
            risk_level=RiskLevel.MEDIUM,
            estimated_impact="Improved response times"
        )
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance risk."""
        return {
            "risk_level": "medium",
            "reasoning": "Performance changes may affect system behavior",
            "mitigations": ["Add benchmarks", "Monitor metrics"]
        }


class ArchitectureAgent(BaseAgent):
    """Architecture-focused agent for design review."""
    
    def __init__(self):
        super().__init__(AgentRole.ARCHITECTURE, "architecture-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Review commit for architectural impact."""
        findings = []
        concerns = []
        
        if commit.get("change_type") == "refactor":
            findings.append("Refactor detected - review architectural impact")
        
        if len(commit.get("files", [])) > 5:
            concerns.append("Large change spans many files - consider splitting")
        
        score = 0.8 if not concerns else 0.65
        approved = len(concerns) == 0
        
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": approved,
            "findings": findings,
            "concerns": concerns,
            "suggestions": ["Update architecture documentation"],
            "score": score
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        """Propose architecture-related changes."""
        from agentvcs.models import Proposal, ChangeType, RiskLevel
        import hashlib
        
        proposal_id = hashlib.sha256(f"arch-{context['target']}".encode()).hexdigest()[:12]
        
        return Proposal(
            id=proposal_id,
            agent=self.name,
            change_type=ChangeType.REFACTOR,
            target=context.get("target", "unknown"),
            diff="# Architectural improvements\n# Decouple components\n# Improve modularity",
            reasoning="Architecture analysis identified design improvements",
            risk_level=RiskLevel.MEDIUM,
            estimated_impact="Improved maintainability"
        )
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze architectural risk."""
        return {
            "risk_level": "medium",
            "reasoning": "Architectural changes affect system design",
            "mitigations": ["Update docs", "Review dependencies"]
        }


class RefactorAgent(BaseAgent):
    """Refactor-focused agent for code improvements."""
    
    def __init__(self):
        super().__init__(AgentRole.REFACTOR, "refactor-agent")
    
    def review_commit(self, commit: Dict[str, Any]) -> Dict[str, Any]:
        """Review commit for refactoring quality."""
        findings = []
        concerns = []
        
        if commit.get("change_type") == "refactor":
            findings.append("Refactor change - verify behavior preservation")
        
        score = 0.9 if not concerns else 0.75
        approved = len(concerns) == 0
        
        return {
            "agent": self.name,
            "role": self.role.value,
            "approved": approved,
            "findings": findings,
            "concerns": concerns,
            "suggestions": ["Add regression tests"],
            "score": score
        }
    
    def propose_change(self, context: Dict[str, Any]) -> Proposal:
        """Propose refactor-related changes."""
        from agentvcs.models import Proposal, ChangeType, RiskLevel
        import hashlib
        
        proposal_id = hashlib.sha256(f"refactor-{context['target']}".encode()).hexdigest()[:12]
        
        return Proposal(
            id=proposal_id,
            agent=self.name,
            change_type=ChangeType.REFACTOR,
            target=context.get("target", "unknown"),
            diff="# Refactoring\n# Extract methods\n# Reduce complexity",
            reasoning="Code analysis identified refactoring opportunities",
            risk_level=RiskLevel.LOW,
            estimated_impact="Improved code quality"
        )
    
    def analyze_risk(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze refactor risk."""
        return {
            "risk_level": "low",
            "reasoning": "Refactoring maintains behavior",
            "mitigations": ["Add tests", "Review carefully"]
        }
