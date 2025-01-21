from pydantic import BaseModel, Field, HttpUrl
from typing import List

class VisitorStats(BaseModel):
    today_visitor: int
    total_visitor: int

class PostSummary(BaseModel):
    id: str
    title: str
    created_at: str
    likes: int

class PostDetail(PostSummary):
    summary: str
    thumbnail_url: HttpUrl

class GetBlogMainResponse(BaseModel):
    all_posts: List[PostDetail] = Field(default_factory=list)
    popular_posts: List[PostSummary] = Field(default_factory=list)
    latest_posts: List[PostSummary] = Field(default_factory=list)
    visitor_stats: List[VisitorStats] = Field(default_factory=list)