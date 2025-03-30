from fastapi import APIRouter, Depends, HTTPException, Header, Query
from app.services.fhir_service import FHIRService
from app.config.settings import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_fhir_service(authorization: Optional[str] = Header(None)):
    """Dependency to inject FHIR service with authentication"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid authorization token required")
    
    token = authorization.replace("Bearer ", "")
    return FHIRService(settings.FHIR_SERVER_URL, token)

@router.get("/{patient_id}")
async def get_patient(
    patient_id: str, 
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient details by ID"""
    return await fhir_service.get_patient(patient_id)

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