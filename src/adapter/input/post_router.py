from fastapi import APIRouter, Depends, status, HTTPException
from core.usecase import PostUseCase
from adapter.output.post_repository_impl import PostReposiotryImpl
from infrastructure.sqlalchemy.config import SessionLocal
from core.domain import Post
from port.input.post_app_service import PostApplicationService

router = APIRouter(prefix="/posts")

def get_post_application_service():
    db = SessionLocal()
    try:
        adapter = PostReposiotryImpl(db)
        usecase = PostUseCase(adapter)
        service = PostApplicationService(usecase)
        yield service
    finally:
        db.close()

@router.post(path='', 
            status_code=status.HTTP_201_CREATED,
            responses={
                403: {"description": "인증 코드가 올바르지 않음"},
                500: {"description": "서버 내부 오류"}
            })
def create_post(post: Post, service: PostApplicationService = Depends(get_post_application_service)):
    try:
        return service.create_post(post)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )