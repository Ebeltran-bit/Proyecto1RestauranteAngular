from fastapi import FastAPI

from app.routers import categories, health, orders, products, tables

app = FastAPI(
    title="Restaurant Orders API",
    description="API REST para que el personal de sala gestione los pedidos de las mesas.",
    version="0.2.0",
)

app.include_router(health.router)
app.include_router(tables.router)
app.include_router(orders.router)
app.include_router(categories.router)
app.include_router(products.router)
