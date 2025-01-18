from abc import ABC, abstractmethod
from adapter.dto.visit_dto import VisitCreateRequest

class VisitService(ABC):
    @abstractmethod
    def create_visit(self, visit_create_request:VisitCreateRequest) -> None:
        raise NotImplementedError