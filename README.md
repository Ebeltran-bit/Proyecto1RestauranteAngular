# Proyecto Restaurante

API REST para que el personal de sala gestione los pedidos de las mesas de un restaurante,
y cliente web en Angular que la consumirá. El proyecto se entrega por fases; el registro de
decisiones y cambios está en [docs/memoria-proyecto.md](docs/memoria-proyecto.md).

| Carpeta    | Contenido                                   |
|------------|---------------------------------------------|
| `backend/` | API REST en Python con FastAPI              |
| `src/`     | Cliente web en Angular (fases posteriores)  |

## Backend (FastAPI)

### Requisitos

- Python 3.9 o superior.

### Instalación

Desde la carpeta `backend/`:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

La carpeta `.venv` no se sube al repositorio: cada persona crea la suya con los pasos anteriores.

### Ejecución

```bash
uvicorn app.main:app --reload
```

- Interfaz para el personal de sala: `http://127.0.0.1:8000/`
  (elegir mesa, ver sus pedidos, añadir y modificar).
- Documentación interactiva de la API: `http://127.0.0.1:8000/docs`, desde donde se pueden
  ejecutar todas las consultas.

### Pruebas

```bash
python -m pytest
```

### Estructura

```
backend/
  app/
    main.py            # crea la aplicación y registra los routers
    routers/           # endpoints agrupados por recurso
      dependencies.py  # búsquedas comunes que responden 404 si el recurso no existe
    schemas/           # modelos Pydantic de entrada y salida
    static/            # interfaz visual (HTML, CSS y JavaScript sin dependencias)
    data/
      sample_data.py   # carta, mesas y pedidos de ejemplo en memoria
      order_store.py   # almacén de pedidos en memoria (hasta la Fase 3)
  tests/               # pruebas automáticas de los endpoints
  requirements.txt
```

### Endpoints

El orden sigue el recorrido del camarero: elegir mesa, ver sus pedidos y añadir o modificar.

| Método | Ruta                                       | Descripción                                          |
|--------|--------------------------------------------|------------------------------------------------------|
| GET    | `/health`                                  | Confirma que la API funciona                         |
| GET    | `/tables`                                  | Lista las mesas del restaurante                      |
| GET    | `/tables/{table_id}`                       | Selecciona una mesa                                  |
| GET    | `/tables/{table_id}/orders`                | Lista los pedidos de la mesa                         |
| POST   | `/tables/{table_id}/orders`                | Añade un pedido a la mesa                            |
| GET    | `/tables/{table_id}/orders/{order_id}`     | Consulta un pedido de la mesa                        |
| PATCH  | `/tables/{table_id}/orders/{order_id}`     | Modifica la presentación o la cantidad de un pedido  |
| GET    | `/categories`                              | Lista las categorías de la carta                     |
| GET    | `/categories/{category_id}/products`       | Lista los productos de una categoría                 |
| GET    | `/products/{product_id}`                   | Detalle de un producto con su categoría y presentaciones |
| GET    | `/products/{product_id}/presentations`     | Solo las presentaciones activas del producto         |

Cuerpo JSON para crear un pedido (`POST`):

```json
{"product_id": 5, "presentation_id": 3, "quantity": 2}
```

Cuerpo JSON para modificarlo (`PATCH`), con uno o los dos campos:

```json
{"presentation_id": 4, "quantity": 3}
```

Respuestas de error controladas:

- `404`: la mesa, la categoría, el producto o el pedido de la URL no existen, o el pedido
  es de otra mesa. Ejemplo: `{"detail": "No existe la mesa con id 999"}`.
- `422`: el JSON no es válido (falta un campo, tipo incorrecto como `"2"` en vez de `2`,
  cantidad fuera de 1 a 99, campos desconocidos) o hace referencia a un producto o presentación
  que no existe o no está activa. Ejemplo: `{"detail": "Agua mineral no está disponible en Ración"}`.

### Datos de prueba

Los datos están en memoria, en `backend/app/data/sample_data.py`. Los pedidos que se crean o
modifican se pierden al reiniciar el servidor (la base de datos llega en la Fase 3).

- Categorías: 1 Bebidas, 2 Entrantes, 3 Carnes, 4 Pescados, 5 Postres.
- Mesas: 1 Mesa 1, 2 Mesa 2, 3 Mesa 3, 4 Terraza 1, 5 Barra.
- Presentaciones: 1 Unidad, 2 Tapa, 3 Media ración, 4 Ración.
- Productos: entre 2 y 3 por categoría, cada uno con sus presentaciones activas
  (por ejemplo, las bebidas solo se sirven por unidad).
- Pedidos iniciales: la Mesa 1 tiene 2 pedidos, la Mesa 2 tiene 1 y el resto ninguno.

## Frontend (Angular)

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.9.

### Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

### Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

### Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

### Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

### Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

### Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
