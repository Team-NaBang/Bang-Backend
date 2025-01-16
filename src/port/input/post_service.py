from abc import ABC, abstractmethod
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse, PostDetailResponse

class PostService(ABC):
    @abstractmethod
    def create_post(self, post_create_request:PostCreateRequest) -> PostCreateResponse:
        """
        Create a new post based on the provided post creation request.
        
        Parameters:
            post_create_request (PostCreateRequest): Request object containing details for creating a new post
        
        Returns:
            PostCreateResponse: Response object representing the result of post creation
        
        Raises:
            NotImplementedError: Indicates that this method must be implemented by a concrete subclass
        """
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id:str) -> None:
        """
        Delete a post by its unique identifier.
        
        Parameters:
            post_id (str): The unique identifier of the post to be deleted.
        
        Raises:
            NotImplementedError: Indicates that this method must be implemented by a concrete subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id:str, post_update_request:PostUpdateRequest) -> PostUpdateResponse:
        """
        Update an existing post with new information.
        
        Parameters:
            post_id (str): The unique identifier of the post to be updated
            post_update_request (PostUpdateRequest): A request object containing the updated post details
        
        Returns:
            PostUpdateResponse: A response object representing the result of the post update operation
        
        Raises:
            NotImplementedError: Indicates that this method must be implemented by a concrete subclass
        """
        raise NotImplementedError

    @abstractmethod
    def get_post_detail(self, post_id:str) -> PostDetailResponse:
        """
        Retrieve detailed information about a specific post.
        
        Parameters:
            post_id (str): Unique identifier of the post to retrieve details for
        
        Returns:
            PostDetailResponse: Comprehensive details of the requested post
        
        Raises:
            NotImplementedError: Indicates that a concrete implementation must be provided by subclasses
        """
        raise NotImplementedError

    @abstractmethod
    def add_like_post(self, post_id:str) -> None:
        """
        Add a like to a specific post.
        
        Parameters:
            post_id (str): The unique identifier of the post to be liked.
        
        Raises:
            NotImplementedError: Indicates that this method must be implemented by a concrete subclass.
        
        Notes:
            This is an abstract method that defines the contract for liking a post in the service layer.
            Concrete implementations should provide the actual logic for adding a like to a post.
        """
        raise NotImplementedError