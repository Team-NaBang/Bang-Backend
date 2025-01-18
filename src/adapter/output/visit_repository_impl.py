from port.output.visit_repository import VisitRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import VisitLog as VisitLogEntity
from fastapi import HTTPException, status


class VisitRepositoryImpl(VisitRepository):
    def __init__(self, db:Session) -> None:
        self.db = db
        
    def save(self, visit_log:VisitLogEntity) -> VisitLogEntity:        
        try:
            self.db.add(visit_log)
            self.db.commit()
            self.db.refresh(visit_log)
            return visit_log
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while working on the database: {str(e)}") from e