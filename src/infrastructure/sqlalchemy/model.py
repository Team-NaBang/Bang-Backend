from sqlalchemy import Column, NVARCHAR, Integer, DateTime, CHAR, TEXT
from infrastructure.sqlalchemy.config import Base
from datetime import datetime
import uuid

now = datetime.now()

class Post(Base):
    __tablename__ = "post"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(NVARCHAR(255), nullable=False)
    summary = Column(NVARCHAR(255), nullable=True)
    content = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=now.strftime("%Y-%m-%d %H:%M:%S"))
    likes_count = Column(Integer, default=0)
    category = Column(NVARCHAR(50), nullable=False)

class VisitLog(Base):
    __tablename__ = "visit_log"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visitor_ip = Column(NVARCHAR(45), nullable=False)
    visit_date = Column(DateTime, nullable=False ,default=now.strftime("%Y-%m-%d %H:%M:%S"))
    