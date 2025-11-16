from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Participant:
    name: str
    email: str
    phone: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }