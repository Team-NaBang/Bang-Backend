from abc import ABC, abstractmethod

class VisitService(ABC):
    @abstractmethod
    def create_visit(self) -> None:
        raise NotImplementedError