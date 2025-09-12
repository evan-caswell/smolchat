from fastapi.routing import APIRouter
from backend.settings import settings

router = APIRouter()

MODEL_ID = settings.MODEL_ID


@router.get("/healthz")
async def healthz() -> dict[str, object]:
    """Return service liveness and the configured model identifier."""
    return {"ok": True, "model": MODEL_ID}
