from abc import ABC, abstractmethod
from infrastructure.sqlalchemy.model import VisitLog

class VisitRepository(ABC):
    @abstractmethod
    def save(self, visit_log:VisitLog) -> VisitLog:
        raise NotImplementedError