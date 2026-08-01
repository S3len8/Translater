from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from core.postgre import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.export import ExportRepository
from services.export import ExportService


router = APIRouter()


def export_service(db: AsyncSession = Depends(get_db)) -> ExportService:
    repository = ExportRepository(db)
    return ExportService(repository)


@router.get("/export")
async def create_excel(service: ExportService = Depends(export_service)):
    result = await service.create_excel()
    return StreamingResponse(
        result,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": (
                "attachment; filename=translation_history.xlsx"
            )
        },
    )