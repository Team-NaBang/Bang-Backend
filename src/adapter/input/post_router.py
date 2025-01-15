from fastapi import APIRouter, Depends, status
from core.usecase import PostUseCase
from adapter.output.post_repository_impl import PostReposiotryImpl
from infrastructure.sqlalchemy.config import SessionLocal
from core.domain import Post
from port.input.post_app_service import PostApplicationService

router = APIRouter(prefix="/posts")

def get_post_application_service():
    db = SessionLocal()
    adapter = PostReposiotryImpl(db)
    usecase = PostUseCase(adapter)
    return PostApplicationService(usecase)

@router.post(path='', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, service: PostApplicationService = Depends(get_post_application_service)):
    return service.create_post(post)