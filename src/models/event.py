from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    name: str
    description: str
    date: datetime
    location: str
    capacity: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            'location': self.location,
            'capacity': self.capacity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }