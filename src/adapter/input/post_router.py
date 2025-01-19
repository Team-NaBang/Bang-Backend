from fastapi import APIRouter, Depends, status, HTTPException, Header, Request
from core.usecase import PostUseCase
from adapter.output.post_repository_impl import PostRepositoryImpl
from infrastructure.sqlalchemy.config import SessionLocal
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse, PostDetailResponse
from port.input.post_app_service import PostApplicationService
from infrastructure.slowapi.config import limiter
from cachetools import TTLCache
from time import time

router = APIRouter(prefix="/posts")


global_request_limit = TTLCache(maxsize=1000, ttl=3600)

def check_global_rate_limit():
    """Check global request rate limit (Max: 10 requests per hour)"""
    current_time = int(time())

    if "requests" not in global_request_limit:
        global_request_limit["requests"] = []

    # Filter requests within the last hour
    recent_requests = [t for t in global_request_limit["requests"] if t > current_time - 3600]
    recent_requests.append(current_time)

    if len(recent_requests) > 10:
        raise HTTPException(status_code=429, detail="Too many overall requests, up to 10 requests per hour")

    global_request_limit["requests"] = recent_requests

def get_post_application_service():
    """Provide PostApplicationService instance"""
    db = SessionLocal()
    try:
        adapter = PostRepositoryImpl(db)
        usecase = PostUseCase(adapter)
        service = PostApplicationService(usecase)
        yield service
    finally:
        db.close()

@router.post("",
            status_code=status.HTTP_201_CREATED,
            responses={403: {"description": "Authentication Code Error"},
                    500: {"description": "Internal Server Error"}},
            response_model=PostCreateResponse)
@limiter.limit("5/minute") 
def create_post(request: Request, post_create_request: PostCreateRequest, service: PostApplicationService = Depends(get_post_application_service)):
    """Create a new post"""
    try:
        return service.create_post(post_create_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error - Failed to create post")

@router.delete("/{post_id}",
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "Authentication Code Error"},
                        404: {"description": "Post Not Found"},
                        500: {"description": "Internal Server Error"}})
@limiter.limit("3/minute") 
def delete_post(request: Request, post_id: str, authentication_code=Header(None, convert_underscores=False), service: PostApplicationService = Depends(get_post_application_service)):
    """Delete a post by ID"""
    try:
        service.delete_post(post_id, authentication_code)
        return {"message": "Post deleted successfully."}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error - Failed to delete post")

@router.patch("/{post_id}",
            status_code=status.HTTP_200_OK,
            responses={403: {"description": "Authentication Code Error"},
                        404: {"description": "Post Not Found"},
                        500: {"description": "Internal Server Error"}},
            response_model=PostUpdateResponse)
@limiter.limit("10/minute") 
def update_post(request: Request, post_id: str, post_update_request: PostUpdateRequest, service: PostApplicationService = Depends(get_post_application_service)):
    """Update an existing post"""
    try:
        return service.update_post(post_id, post_update_request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error - Failed to update post")

@router.get("/{post_id}",
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "Post Not Found"},
                    500: {"description": "Internal Server Error"}},
            response_model=PostDetailResponse)
@limiter.limit("50/minute") 
def get_post_detail(request: Request, post_id: str, service: PostApplicationService = Depends(get_post_application_service)):
    """Retrieve post details by ID"""
    try:
        return service.get_post_detail(post_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error - Failed to fetch post details")

@router.post("/{post_id}/likes",
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "Post Not Found"},
                        429: {"description": "Too Many Request"},
                        500: {"description": "Internal Server Error"}})
@limiter.limit("10/minute") 
def add_like_post(request: Request, post_id: str, service: PostApplicationService = Depends(get_post_application_service)):
    """Add a like to a post"""
    check_global_rate_limit()
    try:
        service.add_like_post(post_id)
        return {"message": "Added like successfully"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error - Failed to add like")
