import httpx
from fastapi import HTTPException

class FHIRService:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token
        
    def _get_headers(self):
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def get_patient(self, patient_id):
        """Fetch a patient resource by ID"""
        url = f"{self.base_url}/Patient/{patient_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                error_detail = f"Failed to fetch patient data: HTTP {status_code}"
                try:
                    error_body = e.response.json()
                    if "issue" in error_body:
                        error_detail += f" - {error_body['issue'][0].get('details', {}).get('text', '')}"
                except:
                    pass
                
                raise HTTPException(
                    status_code=status_code,
                    detail=error_detail
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503, 
                    detail=f"Failed to fetch patient data: {str(e)}"
                )
    
    async def get_observations(self, patient_id, category=None):
        """Fetch observations for a patient"""
        url = f"{self.base_url}/Observation?patient={patient_id}"
        
        if category:
            url += f"&category={category}"
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503, 
                    detail=f"Failed to fetch observation data: {str(e)}"
                )
    
    async def get_conditions(self, patient_id):
        """Fetch conditions for a patient"""
        url = f"{self.base_url}/Condition?patient={patient_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503, 
                    detail=f"Failed to fetch condition data: {str(e)}"
                )