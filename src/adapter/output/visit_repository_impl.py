from port.output.visit_repository import VisitRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import VisitLog as VisitLogEntity
from fastapi import HTTPException, status
from datetime import datetime

class VisitRepositoryImpl(VisitRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def save(self, visit_log: VisitLogEntity) -> VisitLogEntity:        
        try:
            self.db.add(visit_log)
            self.db.commit()
            self.db.refresh(visit_log)
            return visit_log
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - DB Operation Failed"
            )
            
    def get_today_visitor_count(self) -> int:
        today = datetime.today().date()
        try:
            return (
                self.db.query(func.count())
                .select_from(
                    self.db.query(func.date(VisitLogEntity.visit_date), VisitLogEntity.visitor_ip)
                    .filter(func.date(VisitLogEntity.visit_date) == today)  
                    .distinct() 
                    .subquery()
                )
                .scalar()
            )
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch visitor count"
            )
        
    def get_total_visitor_count(self) -> int:
        try:
            return self.db.query(VisitLogEntity.visitor_ip).distinct().count()
        except SQLAlchemyError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch total visitor count"
            )