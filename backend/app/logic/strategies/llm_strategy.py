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
            "model": "gpt-4o",  
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Your job is to assign an ESI level (1-5) and explain your decision in 50-100 words. Use the following logic:\n\n"
                        "1. **Level 1 (Immediate):** Life-threatening, needs immediate life-saving intervention (e.g., cardiac arrest, unresponsive, severe hypoglycemia).\n"
                        "2. **Level 2 (Emergent):** High risk of deterioration or signs of time-critical condition (e.g., chest pain with cardiac history, asthma attack, altered mental status).\n"
                        "3. **Level 3 (Urgent):** Stable, with multiple types of resources needed to investigate or treat (such as lab tests plus diagnostic imaging) (e.g., abdominal pain, high fever with cough, persistent headache).\n"
                        "4. **Level 4 (Less Urgent):** Stable, with only one type of resource anticipated (such as only an x-ray, or only sutures) (e.g., rabies vaccination, sore throat, simple laceration).\n"
                        "5. **Level 5 (Non-Urgent):** Stable, with no resources anticipated except oral or topical medications, or prescriptions (e.g., suture removal, prescription refill, foreign body in eye).\n\n"
                        "Take medical history into account **only if current symptoms or vitals are provided**. If no symptoms or vitals are given, assign a score of 4 or 5 based on the likelihood of needing minimal resources. Medical history should not significantly influence the score in such cases."
                        "Example of taking medical history into account properly: If the patient comes in with shortness of breath and has a condition of asthma and had a recent encounter in the ER due to an asthma attack, then we need to take the medical history into account and maybe raise the ESI from a 3 to a 2.\n"
                        "Example of not being overly sensitive to medical history: An older patient comes in and has normal vitals and no symptoms but has existing conditions and a good number of past encounters. The ESI should only be 5, or 4 if they have excessive concerning medical history.\n"
                        "- **Recent medical history** (conditions, medications, allergies, especially recurring or high-risk conditions).\n"
                        "- **Recent encounters only** (last 1-2 years; older ones are less relevant unless highly significant).\n"
                        "- **Vitals** (look for instability: low O₂ saturation, high heart rate, low BP, etc.).\n"
                        "- **Current symptoms** and clinical notes.\n\n"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
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
            if content.startswith("```json"):
                content = content[7:-3].strip()

            parsed = json.loads(content)
            esi_score = parsed.get("esi_score")
            explanation = parsed.get("explanation")
        except json.JSONDecodeError:
            esi_score = 3  # Default to a neutral score
            explanation = content.strip()

        # Return the parsed or fallback response
        return {
            "esi_score": esi_score,
            "explanation": explanation
        }

    def build_prompt(self, data: LLMRequest) -> str:
        return f"""Patient's information and past medical history (Refer back to system role content for triage instructions!):

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

Respond with a JSON with these fields:
  "esi_score": <1-5>,
  "explanation": "<reasoning>"
"""