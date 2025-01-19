from abc import ABC, abstractmethod
from infrastructure.sqlalchemy.model import VisitLog

class VisitRepository(ABC):
    @abstractmethod
    def save(self, visit_log:VisitLog) -> VisitLog:
        raise NotImplementedError
    
    @abstractmethod
    def get_today_visitor_count(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def get_total_visitor_count(self) -> int:
        raise NotImplementedError