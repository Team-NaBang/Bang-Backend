from core.domain import Post,Category
from infrastructure.sqlalchemy.model import Post as PostEntity
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated

class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=20000)
    thumbnail_url: HttpUrl
    category: Category
    authentication_code: str

    def toDomain(self) -> Post:
        return Post(title=self.title, 
                    summary=self.summary, 
                    content=self.content, 
                    category=self.category,
                    thumbnail_url=self.thumbnail_url)

class PostCreateResponse(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str
    thumbnail_url: HttpUrl
    
    @classmethod
    def fromEntity(cls, post: PostEntity) -> "PostCreateResponse":
        return cls(
            id=str(post.id),
            title=post.title,
            summary=post.summary,
            content=post.content,
            created_at=post.created_at.strftime("%Y-%m-%d"),
            likes_count=post.likes_count,
            category = post.category,
            thumbnail_url = post.thumbnail_url
        )

class PostUpdateRequest(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=255)]
    summary: Annotated[str | None, Field(default=None, min_length=1, max_length=255)]
    content: Annotated[str | None, Field(default=None, min_length=1, max_length=20000)]
    category: Annotated[Category | None, Field(None)]
    thumbnail_url: Annotated[HttpUrl | None, Field(None)]
    authentication_code: str

class PostUpdateResponse(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str
    thumbnail_url: HttpUrl
    
    @classmethod
    def fromEntity(cls, post: PostEntity) -> "PostUpdateResponse":
        return cls(
            id=str(post.id),
            title=post.title,
            summary=post.summary,
            content=post.content,
            created_at=post.created_at.strftime("%Y-%m-%d"),
            likes_count=post.likes_count,
            category = post.category,
            thumbnail_url = post.thumbnail_url
        )

class PostDetailResponse(BaseModel):
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str
    thumbnail_url: HttpUrl