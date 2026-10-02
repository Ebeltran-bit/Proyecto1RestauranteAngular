from typing import List

from fastapi import APIRouter, HTTPException, status

from app.data.sample_data import CATEGORIES, CATEGORIES_BY_ID, PRODUCTS_BY_CATEGORY
from app.schemas import Category, Product

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[Category], summary="List menu categories")
def list_categories() -> List[Category]:
    return CATEGORIES


@router.get(
    "/{category_id}/products",
    response_model=List[Product],
    summary="List the products of a category",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Category not found"}},
)
def list_category_products(category_id: int) -> List[Product]:
    if category_id not in CATEGORIES_BY_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe la categoría con id {category_id}",
        )
    return PRODUCTS_BY_CATEGORY[category_id]
