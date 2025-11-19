from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.responses import JSONResponse
from routes import (nlp_routes)
from fastapi.exceptions import RequestValidationError
import uvicorn
# cron here if this one has to be inside the same app

hf = FastAPI(title="API Hugging Face")

# Aquí agregás tu exception handler personalizado
@hf.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error for: {request.url}")
    logging.error(exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger("python_multipart.multipart").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
# Incluir routers
hf.include_router(nlp_routes.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:hf",  
        host="0.0.0.0",
        port=7000
    )
