from pydantic import BaseModel
from typing import List, Dict, Optional

class Medication(BaseModel):
    name: str
    dosage: Optional[List[Dict[str, str]]] = None  # Dosage details

class Allergy(BaseModel):
    name: str  # What the patient is allergic to
    criticality: str  # Severity of the allergy
    reaction: Optional[List[Dict[str, str]]] = None  # Reaction details

class ClinicalNote(BaseModel):
    type: str  # Type of the clinical note
    date: str  # Date of the note
    content: str  # Content of the note

class Encounter(BaseModel):
    type: List[str]  # Encounter type (e.g., "Check-up")
    class_: str  # Class of the encounter (e.g., "AMB")
    reason: str # Actual reason itself the patient came in
    period: Dict[str, str]  # Start and end times of the encounter

class LLMRequest(BaseModel):
    age: int
    gender: str
    symptoms: str
    vitals: Dict[str, str]
    conditions: List[str]
    medications: List[Medication]
    allergies: List[Allergy]
    clinical_notes: List[ClinicalNote]
    encounters: List[Encounter]

class LLMResponse(BaseModel):
    esi_score: int
    explanation: str