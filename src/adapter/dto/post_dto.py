from core.domain import Post,Category
from infrastructure.sqlalchemy.model import Post as PostEntity
from pydantic import BaseModel, Field
from typing import Annotated

class PostCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=20000)
    category: Category
    authentication_code: str

    def toDomain(self) -> Post:
        return Post(title=self.title, 
                    summary=self.summary, 
                    content=self.content, 
                    category=self.category)

class PostCreateResponse(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str
    
    @classmethod
    def fromEntity(cls, post: PostEntity) -> "PostCreateResponse":
        return cls(
            id=str(post.id),
            title=post.title,
            summary=post.summary,
            content=post.content,
            created_at=post.created_at,
            likes_count=post.likes_count,
            category = post.category
        )

class PostUpdateRequest(BaseModel):
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=255)]
    summary: Annotated[str | None, Field(default=None, min_length=1, max_length=255)]
    content: Annotated[str | None, Field(default=None, min_length=1, max_length=20000)]
    category: Annotated[Category | None, Field(None)]
    authentication_code: str

class PostUpdateResponse(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str

class PostDetailResponse(BaseModel):
    title: str
    summary: str
    content: str
    created_at: str
    likes_count: int
    category: str