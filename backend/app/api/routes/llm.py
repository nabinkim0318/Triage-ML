# api/routes/llm.py

from fastapi import APIRouter, HTTPException
from app.schemas.triage import LLMRequest, LLMResponse
from app.logic.scorer import TriageScorer
from app.config.settings import settings  
import logging
import openai

router = APIRouter()

if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    print("⚠️ OPENAI_API_KEY is not set")
    
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=LLMResponse)
async def predict_with_llm(request: LLMRequest):
    try:
        scorer = TriageScorer(strategy="llm")  # change to "rule" to test rule-based
        result = await scorer.predict(request)
        return LLMResponse(**result)
    except Exception as e:
        logger.exception("Scoring failed.")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")
