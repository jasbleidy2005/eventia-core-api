from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Attendance:
    event_id: int
    participant_id: int
    id: Optional[int] = None
    registered_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'participant_id': self.participant_id,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None
        }