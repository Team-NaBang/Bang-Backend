from enum import Enum

class Category(Enum):
    DEVELOP = "Develop"
    RECAP = "Recap"

class Post:
    title: str
    summary: str
    content: str
    category: Category

class VisitLog:
    def __init__(self, visitor_ip: str):
        self.visitor_ip = visitor_ip