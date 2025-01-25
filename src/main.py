from fastapi import FastAPI
from adapter.input.post_router import router as post_router
from adapter.input.blog_router import router as blog_router
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.env_variable import CLIENT_DOMAIN
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware
from infrastructure.log.logger import logger
from infrastructure.slowapi.config import limiter

app = FastAPI(
    title="My Blog API",
    description="A FastAPI backend for managing blog posts and user interactions.",
    version="1.0.0",
    contact={
        "name": "Na Byunghyun",
        "url": "https://iambottle.com",
        "email": "nbhyun0329@gmail.com",
    },
    docs_url="/docs",  
    redoc_url="/redoc", 
    openapi_url="/openapi.json", 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_DOMAIN],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "authentication-code", "X-Forwarded-For"],
)

app.state.limiter = limiter

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


app.include_router(post_router, tags=["Post API"])
app.include_router(blog_router, tags=["Blog API"])