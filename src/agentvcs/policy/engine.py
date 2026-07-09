"""Policy engine for machine-first permissions."""

from typing import List, Optional, Dict, Any
from agentvcs.models import PolicyRule, RiskLevel
from agentvcs.core.storage import Storage


class PolicyEngine:
    """Engine for evaluating and enforcing agent policies."""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def check_permission(self, agent: str, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check if an agent has permission to perform an action."""
        rules = self.storage.get_policy_rules()
        
        for rule in rules:
            if self._matches_rule(agent, action, rule, context):
                return {
                    "allowed": True,
                    "requires_human_review": rule.requires_human_review,
                    "rule_id": rule.id,
                    "restricted_subsystems": rule.restricted_subsystems,
                    "allowed_subsystems": rule.allowed_subsystems
                }
        
        # Default deny
        return {
            "allowed": False,
            "requires_human_review": True,
            "rule_id": None,
            "reason": "No matching policy rule found"
        }
    
    def _matches_rule(self, agent: str, action: str, rule: PolicyRule, context: Dict[str, Any]) -> bool:
        """Check if an agent/action/context matches a rule."""
        # Check agent pattern
        if not self._matches_pattern(agent, rule.agent_pattern):
            return False
        
        # Check action
        if rule.action != "*" and rule.action != action:
            return False
        
        # Check condition
        if not self._evaluates_condition(rule.condition, context):
            return False
        
        return True
    
    def _matches_pattern(self, agent: str, pattern: str) -> bool:
        """Check if agent matches the pattern."""
        if pattern == "*":
            return True
        if pattern in agent:
            return True
        return False
    
    def _evaluates_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a condition string against context."""
        # Simple evaluation for demo
        if condition == "always":
            return True
        
        # Check for risk level conditions
        if "risk_level" in condition:
            risk_level = context.get("risk_level", "medium")
            if risk_level in condition:
                return True
        
        return False
    
    def can_merge(self, agent: str, branch: str, risk_level: RiskLevel) -> Dict[str, Any]:
        """Check if an agent can merge a branch."""
        context = {
            "branch": branch,
            "risk_level": risk_level.value
        }
        return self.check_permission(agent, "merge", context)
    
    def can_commit(self, agent: str, risk_level: RiskLevel, subsystem: Optional[str]) -> Dict[str, Any]:
        """Check if an agent can commit."""
        context = {
            "risk_level": risk_level.value,
            "subsystem": subsystem
        }
        return self.check_permission(agent, "commit", context)
    
    def requires_human_review(self, agent: str, action: str, context: Dict[str, Any]) -> bool:
        """Check if an action requires human review."""
        permission = self.check_permission(agent, action, context)
        return permission.get("requires_human_review", True)
    
    def is_subsystem_restricted(self, agent: str, subsystem: str) -> bool:
        """Check if a subsystem is restricted for an agent."""
        rules = self.storage.get_policy_rules()
        
        for rule in rules:
            if self._matches_pattern(agent, rule.agent_pattern):
                if subsystem in rule.restricted_subsystems:
                    return True
                if rule.allowed_subsystems and subsystem not in rule.allowed_subsystems:
                    return True
        
        return False
    
    def add_rule(self, rule: PolicyRule) -> None:
        """Add a new policy rule."""
        self.storage.add_policy_rule(rule)
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a policy rule."""
        rules = self.storage.get_policy_rules()
        filtered_rules = [r for r in rules if r.id != rule_id]
        
        if len(filtered_rules) == len(rules):
            return False  # Rule not found
        
        config = self.storage.load_config()
        config.policies = filtered_rules
        self.storage.save_config(config)
        return True
    
    def list_rules(self) -> List[PolicyRule]:
        """List all policy rules."""
        return self.storage.get_policy_rules()
