from typing import Dict

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Check that the API is running")
def health() -> Dict[str, str]:
    return {"status": "ok"}
