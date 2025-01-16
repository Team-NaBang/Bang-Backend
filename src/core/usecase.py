from core.domain import Post
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import status, HTTPException
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse
from port.input.post_service import PostService
from port.output.post_repository import PostRepository
import os
from dotenv import load_dotenv

load_dotenv()

AUTHENTICATION_CODE = os.getenv("AUTHENTICATION_CODE")

if not AUTHENTICATION_CODE:
    raise ValueError("AUTHENTICATION_CODE 환경 변수가 설정되지 않았습니다.")

class PostUseCase(PostService):
    def __init__(self, post_repository:PostRepository) -> None:
        self.post_repository = post_repository
        
    def create_post(self, post_create_request: PostCreateRequest) -> PostCreateResponse:
        if post_create_request.authentication_code != AUTHENTICATION_CODE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication code not correct.")
        
        post:Post = post_create_request.toDomain()
        
        post_entity = PostEntity(title=post.title,
                                summary=post.summary,
                                content=post.content,
                                category=post.category)
        post_create_response = PostCreateResponse.fromEntity(self.post_repository.save(post_entity))
        return post_create_response