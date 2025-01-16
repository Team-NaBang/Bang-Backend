from core.usecase import PostUseCase
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse
from core.domain import Post

class PostApplicationService:
    def __init__(self, usecase: PostUseCase):
        self.usecase = usecase

    def create_post(self, post_create_request: PostCreateRequest) -> PostCreateResponse:
        return self.usecase.create_post(post_create_request)
    
    def delete_post(self, post_id, authentication_code) -> None:
        self.usecase.delete_post(post_id, authentication_code)