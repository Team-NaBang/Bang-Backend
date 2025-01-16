from abc import ABC, abstractmethod
from core.domain import Post

class PostService(ABC):
    @abstractmethod
    def create_post(self, post:Post) -> Post:
        raise NotImplementedError
    
    @abstractmethod
    def delete_post(self, post_id:str) -> None:
        raise NotImplementedError