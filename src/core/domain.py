from pydantic import BaseModel
from enum import Enum

class Category(Enum):
    DEVELOP = "Develop"
    RECAP = "Recap"

class Post(BaseModel):
    title: str
    summary: str
    content: str
    category: Category
    authentication_code: str