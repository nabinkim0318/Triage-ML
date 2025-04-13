from app.schemas.triage import LLMRequest
from app.logic.strategies.llm_strategy import LLMScoringStrategy
from app.logic.strategies.rule_strategy import RuleBasedESIStrategy

class TriageScorer:
    def __init__(self, strategy: str = "llm"):
        self.strategy_name = strategy.lower()
        self.strategy = {
            "llm": LLMScoringStrategy(),
            "rule": RuleBasedESIStrategy()
        }.get(self.strategy_name)

        if not self.strategy:
            raise ValueError(f"Unknown strategy: {strategy}")

    async def predict(self, request_data: LLMRequest) -> dict:
        return await self.strategy.score(request_data)
