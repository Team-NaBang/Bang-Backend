from core.usecase import PostUseCase
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse, PostDetailResponse
from core.domain import Post

class PostApplicationService:
    def __init__(self, usecase: PostUseCase):
        self.usecase = usecase

    def create_post(self, post_create_request: PostCreateRequest) -> PostCreateResponse:
        """
        Create a new post using the provided post creation request.
        
        Parameters:
            post_create_request (PostCreateRequest): Request containing details for creating a new post
        
        Returns:
            PostCreateResponse: Response containing details of the newly created post
        """
        return self.usecase.create_post(post_create_request)

    def delete_post(self, post_id:str, authentication_code) -> None:
        """
        Delete a post using its unique identifier and authentication code.
        
        Parameters:
            post_id (str): The unique identifier of the post to be deleted
            authentication_code: Authentication credentials required to authorize post deletion
        
        Raises:
            Potential exceptions from underlying use case method related to authentication or post deletion
        """
        self.usecase.delete_post(post_id, authentication_code)

    def update_post(self, post_id:str, post_update_request: PostUpdateRequest) -> PostUpdateResponse:
        """
        Update an existing post with new information.
        
        Parameters:
            post_id (str): The unique identifier of the post to be updated
            post_update_request (PostUpdateRequest): Request object containing updated post details
        
        Returns:
            PostUpdateResponse: Response object representing the result of the post update operation
        
        Delegates the update operation to the underlying use case, transforming the request and returning the response.
        """
        return self.usecase.update_post(post_id, post_update_request)

    def get_post_detail(self, post_id:str) -> PostDetailResponse:
        """
        Retrieve detailed information about a specific post.
        
        Parameters:
            post_id (str): Unique identifier of the post to retrieve details for
        
        Returns:
            PostDetailResponse: Comprehensive details of the requested post
        """
        return self.usecase.get_post_detail(post_id)

    def add_like_post(self, post_id:str) -> None:
        """
        Add a like to a specific post.
        
        Parameters:
            post_id (str): The unique identifier of the post to be liked
        
        Raises:
            ValueError: If the post_id is invalid or empty
        """
        self.usecase.add_like_post(post_id)