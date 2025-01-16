from enum import Enum

class Category(Enum):
    DEVELOP = "Develop"
    RECAP = "Recap"

class Post:
    title: str
    summary: str
    content: str
    category: Category