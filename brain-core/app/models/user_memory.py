from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserMemory(BaseModel):
    userId: str
    name: str
    preferences: dict
    lastInteraction: datetime
    tags: List[str]
    notes: Optional[str]
