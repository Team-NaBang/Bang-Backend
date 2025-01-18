from pydantic import BaseModel, Field
from typing import List, Dict

class VisitorStats(BaseModel):
    today_visitor: int
    total_visitor: int

class GetBlogMainResponse(BaseModel):
    all_posts: List[dict] = Field(default_factory=list)
    popular_posts: List[dict] = Field(default_factory=list)
    latest_posts: List[dict] = Field(default_factory=list)
    visitor_stats: List[VisitorStats] = Field(default_factory=list) 