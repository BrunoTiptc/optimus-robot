from pydantic import BaseModel
from datetime import datetime
from typing import List

class ConversationMemory(BaseModel):
    userId: str
    timestamp: datetime
    input: str
    response: str
    summary: str
    contextUsed: List[str]
