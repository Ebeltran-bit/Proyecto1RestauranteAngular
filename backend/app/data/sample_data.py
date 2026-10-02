"""In-memory sample data for Phase 1.

It replaces the MySQL database until Phase 3. Lookup indexes are built once at
import time so each request is a dictionary access instead of a list scan.
"""

from typing import Dict, List

from app.schemas import Category, Product, Table

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
