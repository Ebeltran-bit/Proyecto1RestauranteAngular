from typing import List

from fastapi import APIRouter

from app.data.sample_data import TABLES
from app.schemas import Table

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("", response_model=List[Table], summary="List restaurant tables")
def list_tables() -> List[Table]:
    return TABLES
