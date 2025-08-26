from fastapi.routing import APIRouter
from backend.settings import get_settings

settings = get_settings()

router = APIRouter()

MODEL_ID = settings.MODEL_ID


@router.get("/healthz")
async def healthz():
    """Return service liveness and the configured model identifier."""
    return {"ok": True, "model": MODEL_ID}
