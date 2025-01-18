from abc import ABC, abstractmethod
from infrastructure.sqlalchemy.model import Post

class PostRepository(ABC):
    @abstractmethod
    def save(self, post:Post) -> Post:
        raise NotImplementedError
    
    @abstractmethod
    def delete_by_id(self, post_id:str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, post_id:str) -> Post:
        raise NotImplementedError
    
    @abstractmethod
    def update_post_likes_by_id(self, post_id:str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_all_post(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def get_popular_posts(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def get_latest_posts(self) -> list:
        raise NotImplementedError