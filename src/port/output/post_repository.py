from abc import ABC, abstractmethod
from infrastructure.sqlalchemy.model import Post

class PostRepository(ABC):
    @abstractmethod
    def save(self, post:Post) -> Post:
        raise NotImplementedError
    
    @abstractmethod
    def delete_by_id(self, post_id) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, post_id) -> Post:
        raise NotImplementedError