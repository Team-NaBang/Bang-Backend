from fastapi import APIRouter, Depends, status, HTTPException, Header
from core.usecase import PostUseCase
from adapter.output.post_repository_impl import PostRepositoryImpl
from infrastructure.sqlalchemy.config import SessionLocal
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse, PostDetailResponse
from port.input.post_app_service import PostApplicationService
from cachetools import TTLCache
from time import time

router = APIRouter(prefix="/posts")

global_request_limit = TTLCache(maxsize=1000, ttl=3600)

def check_global_rate_limit():
    current_time = int(time())

    if "requests" not in global_request_limit:
        global_request_limit["requests"] = []

    recent_requests = [t for t in global_request_limit["requests"] if t > current_time - 3600]
    recent_requests.append(current_time)

    if len(recent_requests) > 10:
        raise HTTPException(status_code=429, detail="Too many overall requests, up to 10 requests per hour")

    global_request_limit["requests"] = recent_requests

def get_post_application_service():
    db = SessionLocal()
    try:
        adapter = PostRepositoryImpl(db)
        usecase = PostUseCase(adapter)
        service = PostApplicationService(usecase)
        yield service
    finally:
        db.close()

@router.post(path='', 
            status_code=status.HTTP_201_CREATED,
            responses={
                403: {"description": "Authentication Code Error"},
                500: {"description": "Internal Server Error"}
            },
            response_model=PostCreateResponse)
def create_post(post_create_request: PostCreateRequest, service: PostApplicationService = Depends(get_post_application_service)):
    try:
        return service.create_post(post_create_request)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e

@router.delete(path='/{post_id}',
            status_code=status.HTTP_200_OK,
            responses={
                403: {"description": "Authentication Code Error"},
                404: {"description": "Post Not Found"},
                500: {"description": "Internal Server Error"}
            })
def delete_post(post_id:str, authentication_code = Header(None, convert_underscores=False), service: PostApplicationService = Depends(get_post_application_service)):
    try:
        service.delete_post(post_id, authentication_code)
        return {"message":"Post deleted successfully."}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e

@router.patch(path='/{post_id}',
            status_code=status.HTTP_200_OK,
            responses={
                403: {"description": "Authentication Code Error"},
                404: {"description": "Post Not Found"},
                500: {"description": "Internal Server Error"}
            },
            response_model=PostUpdateResponse)
def update_post(post_id:str, post_update_request: PostUpdateRequest, service: PostApplicationService = Depends(get_post_application_service)):
    try:
        return service.update_post(post_id, post_update_request)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e

@router.get(path='/{post_id}',
            status_code=status.HTTP_200_OK,
            responses={
                404: {"description": "Post Not Found"},
                500: {"description": "Internal Server Error"}
            },
            response_model=PostDetailResponse)
def get_post_detail(post_id:str, service: PostApplicationService = Depends(get_post_application_service)):
    try:
        return service.get_post_detail(post_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e

@router.post(path='/{post_id}/likes',
            status_code=status.HTTP_200_OK,
            responses={
                404: {"description": "Post Not Found"},
                429: {"description": "Too Many Request"},
                500: {"description": "Internal Server Error"}
            })
def add_like_post(post_id:str, service: PostApplicationService = Depends(get_post_application_service)):
    check_global_rate_limit()
    try:
        service.add_like_post(post_id)
        return {"message":"Post deleted successfully."}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e