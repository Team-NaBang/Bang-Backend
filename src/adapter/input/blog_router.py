from fastapi import APIRouter, Depends, Request, HTTPException, status
from infrastructure.sqlalchemy.config import SessionLocal
from adapter.output.visit_repository_impl import VisitRepositoryImpl
from core.usecase import VisitUseCase
from port.input.visit_app_service import VisitApplicationService
from adapter.dto.visit_dto import VisitCreateRequest

router = APIRouter()

def get_post_application_service():
    db = SessionLocal()
    try:
        adapter = VisitRepositoryImpl(db)
        usecase = VisitUseCase(adapter)
        service = VisitApplicationService(usecase)
        yield service
    finally:
        db.close()

@router.get('/blog')
def get_blog_main(request:Request, serivce:VisitApplicationService = Depends(get_post_application_service)):
    try:
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host
        return serivce.create_visit(VisitCreateRequest(visitor_ip=client_ip))
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in request process: {str(e)}") from e