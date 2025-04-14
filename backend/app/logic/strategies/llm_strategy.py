import json
from app.schemas.triage import LLMRequest
from app.logic.strategies.base import TriageScoringStrategy
from app.config.settings import settings
import httpx


print("🧪 OPENAI_API_KEY:", settings.OPENAI_API_KEY)

class LLMScoringStrategy(TriageScoringStrategy):
    async def score(self, data: LLMRequest) -> dict:
        prompt = self.build_prompt(data)

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "triage-llm-dev",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",  
            "messages": [
                {"role": "system", "content": "You are a medical triage assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        # 🔍 DEBUG 로그 출력
        print("📦 [디버그] API KEY:", settings.OPENAI_API_KEY)
        print("📦 [디버그] Headers:", headers)
        print("📦 [디버그] Payload:", json.dumps(payload, indent=2))

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

        print("📨 [디버그] 응답 상태코드:", response.status_code)
        print("📨 [디버그] 응답 본문:", response.text)

        if response.status_code != 200:
            raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")

        content = response.json()["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {
                "esi_score": 3,
                "explanation": content.strip()
            }

        return parsed

    def build_prompt(self, data: LLMRequest) -> str:
        return f"""You are a triage assistant. Based on the following data, assign an ESI level (1–5) and explain.

Patient:
- Age: {data.age}
- Gender: {data.gender}
- Symptoms: {data.symptoms}
- Vitals:
    - Heart Rate: {data.vitals.get("heartRate", "N/A")}
    - Blood Pressure: {data.vitals.get("bloodPressureSystolic", "N/A")}/{data.vitals.get("bloodPressureDiastolic", "N/A")}
    - Temperature: {data.vitals.get("temperature", "N/A")}
    - Respiratory Rate: {data.vitals.get("respiratoryRate", "N/A")}
    - Oxygen Saturation: {data.vitals.get("oxygenSaturation", "N/A")}
- Chronic Conditions: {", ".join(data.conditions) or "None"}

Respond in JSON:
{{
  "esi_score": <1-5>,
  "explanation": "<reasoning>"
}}"""
