from core.domain import Post
from port.input.post_service import PostService
from port.output.post_repository import PostRepository

class PostUseCase(PostService):
    def __init__(self, post_repository:PostRepository) -> None:
        self.post_repository = post_repository
        
    def create_post(self, post: Post) -> Post:
        return self.post_repository.save(post)