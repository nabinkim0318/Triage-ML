import secrets
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from app.auth.oauth import SMARTAuth

router = APIRouter()
smart_auth = SMARTAuth()

states = {}

@router.get("/login")
async def login():
    """Initiate SMART on FHIR authorization"""
    state = secrets.token_urlsafe(16)
    states[state] = True
    
    auth_url = smart_auth.get_authorization_url(state)
    
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str = None, state: str = None, error: str = None):
    """Handle OAuth2 callback from FHIR server"""
    if error:
        raise HTTPException(status_code=400, detail=f"Authorization error: {error}")
        
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code missing")
        
    if state not in states:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    del states[state]
    
    token_response = await smart_auth.exchange_code_for_token(code)
    
    return {
        "access_token": token_response.get("access_token"),
        "token_type": token_response.get("token_type", "Bearer"),
        "expires_in": token_response.get("expires_in"),
        "scope": token_response.get("scope"),
        "patient": token_response.get("patient", ""),
        "id_token": token_response.get("id_token", ""),
        "refresh_token": token_response.get("refresh_token", "")
    }

@router.get("/launch")
async def launch(iss: str = None, launch: str = None):
    if not iss or not launch:
        raise HTTPException(status_code=400, detail="Missing iss or launch parameters")
    
    state = secrets.token_urlsafe(16)
    states[state] = True
    
    params = {
        'response_type': 'code',
        'client_id': smart_auth.client_id,
        'redirect_uri': smart_auth.redirect_uri,
        'scope': 'launch patient/*.read',
        'state': state,
        'aud': iss,
        'launch': launch
    }
    
    auth_url = f"{smart_auth.auth_endpoint}?{urlencode(params)}"
    
    return RedirectResponse(auth_url)