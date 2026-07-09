"""Graph builder for semantic repository analysis."""

from typing import Dict, Any, List
from agentvcs.core.storage import Storage
from agentvcs.models import GraphNode, GraphEdge


class GraphBuilder:
    """Builder for semantic repository graphs."""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def build_graph(self) -> Dict[str, Any]:
        """Build the semantic repository graph."""
        nodes = []
        edges = []
        
        # Add commits as nodes
        commits = self.storage.load_commits()
        for commit in commits:
            nodes.append(GraphNode(
                id=commit["id"],
                type="commit",
                properties={
                    "author": commit["author"],
                    "intent": commit["intent"],
                    "risk_level": commit["risk_level"],
                    "change_type": commit["change_type"],
                    "timestamp": commit.get("timestamp")
                }
            ).model_dump())
            
            # Add file nodes and edges
            for file_path in commit.get("files", []):
                file_node = GraphNode(
                    id=file_path,
                    type="file",
                    properties={"path": file_path}
                ).model_dump()
                
                if file_node not in nodes:
                    nodes.append(file_node)
                
                edges.append(GraphEdge(
                    source=commit["id"],
                    target=file_path,
                    relationship="modifies",
                    properties={"timestamp": commit.get("timestamp")}
                ).model_dump())
        
        # Add agents as nodes
        agents = set(commit["author"] for commit in commits)
        for agent in agents:
            nodes.append(GraphNode(
                id=agent,
                type="agent",
                properties={"name": agent}
            ).model_dump())
            
            # Connect agents to their commits
            for commit in commits:
                if commit["author"] == agent:
                    edges.append(GraphEdge(
                        source=agent,
                        target=commit["id"],
                        relationship="authored",
                        properties={}
                    ).model_dump())
        
        # Add subsystem nodes
        subsystems = set(commit.get("subsystem") for commit in commits if commit.get("subsystem"))
        for subsystem in subsystems:
            nodes.append(GraphNode(
                id=subsystem,
                type="subsystem",
                properties={"name": subsystem}
            ).model_dump())
            
            # Connect commits to subsystems
            for commit in commits:
                if commit.get("subsystem") == subsystem:
                    edges.append(GraphEdge(
                        source=commit["id"],
                        target=subsystem,
                        relationship="belongs_to",
                        properties={}
                    ).model_dump())
        
        return {"nodes": nodes, "edges": edges}
    
    def query_dependencies(self, target: str) -> List[Dict[str, Any]]:
        """Query dependencies of a target."""
        graph = self.build_graph()
        dependencies = [
            edge for edge in graph["edges"]
            if edge["source"] == target and edge["relationship"] == "depends_on"
        ]
        return dependencies
    
    def query_impact(self, target: str) -> List[Dict[str, Any]]:
        """Query impact of changes to a target."""
        graph = self.build_graph()
        impact = [
            edge for edge in graph["edges"]
            if edge["target"] == target
        ]
        return impact
    
    def get_commit_history(self, file_path: str) -> List[Dict[str, Any]]:
        """Get commit history for a file."""
        graph = self.build_graph()
        commit_edges = [
            edge for edge in graph["edges"]
            if edge["target"] == file_path and edge["relationship"] == "modifies"
        ]
        return commit_edges
