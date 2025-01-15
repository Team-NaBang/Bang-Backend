from port.output.post_repository import PostRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.domain import Post
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

AUTHENTICATION_CODE = os.getenv("AUTHENTICATION_CODE")

if not AUTHENTICATION_CODE:
    raise ValueError("AUTHENTICATION_CODE 환경 변수가 설정되지 않았습니다.")

class PostReposiotryImpl(PostRepository):
    def __init__(self, db:Session) -> None:
        self.db = db
        
    def save(self, post:Post) -> PostEntity:
        if post.authentication_code != AUTHENTICATION_CODE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication code not correct.")
        
        try:
            post_entity = PostEntity(**post.model_dump(exclude={"authentication_code"}))
            self.db.add(post_entity)
            self.db.commit()
            self.db.refresh(post_entity)
            return post_entity
        except SQLAlchemyError as e:
            self.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 작업 중 오류가 발생했습니다.") from e