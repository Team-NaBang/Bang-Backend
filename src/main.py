from fastapi import FastAPI
from adapter.input.post_router import router as post_router
from adapter.input.blog_router import router as blog_router

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

app.include_router(post_router, tags=["Post API"])
app.include_router(blog_router, tags=["Blog API"])