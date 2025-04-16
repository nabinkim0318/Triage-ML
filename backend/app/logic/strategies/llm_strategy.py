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
        return f"""You are a triage assistant. Based on the following FHIR and patient data, assign an Emergency Severity Index level (1-5) and give a short 50-100 word-long explanation. Level 1 is life-threatening, level 5 is non-urgent. Please take the patient's vitals, symptoms, and medical information as context to calculate the score. Also use recent and relevant encounters for context on if the patient is visiting the ER for a recurring issue.

Patient:
- Age: {"N/A" if data.age is -1 else data.age}
- Gender: {data.gender}
- Symptoms: {data.symptoms or "N/A"}
- Vitals:
    - Heart Rate: {data.vitals.get("heartRate", "N/A")} bpm
    - Blood Pressure: {data.vitals.get("bloodPressureSystolic", "N/A")}/{data.vitals.get("bloodPressureDiastolic", "N/A")} mmHg
    - Temperature: {data.vitals.get("temperature", "N/A")} {data.vitals.get("temperatureUnit", "N/A")}
    - Respiratory Rate: {data.vitals.get("respiratoryRate", "N/A")} breaths/min
    - Oxygen Saturation: {data.vitals.get("oxygenSaturation", "N/A")} %
- Chronic Conditions: {", ".join(data.conditions) or "None"}
- Medications: {", ".join([med.name for med in data.medications]) or "None"}
- Allergies: {", ".join([allergy.name for allergy in data.allergies]) or "None"}
- Clinical Notes: {", ".join([f"{note.type} ({note.date})" for note in data.clinical_notes]) or "None"}
- Encounters: {", ".join([f"{', '.join(enc.type)}. Encounter class: {enc.class_}. Reason for visit: {enc.reason} (Encounter start: {enc.period.get('start', 'Unknown')} - Encounter end: {enc.period.get('end', 'Unknown')})" for enc in data.encounters]) or "None"}

Respond in JSON:
{{
  "esi_score": <1-5>,
  "explanation": "<reasoning>"
}}"""
