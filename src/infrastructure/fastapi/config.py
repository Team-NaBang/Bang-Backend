from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.env_variable import CLIENT_DOMAIN
from slowapi.middleware import SlowAPIMiddleware
from infrastructure.log import logger
from main import app


app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_DOMAIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "authentication-code", "X-Forwarded-For"],
)

app.add_middleware(SlowAPIMiddleware)

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"  
    response.headers["X-Content-Type-Options"] = "nosniff"  
    response.headers["Content-Security-Policy"] = "default-src 'self'" 
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
