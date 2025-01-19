from port.output.post_repository import PostRepository
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import HTTPException, status
from infrastructure.log.logger import logger

class PostRepositoryImpl(PostRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def save(self, post: PostEntity) -> PostEntity:        
        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in save(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - DB Operation Failed"
            )
    
    def find_by_id(self, post_id: str) -> PostEntity:
        post = self.db.query(PostEntity).filter(PostEntity.id == post_id).first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    def delete_by_id(self, post_id: str) -> None:
        post = self.find_by_id(post_id)
        try:
            self.db.delete(post)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in delete_by_id(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to delete post"
            )
    
    def update_post_likes_by_id(self, post_id: str) -> None:
        try:
            sql = (
                update(PostEntity)
                .where(PostEntity.id == post_id)
                .values(likes_count=PostEntity.likes_count + 1) 
                .execution_options(synchronize_session="fetch")  
            )
            self.db.execute(sql)
            self.db.commit()
        except SQLAlchemyError as e:
            logger.error(f"❌ Database error in update_post_likes_by_id(): {e}") 
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to update post likes"
            )
    
    def get_all_post(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"❌ Database error in get_all_post(): {e}") 
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch posts"
            )
            
    def get_popular_posts(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.likes_count.desc()).limit(3).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in get_popular_posts(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch popular posts"
            )
            
    def get_latest_posts(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.created_at.desc()).limit(3).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in get_latest_posts(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch latest posts"
            )