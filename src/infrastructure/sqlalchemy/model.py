from sqlalchemy import Column, String, Integer, DateTime, CHAR, Text, Date, func, UniqueConstraint
from infrastructure.sqlalchemy.config import Base
from datetime import datetime
import uuid

class Post(Base):
    __tablename__ = "post"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    summary = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    likes_count = Column(Integer, default=0)
    category = Column(String(50), nullable=False)  
    thumbnail_url = Column(String(2083), nullable=False)  


class VisitLog(Base):
    __tablename__ = "visit_log"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visitor_ip = Column(String(45), nullable=False)  
    visit_date = Column(Date, nullable=False, server_default=func.current_date())