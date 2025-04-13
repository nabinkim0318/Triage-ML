from app.logic.strategies.base import TriageScoringStrategy
from app.schemas.triage import LLMRequest

class RuleBasedESIStrategy(TriageScoringStrategy):
    async def score(self, data: LLMRequest) -> dict:
        vitals = data.vitals
        symptoms = data.symptoms.lower()
        conditions = data.conditions

        hr = int(vitals.get("heartRate", "0"))
        bp = int(vitals.get("bloodPressureSystolic", "120"))
        rr = int(vitals.get("respiratoryRate", "16"))

        explanation = []

        if hr > 130 or bp < 90 or rr > 30:
            explanation.append("Abnormal vitals (HR > 130, BP < 90, RR > 30)")
            score = 2
        elif "chest pain" in symptoms or "shortness of breath" in symptoms:
            explanation.append("Symptoms indicate moderate severity")
            score = 2
        elif "hypertension" in conditions:
            explanation.append("Stable chronic condition with no acute distress")
            score = 3
        else:
            explanation.append("Stable vitals and symptoms")
            score = 4

        return {
            "esi_score": score,
            "explanation": "; ".join(explanation)
        }
