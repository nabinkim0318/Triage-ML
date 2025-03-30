from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.fhir_service import FHIRService
from app.config.settings import settings
from typing import Optional

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

@router.get("/{patient_id}/vitals")
async def get_patient_vitals(
    patient_id: str, 
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient vital signs"""
    return await fhir_service.get_observations(patient_id, category="vital-signs")

@router.get("/{patient_id}/conditions")
async def get_patient_conditions(
    patient_id: str, 
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    """Get patient conditions/problems"""
    return await fhir_service.get_conditions(patient_id)