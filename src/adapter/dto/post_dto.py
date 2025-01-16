from core.domain import Post,Category
from datetime import datetime
from infrastructure.sqlalchemy.model import Post
from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    title: str
    summary: str
    content: str
    category: Category
    authentication_code: str

    def toDomain(self):
        post = Post(title=self.title, 
                    summary=self.summary, 
                    content=self.content, 
                    category=self.category)
        return post

class PostCreateResponse(BaseModel):
    id: str
    title: str
    summary: str
    content: str
    created_at: datetime
    likes_count: int
    category: str
    
    @classmethod
    def fromEntity(cls, post: Post) -> "PostCreateResponse":
        return cls(
            id=str(post.id),
            title=post.title,
            summary=post.summary,
            content=post.content,
            created_at=post.created_at,
            likes_count=post.likes_count,
            category = post.category
        )