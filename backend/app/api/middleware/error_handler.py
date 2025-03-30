from fastapi import Request
from fastapi.responses import JSONResponse
import logging
from typing import Callable
import traceback

logger = logging.getLogger(__name__)

async def error_handler_middleware(request: Request, call_next: Callable):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An internal server error occurred",
                "type": str(type(e).__name__),
                "path": request.url.path
            }
        )