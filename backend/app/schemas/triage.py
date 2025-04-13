from pydantic import BaseModel
from typing import List, Dict

class LLMRequest(BaseModel):
    age: int
    gender: str
    symptoms: str
    vitals: Dict[str, str]
    conditions: List[str]

class LLMResponse(BaseModel):
    esi_score: int
    explanation: str
