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
    """
    Check and enforce a global rate limit for requests.
    
    This function manages a global request limit of 10 requests per hour. It tracks request timestamps
    and raises an HTTP 429 (Too Many Requests) exception if the limit is exceeded.
    
    Raises:
        HTTPException: If more than 10 requests are made within a one-hour window, with a 429 status code.
    
    Side Effects:
        - Updates the global_request_limit dictionary with current request timestamps
        - Filters out timestamps older than one hour
    """
    current_time = int(time())

    if "requests" not in global_request_limit:
        global_request_limit["requests"] = []

    recent_requests = [t for t in global_request_limit["requests"] if t > current_time - 3600]
    recent_requests.append(current_time)

    if len(recent_requests) > 10:
        raise HTTPException(status_code=429, detail="Too many overall requests, up to 10 requests per hour")

    global_request_limit["requests"] = recent_requests

def get_post_application_service():
    """
    Dependency function to create and manage a PostApplicationService with a database session.
    
    Creates a database session, initializes a PostApplicationService with a repository and use case, 
    and ensures the database session is properly closed after use.
    
    Yields:
        PostApplicationService: A service instance for handling post-related operations
    
    Notes:
        - Uses dependency injection to provide a configured service
        - Automatically closes the database session after the service is used
        - Intended for use with FastAPI's dependency injection system
    """
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
    """
    Create a new post using the provided post creation request.
    
    Parameters:
        post_create_request (PostCreateRequest): The details of the post to be created
        service (PostApplicationService, optional): Application service for post management, automatically injected
    
    Returns:
        PostCreateResponse: The response containing details of the created post
    
    Raises:
        HTTPException: If there is an error during post creation, with appropriate status codes
            - Specific HTTP exceptions from service layer
            - 500 Internal Server Error for unexpected exceptions
    """
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
    """
    Delete a post by its unique identifier.
    
    Parameters:
        post_id (str): The unique identifier of the post to be deleted
        authentication_code (str, optional): Authentication code for post deletion authorization
        service (PostApplicationService): Service responsible for post-related operations
    
    Returns:
        dict: A dictionary with a success message upon post deletion
    
    Raises:
        HTTPException: If authentication fails or an internal server error occurs
        - 401 Unauthorized: If authentication is invalid
        - 404 Not Found: If the post does not exist
        - 500 Internal Server Error: For unexpected errors during deletion process
    """
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
    """
    Retrieve the details of a specific post by its unique identifier.
    
    Parameters:
        post_id (str): The unique identifier of the post to retrieve
        service (PostApplicationService, optional): Application service for post-related operations, automatically injected
    
    Returns:
        PostDetailResponse: Detailed information about the requested post
    
    Raises:
        HTTPException: If the post cannot be found (404) or an internal server error occurs (500)
    """
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
    """
    Add a like to a specific post.
    
    Adds a like to the post identified by the given post_id. This endpoint is rate-limited to prevent abuse.
    
    Parameters:
        post_id (str): Unique identifier of the post to be liked
        service (PostApplicationService, optional): Application service for post-related operations. Defaults to dependency injection.
    
    Returns:
        dict: A dictionary with a success message upon successfully adding a like
    
    Raises:
        HTTPException: 
            - 429 Too Many Requests if global rate limit is exceeded
            - 500 Internal Server Error for unexpected processing errors
    
    Side Effects:
        - Increments the like count for the specified post
        - Tracks and limits global request rate
    """
    check_global_rate_limit()
    try:
        service.add_like_post(post_id)
        return {"message":"Added like successfully"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e