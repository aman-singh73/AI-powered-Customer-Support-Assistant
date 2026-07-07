from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    answer: str
    escalated: bool
    confidence: float
    sources: List[str]