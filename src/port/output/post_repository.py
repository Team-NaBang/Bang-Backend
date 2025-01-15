from abc import ABC, abstractmethod
from core.domain import Post

class PostRepository(ABC):
    @abstractmethod
    def save(self, post:Post) -> Post:
        raise NotImplementedError