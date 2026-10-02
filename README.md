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

La API queda en `http://127.0.0.1:8000` y la documentación interactiva en
`http://127.0.0.1:8000/docs`, desde donde se pueden ejecutar todas las consultas.

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
    schemas/           # modelos Pydantic de respuesta
    data/              # datos de ejemplo en memoria (Fase 1)
  tests/               # pruebas automáticas de los endpoints
  requirements.txt
```

### Endpoints (Fase 1)

| Método | Ruta                            | Descripción                                   |
|--------|---------------------------------|-----------------------------------------------|
| GET    | `/health`                       | Confirma que la API funciona                  |
| GET    | `/categories`                   | Lista las categorías de la carta              |
| GET    | `/tables`                       | Lista las mesas del restaurante               |
| GET    | `/categories/{id}/products`     | Lista los productos de una categoría          |

Errores controlados: una categoría inexistente devuelve `404` con un mensaje
(`{"detail": "No existe la categoría con id 999"}`) y un id no numérico devuelve `422`.

### Datos de prueba

En la Fase 1 los datos están en memoria, en `backend/app/data/sample_data.py`:

- Categorías: 1 Bebidas, 2 Entrantes, 3 Carnes, 4 Pescados, 5 Postres.
- Mesas: 1 Mesa 1, 2 Mesa 2, 3 Mesa 3, 4 Terraza 1, 5 Barra.
- Productos: entre 2 y 3 por categoría (por ejemplo, `GET /categories/2/products`
  devuelve Patatas bravas, Croquetas caseras y Ensaladilla rusa).

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
