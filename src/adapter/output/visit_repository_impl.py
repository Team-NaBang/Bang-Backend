from port.output.visit_repository import VisitRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select, exists
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.sqlalchemy.model import VisitLog as VisitLogEntity
from fastapi import HTTPException, status
from infrastructure.log.logger import logger

class VisitRepositoryImpl(VisitRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def save(self, visit_log: VisitLogEntity) -> VisitLogEntity:        
        try:
            self.db.add(visit_log)
            self.db.commit()
            self.db.refresh(visit_log)
            return visit_log
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in save(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - DB Operation Failed"
            )
    
    def exist_by_ip_and_date(self, ip: str) -> bool:
        try:
            stmt = select(exists().where(
                VisitLogEntity.visitor_ip == ip,
                func.date(VisitLogEntity.visit_date) == func.current_date()
            ))

            return self.db.execute(stmt).scalar()
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in exist_by_ip_and_date(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to check visit existence"
            )

    def get_today_visitor_count(self) -> int:
        try:
            return (
                self.db.query(func.count(func.distinct(VisitLogEntity.visitor_ip)))
                .filter(func.date(VisitLogEntity.visit_date) == func.current_date())
                .scalar()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in get_today_visitor_count(): {e}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch visitor count"
            )

    def get_total_visitor_count(self) -> int:
        try:
            return (
                self.db.query(func.count(func.distinct(VisitLogEntity.visitor_ip)))
                .scalar()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"❌ Database error in get_total_visitor_count(): {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error - Unable to fetch total visitor count"
            )
