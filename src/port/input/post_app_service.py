from core.usecase import PostUseCase
from core.domain import Post

class PostApplicationService:
    def __init__(self, usecase: PostUseCase):
        self.usecase = usecase

    def create_post(self, post: Post):
        return self.usecase.create_post(post)