from core.domain import VisitLog
from pydantic import BaseModel, IPvAnyAddress

class VisitCreateRequest(BaseModel):
    visitor_ip: IPvAnyAddress

    def toDomain(self) -> VisitLog:
        return VisitLog(visitor_ip=self.visitor_ip)