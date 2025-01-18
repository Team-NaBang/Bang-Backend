from abc import ABC, abstractmethod
from adapter.dto.post_dto import PostCreateRequest, PostCreateResponse, PostUpdateRequest, PostUpdateResponse, PostDetailResponse
from typing import List

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

    @abstractmethod
    def get_post_detail(self, post_id:str) -> PostDetailResponse:
        raise NotImplementedError

    @abstractmethod
    def add_like_post(self, post_id:str) -> None:
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