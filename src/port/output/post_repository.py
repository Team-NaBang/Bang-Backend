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
        """
        Retrieve a post by its unique identifier.
        
        Parameters:
            post_id (str): The unique identifier of the post to retrieve.
        
        Returns:
            Post: The post object corresponding to the given post_id.
        
        Raises:
            NotImplementedError: Indicates that a concrete subclass must implement this method.
        """
        raise NotImplementedError
    
    @abstractmethod
    def update_post_likes_by_id(self, post_id:str) -> None:
        """
        Update the number of likes for a post identified by its unique identifier.
        
        Parameters:
            post_id (str): The unique identifier of the post to update likes for.
        
        Raises:
            NotImplementedError: Indicates that this method must be implemented by concrete subclasses.
        
        Notes:
            This is an abstract method that defines the contract for updating post likes in a repository.
            Concrete implementations must provide their own logic for incrementing or modifying post likes.
        """
        raise NotImplementedError