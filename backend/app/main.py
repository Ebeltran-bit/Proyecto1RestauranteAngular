from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import categories, health, orders, products, tables

STATIC_DIR = Path(__file__).parent / "static"

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

# Interfaz visual para el personal de sala: http://127.0.0.1:8000/
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def waiter_interface() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
