"""Shared lookups for path parameters.

Each function is a FastAPI dependency: it returns the resource or answers 404
with a clear message, so the endpoints only deal with the happy path.
"""

from fastapi import Depends, HTTPException, status

from app.data.order_store import order_store
from app.data.sample_data import CATEGORIES_BY_ID, PRODUCTS_BY_ID, TABLES_BY_ID
from app.schemas import Category, Order, Product, Table


def _not_found(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


def get_category_or_404(category_id: int) -> Category:
    category = CATEGORIES_BY_ID.get(category_id)
    if category is None:
        raise _not_found(f"No existe la categoría con id {category_id}")
    return category


def get_product_or_404(product_id: int) -> Product:
    product = PRODUCTS_BY_ID.get(product_id)
    if product is None:
        raise _not_found(f"No existe el producto con id {product_id}")
    return product


def get_table_or_404(table_id: int) -> Table:
    table = TABLES_BY_ID.get(table_id)
    if table is None:
        raise _not_found(f"No existe la mesa con id {table_id}")
    return table


def get_order_or_404(order_id: int, table: Table = Depends(get_table_or_404)) -> Order:
    order = order_store.get(order_id)
    if order is None or order.table_id != table.id:
        raise _not_found(f"La mesa {table.id} no tiene ningún pedido con id {order_id}")
    return order
