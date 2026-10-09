# Memoria del proyecto

Registro de cada decisión de desarrollo y de cada cambio, en orden cronológico.
Cada entrada indica la fecha, la fase, qué se decidió o cambió y por qué.

## Punto de partida (2026-10-02)

- El repositorio contenía un proyecto Angular 21 generado con Angular CLI
  (componente `header`, modelo y servicio `Product` vacíos).
- El enunciado ("Proyecto previo a Angular") pide primero una API REST en Python con
  FastAPI; el cliente Angular se construirá después sobre esa API.
- Se trabaja por fases. Solo se desarrolla la fase en curso hasta que David indique lo contrario.

## Fase 1: Primer servicio y exploración del dominio

### Decisiones (2026-10-02)

| # | Decisión | Motivo |
|---|----------|--------|
| 1 | El backend va en la carpeta `backend/` del mismo repositorio y Angular se queda en la raíz sin tocar | Aprobado por David. Mantiene juntos cliente y API sin romper el trabajo de otras ramas |
| 2 | Compatibilidad con Python 3.9 | Es la versión instalada en el PC de David (3.9.2). El código evita sintaxis de 3.10+ (por ejemplo `X \| None`) |
| 3 | Paquetes: `fastapi==0.128.8`, `uvicorn[standard]==0.39.0`, `pytest==8.4.2`, `httpx==0.28.1` | Aprobado por David. Son las últimas versiones que admiten Python 3.9; se fijan para que todo el equipo instale lo mismo. SQLAlchemy y PyMySQL se dejan para la Fase 3 |
| 4 | El entorno virtual (`.venv`) se crea en local y no se sube | El enunciado prohíbe subir `.venv`; el README explica cómo crearlo |
| 5 | Estructura `app/routers`, `app/schemas`, `app/data` | Separa endpoints, modelos y datos desde el inicio, para añadir `services/` y `repositories/` en la Sesión 4 sin reescribir |
| 6 | Datos de ejemplo en memoria con índices precalculados por id y por categoría | El enunciado permite datos en memoria en la Fase 1; los índices evitan recorrer listas en cada petición |
| 7 | Nombres de código en inglés; documentación y mensajes de error en español | Norma del enunciado; los mensajes los leerá el personal de sala |
| 8 | Categoría inexistente devuelve `404` con mensaje; id no numérico devuelve `422` | Norma del enunciado: toda entrada inválida recibe una respuesta controlada |
| 9 | La memoria del proyecto se guarda en `docs/memoria-proyecto.md` | Queda versionada junto al código |

### Cambios (2026-10-02)

- Creado el backend FastAPI con `GET /health`, `GET /categories`, `GET /tables`
  y `GET /categories/{category_id}/products`.
- Añadidos los modelos Pydantic `Category`, `Product` y `Table`.
- Añadidos datos de ejemplo: 5 categorías, 12 productos y 5 mesas.
- Añadidas 7 pruebas automáticas (`backend/tests/test_endpoints.py`).
- Añadidos `backend/requirements.txt` y `backend/pytest.ini`.
- Ampliado `.gitignore` con Python, `.venv`, `.env` y bases de datos locales.
- README: nueva introducción y sección del backend (instalación, ejecución, estructura,
  endpoints y datos de prueba). La parte de Angular se conserva.

### Verificación (2026-10-02, Python 3.9.23)

- `python -m pytest`: 7 de 7 pruebas pasan.
- Instalación limpia desde `requirements.txt` en un entorno nuevo: correcta, y las pruebas pasan.
- Servidor real con `uvicorn app.main:app`:
  - `/health` → 200 `{"status":"ok"}`
  - `/categories` → 200, 5 categorías
  - `/tables` → 200, 5 mesas
  - `/categories/2/products` → 200, 3 productos de Entrantes
  - `/categories/999/products` → 404 con mensaje
  - `/categories/abc/products` → 422
  - `/docs` → 200 y `/openapi.json` incluye los cuatro endpoints
- `/docs` (Swagger UI) comprobado por David en su PC el 2026-10-02: carga correctamente y
  muestra los cuatro endpoints agrupados en health, categories y tables, y los esquemas
  `Category`, `Product` y `Table`. En el entorno de pruebas de Claude no se pudo ver porque
  bloquea el CDN del que Swagger UI carga sus archivos.

## Fase 2: Navegación de carta y selección de pedido

### Requisitos (2026-10-09)

- Enunciado: completar la lectura de la carta en el orden del camarero (mesa, categoría,
  producto y presentación), con modelos de entrada y salida para que la API valide los JSON.
  Rutas mínimas: `GET /tables`, `GET /categories`, `GET /categories/{category_id}/products`,
  `GET /products/{product_id}/presentations` (solo presentaciones activas) y `GET /products/{id}`.
- Petición de David: para modificar, el camarero selecciona la mesa, ve el listado de sus
  pedidos y luego modifica (o no). Para crear, selecciona la mesa y añade o modifica el pedido.
  Trabajar en una rama nueva.

### Decisiones (2026-10-09)

| # | Decisión | Motivo |
|---|----------|--------|
| 1 | Rama `fase2`, creada desde `davidbranch` | David pidió una rama nueva para la Fase 2 |
| 2 | Los pedidos (listar, crear, consultar y modificar) se hacen ya en esta fase, en memoria | Lo pide el flujo de David. El enunciado deja la persistencia en MySQL para la Fase 3; entonces solo cambiará el almacén |
| 3 | Las rutas de pedidos cuelgan de la mesa: `/tables/{table_id}/orders` | Reproduce el flujo: primero se selecciona la mesa y todo lo demás ocurre dentro de ella |
| 4 | Modificar es `PATCH` con solo los campos que cambian (`presentation_id`, `quantity`) | El camarero suele cambiar una sola cosa. El producto y la mesa de un pedido no se cambian: si el producto es otro, es otro pedido |
| 5 | Sin borrado de pedidos todavía | No se pidió; el enunciado lo sitúa en la Fase 3 |
| 6 | JSON estricto: tipos exactos, campos desconocidos rechazados, cantidad de 1 a 99 | El enunciado pide que la API valide los JSON; el límite de 99 detecta errores de tecleo |
| 7 | `404` para lo que viene en la URL; `422` para lo que viene en el JSON | Distingue "esa mesa o pedido no existe" de "los datos enviados no son válidos" |
| 8 | Un pedido de otra mesa responde `404` | Evita modificar por error el pedido de otra mesa |
| 9 | Búsquedas comunes como dependencias de FastAPI (`routers/dependencies.py`) | Un único sitio para los 404, sin repetir código en cada endpoint |
| 10 | Almacén de pedidos en memoria con un candado (`data/order_store.py`) | FastAPI atiende peticiones en varios hilos; el candado evita ids repetidos |
| 11 | Presentaciones activas por producto en `PRODUCT_PRESENTATION_IDS` | Imita las columnas de disponibilidad de la tabla `Carta` |
| 12 | Tres pedidos de ejemplo al arrancar (Mesa 1 y Mesa 2) | Para que el listado de pedidos muestre algo nada más arrancar |

### Cambios (2026-10-09)

- Nuevos endpoints: `GET /tables/{table_id}`, `GET` y `POST /tables/{table_id}/orders`,
  `GET` y `PATCH /tables/{table_id}/orders/{order_id}`, `GET /products/{product_id}` y
  `GET /products/{product_id}/presentations`.
- Nuevos modelos: `Presentation`, `ProductDetail`, `Order`, `OrderCreate` y `OrderUpdate`.
- Datos de ejemplo: 4 presentaciones, presentaciones activas de cada producto y 3 pedidos.
- `GET /categories/{category_id}/products` usa ahora la dependencia común; su respuesta no cambia.
- Versión de la API: 0.2.0.
- Pruebas: de 7 a 41 (`test_tables.py`, `test_products.py`, `test_orders.py` y `conftest.py`,
  que reinicia los pedidos antes de cada prueba).
- README: estructura, endpoints, cuerpos JSON, errores y datos de prueba actualizados.

### Verificación (2026-10-09, Python 3.9.23)

- `python -m pytest -W error`: 41 de 41 pruebas pasan, sin avisos.
- Servidor real, recorrido del camarero: listar mesas, seleccionar la Mesa 1, ver sus 2 pedidos,
  ver categorías, productos de Entrantes, detalle y presentaciones de Croquetas, crear un pedido
  (201), verlo en el listado y modificar su cantidad (200). Errores comprobados: presentación no
  activa (422 con mensaje), cantidad como texto (422), pedido de otra mesa (404) y `PATCH` vacío (422).
