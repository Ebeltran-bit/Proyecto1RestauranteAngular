"""In-memory sample data for Phases 1 and 2.

It replaces the MySQL database until Phase 3. Lookup indexes are built once at
import time so each request is a dictionary access instead of a list scan.
"""

from typing import Dict, List

from app.schemas import Category, Order, Presentation, Product, Table

CATEGORIES: List[Category] = [
    Category(id=1, name="Bebidas"),
    Category(id=2, name="Entrantes"),
    Category(id=3, name="Carnes"),
    Category(id=4, name="Pescados"),
    Category(id=5, name="Postres"),
]

PRODUCTS: List[Product] = [
    Product(id=1, name="Agua mineral", category_id=1),
    Product(id=2, name="Refresco de cola", category_id=1),
    Product(id=3, name="Cerveza", category_id=1),
    Product(id=4, name="Patatas bravas", category_id=2),
    Product(id=5, name="Croquetas caseras", category_id=2),
    Product(id=6, name="Ensaladilla rusa", category_id=2),
    Product(id=7, name="Secreto ibérico", category_id=3),
    Product(id=8, name="Albóndigas en salsa", category_id=3),
    Product(id=9, name="Calamares a la romana", category_id=4),
    Product(id=10, name="Boquerones fritos", category_id=4),
    Product(id=11, name="Tarta de queso", category_id=5),
    Product(id=12, name="Flan casero", category_id=5),
]

PRESENTATIONS: List[Presentation] = [
    Presentation(id=1, name="Unidad"),
    Presentation(id=2, name="Tapa"),
    Presentation(id=3, name="Media ración"),
    Presentation(id=4, name="Ración"),
]

# Presentations each product can currently be ordered in. It mirrors the
# availability columns of the `Carta` table (unidad, tapa, media ración, ración).
PRODUCT_PRESENTATION_IDS: Dict[int, List[int]] = {
    1: [1],
    2: [1],
    3: [1],
    4: [2, 3, 4],
    5: [1, 3, 4],
    6: [2, 4],
    7: [3, 4],
    8: [2, 3, 4],
    9: [2, 3, 4],
    10: [2, 4],
    11: [1],
    12: [1],
}

TABLES: List[Table] = [
    Table(id=1, name="Mesa 1"),
    Table(id=2, name="Mesa 2"),
    Table(id=3, name="Mesa 3"),
    Table(id=4, name="Terraza 1"),
    Table(id=5, name="Barra"),
]

CATEGORIES_BY_ID: Dict[int, Category] = {category.id: category for category in CATEGORIES}

PRODUCTS_BY_CATEGORY: Dict[int, List[Product]] = {category.id: [] for category in CATEGORIES}
for _product in PRODUCTS:
    PRODUCTS_BY_CATEGORY[_product.category_id].append(_product)

PRESENTATIONS_BY_ID: Dict[int, Presentation] = {p.id: p for p in PRESENTATIONS}

PRODUCTS_BY_ID: Dict[int, Product] = {product.id: product for product in PRODUCTS}

PRODUCT_PRESENTATIONS: Dict[int, List[Presentation]] = {
    product_id: [PRESENTATIONS_BY_ID[pid] for pid in presentation_ids]
    for product_id, presentation_ids in PRODUCT_PRESENTATION_IDS.items()
}

TABLES_BY_ID: Dict[int, Table] = {table.id: table for table in TABLES}

# Orders the API starts with, so a table already has something to list.
SAMPLE_ORDERS: List[Order] = [
    Order(id=1, table_id=1, product_id=3, presentation_id=1, quantity=2),
    Order(id=2, table_id=1, product_id=4, presentation_id=4, quantity=1),
    Order(id=3, table_id=2, product_id=9, presentation_id=3, quantity=1),
]
