from fastapi import APIRouter, Depends, HTTPException, Header, Query
from app.services.fhir_service import FHIRService
from app.config.settings import settings
from typing import Optional
import logging
from dotenv import load_dotenv
from app.api.routes.auth import token_store
from pydantic import BaseModel
from typing import Optional, Dict
from app.logic.scorer import TriageScorer
from app.schemas.triage import LLMRequest
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_fhir_service(authorization: Optional[str] = Header(None)):
    """Dependency to inject FHIR service with authentication"""
    # token = os.getenv("TEST_ACCESS_TOKEN")
    token = token_store.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No valid access token available. Please authenticate.")
    return FHIRService(settings.FHIR_SERVER_URL, token)

@router.get("/{patient_id}")
async def get_patient(
    patient_id: str, 
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient details by ID"""
    return await fhir_service.get_patient(patient_id)

class MedicalHistoryRequest(BaseModel):
    firstName: str
    lastName: str
    dob: str
    symptoms: Optional[str] = None
    vitals: Optional[Dict[str, str]] = None
    
def calculate_age(birth_date: str) -> int:
    """Calculate age based on the date of birth."""
    try:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        return -1  # Return -1 if the date format is invalid

@router.post("/medical-history")
async def get_medical_history(
    request: MedicalHistoryRequest,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Retrieve structured medical history for a given patient."""
    age = calculate_age(request.dob)
    
    patient_id = await fhir_service.find_patient_id(request.firstName, request.lastName, request.dob)
    if not patient_id:
        llm_request_data = {
            "age": age if age >= 0 else -1,
            "gender": "N/A",
            "symptoms": request.symptoms or "N/A",
            "vitals": {
                "heartRate": request.vitals.get("heartRate", "N/A") or "N/A",
                "bloodPressureSystolic": request.vitals.get("bloodPressureSystolic", "N/A") or "N/A",
                "bloodPressureDiastolic": request.vitals.get("bloodPressureDiastolic", "N/A") or "N/A",
                "temperature": request.vitals.get("temperature", "N/A") or "N/A",
                "temperatureUnit": request.vitals.get("temperatureUnit", "N/A") or "N/A",
                "respiratoryRate": request.vitals.get("respiratoryRate", "N/A") or "N/A",
                "oxygenSaturation": request.vitals.get("oxygenSaturation", "N/A") or "N/A",
            },
            "conditions": [],
            "medications": [],
            "allergies": [],
            "clinical_notes": [],
            "encounters": [],
        }

        scorer = TriageScorer(strategy="llm")
        llm_response = await scorer.predict(LLMRequest(**llm_request_data))

        return {
            "name": f"{request.firstName} {request.lastName}",
            "birthDate": request.dob,
            "age": age if age >= 0 else None,
            "gender": None,
            "conditions": [],
            "medications": [],
            "allergies": [],
            "clinical_notes": [],
            "encounters": [],
            "triage_score": llm_response["esi_score"],
            "triage_explanation": llm_response["explanation"],
        }

    try:
        # Retrieve FHIR data
        demographics = await fhir_service.get_patient_demographics(patient_id)
        conditions = await fhir_service.get_conditions(patient_id, clinical_status="active")
        medications = await fhir_service.get_medications(patient_id)
        allergies = await fhir_service.get_allergies(patient_id)
        clinical_notes = await fhir_service.get_clinical_notes(patient_id, fetch_content=True)
        encounters = await fhir_service.get_encounters(patient_id)
        
        vitals = {
            "heartRate": request.vitals.get("heartRate", "N/A") or "N/A",
            "bloodPressureSystolic": request.vitals.get("bloodPressureSystolic", "N/A") or "N/A",
            "bloodPressureDiastolic": request.vitals.get("bloodPressureDiastolic", "N/A") or "N/A",
            "temperature": request.vitals.get("temperature", "N/A") or "N/A",
            "temperatureUnit": request.vitals.get("temperatureUnit", "N/A") or "N/A",
            "respiratoryRate": request.vitals.get("respiratoryRate", "N/A") or "N/A",
            "oxygenSaturation": request.vitals.get("oxygenSaturation", "N/A") or "N/A",
        }
        
        # Prepare data for LLM
        llm_request_data = {
            "age": demographics.get("age"),
            "gender": demographics.get("gender"),
            "symptoms": request.symptoms,
            "vitals": vitals,
            "conditions": [condition["code"]["text"] for condition in conditions.get("conditions", [])],
            "medications": [
                {
                    "name": med["medication"].get("text", "Unknown"),
                    "dosage": [
                        {
                            "text": dosage.get("text", "N/A"),
                            "timing": dosage.get("timing", {}).get("text", "N/A"),
                            "route": dosage.get("route", {}).get("text", "N/A"),
                            "dose": dosage.get("doseAndRate", [{}])[0].get("doseQuantity", {}).get("value", "N/A")
                        }
                        for dosage in med.get("dosage", [])
                    ]
                }
                for med in medications.get("medications", [])
            ],
            "allergies": [
                {
                    "name": allergy["code"].get("text", "Unknown"),
                    "criticality": allergy.get("criticality", "unknown"),
                    "reaction": [
                        {
                            "manifestation": [reaction.get("manifestation", [{}])[0].get("text", "N/A")],
                            "severity": reaction.get("severity", "N/A")
                        }
                        for reaction in allergy.get("reaction", [])
                    ]
                }
                for allergy in allergies.get("allergies", [])
            ],
            "clinical_notes": [
                {
                    "type": note.get("type", "Unknown"),
                    "date": note.get("date", "Unknown"),
                    "content": note.get("content", "No content available")
                }
                for note in clinical_notes.get("notes", [])
            ],
            "encounters": [
                {
                    "type": [enc_type.get("text", "Unknown") for enc_type in encounter.get("type", [])],
                    "class_": encounter.get("class", "Unknown"),
                    "reason": encounter.get("reason", "Unknown"),
                    "period": {
                        "start": encounter.get("period", {}).get("start", "Unknown"),
                        "end": encounter.get("period", {}).get("end", "Unknown")
                    }
                }
                for encounter in encounters.get("encounters", [])
            ],
        }
        # Call the LLM scorer
        scorer = TriageScorer(strategy="llm")  # Use the LLM scoring strategy
        llm_response = await scorer.predict(LLMRequest(**llm_request_data))

        return {
            "name": demographics.get("name"),
            "birthDate": demographics.get("birthDate"),
            "age": age if age >= 0 else demographics.get("age"),
            "gender": demographics.get("gender"),
            "conditions": conditions,
            "medications": medications,
            "allergies": allergies,
            "clinical_notes": clinical_notes,
            "encounters": encounters,
            "triage_score": llm_response["esi_score"],
            "triage_explanation": llm_response["explanation"],
        }

    except Exception as e:
        import traceback
        logger.error("Error in get_medical_history:\n" + traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving medical history: {str(e)}")


@router.get("/{patient_id}/demographics")
async def get_patient_demographics(
    patient_id: str, 
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient demographics"""
    return await fhir_service.get_patient_demographics(patient_id)

@router.get("/{patient_id}/vitals")
async def get_patient_vitals(
    patient_id: str,
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient vital signs"""
    return await fhir_service.get_vital_signs(patient_id, date_from, date_to)

@router.get("/{patient_id}/labs")
async def get_patient_labs(
    patient_id: str,
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient lab results"""
    return await fhir_service.get_lab_results(patient_id, date_from, date_to)

@router.get("/{patient_id}/conditions")
async def get_patient_conditions(
    patient_id: str,
    clinical_status: Optional[str] = Query(None, description="Filter by clinical status (active, resolved, etc.)"),
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient conditions/problems"""
    return await fhir_service.get_conditions(patient_id, clinical_status)

@router.get("/{patient_id}/medications")
async def get_patient_medications(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient medications"""
    return await fhir_service.get_medications(patient_id)

@router.get("/{patient_id}/allergies")
async def get_patient_allergies(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient allergies"""
    return await fhir_service.get_allergies(patient_id)

@router.get("/{patient_id}/clinical-notes")
async def get_patient_clinical_notes(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient clinical notes"""
    return await fhir_service.get_clinical_notes(patient_id)

@router.get("/{patient_id}/encounters")
async def get_patient_encounters(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient encounters"""
    return await fhir_service.get_encounters(patient_id)

@router.get("/{patient_id}/observations")
async def get_patient_observations(
    patient_id: str,
    category: Optional[str] = Query(None, description="Filter by category"),
    code: Optional[str] = Query(None, description="Filter by code"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    count: Optional[int] = Query(50, description="Number of results to return"),
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient observations"""
    return await fhir_service.get_observations(
        patient_id, 
        category=category, 
        code=code, 
        date_from=date_from, 
        date_to=date_to, 
        _count=count
    )

@router.get("/{patient_id}/summary")
async def get_patient_summary(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """
    Get a summary of the patient's information, including demographics,
    vital signs, conditions, medications, allergies, and clinical notes.
    """
    import asyncio
    
    tasks = [
        fhir_service.get_patient_demographics(patient_id),
        fhir_service.get_vital_signs(patient_id),
        fhir_service.get_conditions(patient_id, clinical_status="active"),
        fhir_service.get_medications(patient_id),
        fhir_service.get_allergies(patient_id),
        fhir_service.get_clinical_notes(patient_id)
    ]
    
    try:
        demographics, vitals, conditions, medications, allergies, clinical_notes = await asyncio.gather(*tasks)
        
        return {
            "demographics": demographics,
            "vitals": vitals,
            "conditions": conditions,
            "medications": medications,
            "allergies": allergies,
            "clinical_notes": clinical_notes
        }
    except Exception as e:
        logger.error(f"Error fetching patient summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch complete patient summary: {str(e)}"
        )