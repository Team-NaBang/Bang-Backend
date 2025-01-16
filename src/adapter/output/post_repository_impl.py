from port.output.post_repository import PostRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import HTTPException, status


class PostReposiotryImpl(PostRepository):
    def __init__(self, db:Session) -> None:
        self.db = db
        
    def save(self, post:PostEntity) -> PostEntity:        
        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except SQLAlchemyError as e:
            self.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while working on the database.") from e