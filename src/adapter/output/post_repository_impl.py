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
        """
        Delete a post from the database by its unique identifier.
        
        Attempts to remove a specific post from the database using its post ID. 
        First verifies the post's existence by calling `find_by_id`, then attempts 
        to delete the post and commit the transaction.
        
        Parameters:
            post_id (str): The unique identifier of the post to be deleted.
        
        Raises:
            HTTPException: 
                - 404 status if the post is not found (via find_by_id)
                - 500 status if a database error occurs during deletion
        
        Side Effects:
            - Commits the database transaction if deletion is successful
            - Rolls back the transaction if an error occurs
        """
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
        """
        Increments the likes count for a specific post by its ID.
        
        Attempts to update the likes count of a post in the database by incrementing the current likes count by one. 
        If the post with the given ID does not exist or a database error occurs, an appropriate exception is raised.
        
        Args:
            post_id (str): The unique identifier of the post to update.
        
        Raises:
            HTTPException: A 500 Internal Server Error if a database operation fails, 
                           with details about the specific error encountered.
        """
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