from typing import List

from fastapi import APIRouter, Depends, status

from app.data.sample_data import TABLES
from app.routers.dependencies import get_table_or_404
from app.schemas import Table

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("", response_model=List[Table], summary="List restaurant tables")
def list_tables() -> List[Table]:
    return TABLES


@router.get(
    "/{table_id}",
    response_model=Table,
    summary="Select a table",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Table not found"}},
)
def get_table(table: Table = Depends(get_table_or_404)) -> Table:
    return table
