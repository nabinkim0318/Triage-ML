from fastapi import HTTPException
import httpx
from urllib.parse import urlencode
from app.config.settings import settings

class SMARTAuth:
    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.redirect_uri = f"{settings.BASE_URL}/auth/callback"
        self.fhir_base_url = settings.FHIR_SERVER_URL
        
        self.auth_endpoint = settings.AUTH_SERVER_URL
        self.token_endpoint = settings.TOKEN_SERVER_URL
    
    def get_authorization_url(self, state):
        """Generate the SMART app authorization URL"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'launch/patient patient/*.read',
            'state': state,
            'aud': self.fhir_base_url
        }
        return f"{self.auth_endpoint}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, code):
        """Exchange authorization code for access token"""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id
        }
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.token_endpoint, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise HTTPException(status_code=400, detail=f"Token exchange failed: {str(e)}")