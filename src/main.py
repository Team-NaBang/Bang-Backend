from fastapi import FastAPI
from adapter.input.post_router import router as post_router
from adapter.input.blog_router import router as blog_router

app = FastAPI()

app.include_router(post_router, prefix="/api/v1")
app.include_router(blog_router, prefix="/api/v1")