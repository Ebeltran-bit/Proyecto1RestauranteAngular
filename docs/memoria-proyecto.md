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
