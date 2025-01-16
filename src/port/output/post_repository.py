from abc import ABC, abstractmethod
from infrastructure.sqlalchemy.model import Post

class PostRepository(ABC):
    @abstractmethod
    def save(self, post:Post) -> Post:
        raise NotImplementedError