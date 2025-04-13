from abc import ABC, abstractmethod
from app.schemas.triage import LLMRequest

class TriageScoringStrategy(ABC):
    @abstractmethod
    async def score(self, data: LLMRequest) -> dict:
        pass