from fastapi import FastAPI
from adapter.input.post_router import router as post_router

app = FastAPI()

app.include_router(post_router, prefix="/api/v1")