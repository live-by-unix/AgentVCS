"""Event streaming system for AgentVCS."""

import asyncio
from typing import List, Dict, Any, AsyncGenerator
from agentvcs.core.storage import Storage
from agentvcs.models import Event


class EventStream:
    """Event streaming system for real-time event distribution."""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self._subscribers: Dict[str, List] = {}
    
    def subscribe(self, event_type: str, callback) -> None:
        """Subscribe to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    
    def publish(self, event: Event) -> None:
        """Publish an event to subscribers."""
        event_type = event.event_type
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(event)
    
    async def stream(self, event_types: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream events of specified types."""
        while True:
            events = self.storage.load_events()
            recent_events = [
                e for e in events 
                if e["event_type"] in event_types
            ]
            
            for event in recent_events[-5:]:  # Yield last 5 matching events
                yield event
            
            await asyncio.sleep(1)
    
    def get_recent_events(self, event_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent events of a specific type."""
        events = self.storage.load_events()
        filtered = [e for e in events if e["event_type"] == event_type]
        return filtered[-limit:]
    
    def create_event(self, event_type: str, source: str, data: Dict[str, Any]) -> Event:
        """Create and save a new event."""
        import hashlib
        event_id = hashlib.sha256(f"{event_type}{source}{str(data)}".encode()).hexdigest()[:12]
        
        event = Event(
            id=event_id,
            event_type=event_type,
            source=source,
            data=data
        )
        
        self.storage.save_event(event)
        self.publish(event)
        
        return event
