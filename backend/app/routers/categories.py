from typing import List

from fastapi import APIRouter, Depends, status

from app.data.sample_data import CATEGORIES, PRODUCTS_BY_CATEGORY
from app.routers.dependencies import get_category_or_404
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
def list_category_products(category: Category = Depends(get_category_or_404)) -> List[Product]:
    return PRODUCTS_BY_CATEGORY[category.id]
