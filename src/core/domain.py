from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4
from enum import Enum

class Category(Enum):
    DEVELOP = "Develop"
    RECAP = "Recap"

class Post(BaseModel):
    id: UUID4
    title: str
    summary: str
    content: str
    created_at: datetime
    likes_count: int
    category: Category