from fastapi import APIRouter, Depends, Request, HTTPException, status
from infrastructure.sqlalchemy.config import SessionLocal
from adapter.output.post_repository_impl import PostRepositoryImpl
from adapter.output.visit_repository_impl import VisitRepositoryImpl
from core.usecase import PostUseCase, VisitUseCase
from port.input.post_app_service import PostApplicationService
from port.input.visit_app_service import VisitApplicationService
from adapter.dto.visit_dto import VisitCreateRequest
from adapter.dto.blog_dto import GetBlogMainResponse, VisitorStats
from infrastructure.slowapi.config import limiter

router = APIRouter()

def get_visit_application_service():
    db = SessionLocal()
    try:
        adapter = VisitRepositoryImpl(db)
        usecase = VisitUseCase(adapter)
        service = VisitApplicationService(usecase)
        yield service
    finally:
        db.close()

def get_post_application_service():
    db = SessionLocal()
    try:
        adapter = PostRepositoryImpl(db)
        usecase = PostUseCase(adapter)
        service = PostApplicationService(usecase)
        yield service
    finally:
        db.close()

@router.get(path='/blog',
            status_code=status.HTTP_200_OK,
            responses={
                400: {"description": "Bad Request - Invalid Input"},
                500: {"description": "Internal Server Error"},
            },
            response_model=GetBlogMainResponse)
@limiter.limit("30/minute") 
def get_blog_main(request: Request, 
                visit_app_service: VisitApplicationService = Depends(get_visit_application_service), 
                post_app_service: PostApplicationService = Depends(get_post_application_service)):
    try:
        forwarded_for = request.headers.get("X-Forwarded-For")
        client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host

        visit_app_service.create_visit(VisitCreateRequest(visitor_ip=client_ip))

        all_posts = post_app_service.get_all_post() or []
        popular_posts = post_app_service.get_popular_posts() or []
        latest_posts = post_app_service.get_latest_posts() or []
        visitor_stats = visit_app_service.get_visitor_stats()

        sanitized_data = {
            "all_posts": all_posts if all_posts is not None else [],
            "popular_posts": popular_posts if popular_posts is not None else [],
            "latest_posts": latest_posts if latest_posts is not None else [],
            "visitor_stats": [VisitorStats(**visitor_stats)] if isinstance(visitor_stats, dict) else visitor_stats or []
        }

        return GetBlogMainResponse(**sanitized_data)

    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    except KeyError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing required field: {str(err)}") from err
    except HTTPException as http_ex:
        raise http_ex 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error - {str(e)}") from e
