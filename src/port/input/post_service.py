from abc import ABC, abstractmethod
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse

class PostService(ABC):
    @abstractmethod
    def create_post(self, post_create_request:PostCreateRequest) -> PostCreateResponse:
        raise NotImplementedError
    
    @abstractmethod
    def delete_post(self, post_id:str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update_post(self, post_id:str, post_update_request:PostUpdateRequest) -> PostUpdateResponse:
        raise NotImplementedError