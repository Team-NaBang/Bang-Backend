from core.usecase import VisitUseCase
from adapter.dto.visit_dto import VisitCreateRequest

class VisitApplicationService:
    def __init__(self, usecase: VisitUseCase):
        self.usecase = usecase
        
    def create_visit(self, visit_create_request:VisitCreateRequest) -> None:
        self.usecase.create_visit(visit_create_request)