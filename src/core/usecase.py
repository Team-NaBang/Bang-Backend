from core.domain import Post
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import status, HTTPException
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse
from port.input.post_service import PostService
from port.output.post_repository import PostRepository
from dotenv import load_dotenv
import hmac
import os

load_dotenv()

AUTHENTICATION_CODE = os.getenv("AUTHENTICATION_CODE")

if not AUTHENTICATION_CODE:
    raise ValueError("AUTHENTICATION_CODE 환경 변수가 설정되지 않았습니다.")

class PostUseCase(PostService):
    def __init__(self, post_repository:PostRepository) -> PostCreateResponse:
        self.post_repository = post_repository
        
    def create_post(self, post_create_request: PostCreateRequest) -> PostCreateResponse:
        if not hmac.compare_digest(post_create_request.authentication_code, AUTHENTICATION_CODE):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication code not correct.")
        
        post:Post = post_create_request.toDomain()
        
        post_entity = PostEntity(title=post.title,
                                summary=post.summary,
                                content=post.content,
                                category=post.category)
        post_create_response = PostCreateResponse.fromEntity(self.post_repository.save(post_entity))
        return post_create_response
    
    def delete_post(self, post_id, authentication_code) -> None:
        if not hmac.compare_digest(authentication_code, AUTHENTICATION_CODE):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication code not correct.")
        
        self.post_repository.delete_by_id(post_id)
    
    def update_post(self, post_id:str, post_update_request: PostUpdateRequest) -> PostUpdateResponse:
        if not hmac.compare_digest(post_update_request.authentication_code, AUTHENTICATION_CODE):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication code not correct.")
        
        post:PostEntity = self.post_repository.find_by_id(post_id)
        
        if post_update_request.title: post.title = post_update_request.title
        if post_update_request.summary: post.summary = post_update_request.summary
        if post_update_request.content: post.content = post_update_request.content
        if post_update_request.category: post.category = post_update_request.category
        
        return self.post_repository.save(post)