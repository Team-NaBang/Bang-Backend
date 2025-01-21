from enum import Enum

class Category(Enum):
    DEVELOP = "Develop"
    RECAP = "Recap"

class Post:
    def __init__(self, title: str, summary: str, content: str, category: Category, thumbnail_url:str):
        self.title = title
        self.summary = summary
        self.content = content
        self.category = category
        self.thumbnail_url = thumbnail_url

class VisitLog:
    def __init__(self, visitor_ip: str):
        self.visitor_ip = visitor_ip