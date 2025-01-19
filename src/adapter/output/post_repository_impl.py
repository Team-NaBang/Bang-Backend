from port.output.post_repository import PostRepository
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import Post as PostEntity
from fastapi import HTTPException, status


class PostRepositoryImpl(PostRepository):
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
                detail=f"An error occurred while working on the database: {str(e)}") from e
    
    def find_by_id(self, post_id) -> PostEntity:
        post = self.db.query(PostEntity).filter(PostEntity.id == post_id).first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    def delete_by_id(self, post_id) -> None:
        post = self.find_by_id(post_id)

        try:
            self.db.delete(post)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}"
            ) from e   
    
    def update_post_likes_by_id(self, post_id: str) -> None:
        try:
            sql = (
                update(PostEntity)  
                .where(PostEntity.id == post_id) 
                .values(likes_count=PostEntity.likes_count + 1))
            self.db.execute(sql)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}"
            ) from e   
    
    def get_all_post(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.created_at.desc()).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}"
            ) from e   
            
    def get_popular_posts(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.likes_count.desc()).limit(3).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}"
            ) from e  
            
    def get_latest_posts(self) -> list:
        try:
            return self.db.query(PostEntity).order_by(PostEntity.created_at.desc()).limit(3).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}"
            ) from e  