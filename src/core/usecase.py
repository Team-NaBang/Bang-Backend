from core.domain import Post, VisitLog
from infrastructure.sqlalchemy.model import Post as PostEntity
from infrastructure.sqlalchemy.model import VisitLog as VisitLogEntity
from fastapi import status, HTTPException
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostDetailResponse, PostUpdateRequest, PostUpdateResponse
from adapter.dto.visit_dto import VisitCreateRequest
from port.input.post_service import PostService
from port.input.visit_service import VisitService
from port.output.post_repository import PostRepository
from port.output.visit_repository import VisitRepository
from infrastructure.env_variable import AUTHENTICATION_CODE
import hmac

if not AUTHENTICATION_CODE:
    raise ValueError("AUTHENTICATION_CODE 환경 변수가 설정되지 않았습니다.")

class PostUseCase(PostService):
    def __init__(self, post_repository:PostRepository) -> None:
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
        
        if post_update_request.title: 
            post.title = post_update_request.title
        if post_update_request.summary: 
            post.summary = post_update_request.summary
        if post_update_request.content: 
            post.content = post_update_request.content
        if post_update_request.category: 
            post.category = post_update_request.category
        
        return PostUpdateResponse.fromEntity(self.post_repository.save(post))
    
    def get_post_detail(self, post_id: str) -> PostDetailResponse:
        post = self.post_repository.find_by_id(post_id)
        return PostDetailResponse(title=post.title,
                                summary=post.summary,
                                content=post.content,
                                created_at=post.created_at.strftime("%Y-%m-%d"),
                                likes_count=post.likes_count,
                                category=post.category)
    
    def add_like_post(self, post_id: str) -> None:
        self.post_repository.update_post_likes_by_id(post_id)
        
        
    def _format_post_response(self, post) -> dict:
        return {
            "id": post.id,
            "title": post.title,
            "created_at": post.created_at.strftime("%Y-%m-%d"),
            "likes": post.likes_count
        }
        
    def get_all_post(self) -> list:
        posts = self.post_repository.get_all_post()
        return [self._format_post_response(post) | {"summary": post.summary} for post in posts]
    
    def get_popular_posts(self) -> list:
        posts = self.post_repository.get_popular_posts()
        return [self._format_post_response(post) for post in posts]
        
    def get_latest_posts(self) -> list:
        posts = self.post_repository.get_latest_posts()
        return [self._format_post_response(post) for post in posts]

class VisitUseCase(VisitService):
    def __init__(self, visit_repository:VisitRepository) -> None:
        self.visit_repository = visit_repository
    
    def create_visit(self, visit_create_request:VisitCreateRequest) -> None:
        visit_log:VisitLog = visit_create_request.toDomain()
        
        visit_log_entity = VisitLogEntity(visitor_ip = visit_log.visitor_ip)
        
        self.visit_repository.save(visit_log_entity)
        
    def get_visitor_stats(self) -> dict:
        today_visitor = self.visit_repository.get_today_visitor_count()
        total_visitor = self.visit_repository.get_total_visitor_count()
        return {
            "today_visitor":today_visitor,
            "total_visitor":total_visitor
        }
