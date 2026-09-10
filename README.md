# Gestor de Proyectos UCC

Aplicación web desarrollada con Django para administrar proyectos y sus tareas asociadas. Permite crear, consultar, editar y eliminar proyectos, además de registrar tareas con prioridad y estado.

## Funcionalidades

- Listado de proyectos.
- Creación de proyectos con nombre, descripción y duración.
- Visualización del detalle de un proyecto.
- Edición y eliminación de proyectos.
- Creación de tareas asociadas a un proyecto.
- Clasificación de tareas por prioridad: baja, media o alta.
- Seguimiento del estado de las tareas: pendiente, en progreso o completada.
- Panel de administración de Django disponible en `/admin/`.

## Tecnologías

- Python
- Django 5.2.17
- SQLite
- Plantillas Django
- Tailwind CSS mediante CDN

## Requisitos

- Python 3.10 o superior recomendado.
- `pip`.
- macOS, Linux o Windows.

## Instalación

1. Clona el repositorio y entra en su carpeta:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd gestor_proyectos_ucc
   ```

2. Crea un entorno virtual:

   ```bash
   python3 -m venv .venv
   ```

3. Activa el entorno virtual:

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Aplica las migraciones:

   ```bash
   python manage.py migrate
   ```

## Ejecución

Inicia el servidor de desarrollo con:

```bash
python manage.py runserver
```

Abre [http://127.0.0.1:8000/proyectos/](http://127.0.0.1:8000/proyectos/) en el navegador.

## Rutas principales

| Ruta | Descripción |
| --- | --- |
| `/` | Página de bienvenida |
| `/acerca-de/` | Información básica de la aplicación |
| `/proyectos/` | Lista de proyectos |
| `/proyectos/nuevo/` | Crear un proyecto |
| `/proyectos/<id>/` | Ver el detalle de un proyecto |
| `/proyectos/<id>/editar/` | Editar un proyecto |
| `/proyectos/<id>/eliminar/` | Eliminar un proyecto |
| `/proyectos/<id>/tareas/nueva/` | Crear una tarea para un proyecto |
| `/admin/` | Administración de Django |

## Modelos

### Proyecto

- `nombre`: nombre del proyecto.
- `descripcion`: descripción del proyecto.
- `duracion`: duración registrada para el proyecto.

### Tarea

- `proyecto`: proyecto al que pertenece.
- `titulo`: título de la tarea.
- `descripcion`: descripción de la tarea.
- `prioridad`: `BAJA`, `MEDIA` o `ALTA`.
- `estado`: `PENDIENTE`, `EN_PROGRESO` o `COMPLETADA`.

Las tareas utilizan una relación de clave foránea con `Proyecto`. Al eliminar un proyecto, sus tareas también se eliminan.

## Pruebas

Ejecuta la suite de pruebas de Django con:

```bash
python manage.py test
```

## Estructura del proyecto

```text
.
├── manage.py              # Utilidad de administración de Django
├── db.sqlite3             # Base de datos local
├── requirements.txt       # Dependencias del proyecto
├── core/                  # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── gestor/                # Aplicación de gestión de proyectos
    ├── models.py          # Modelos Proyecto y Tarea
    ├── views.py           # Vistas de la aplicación
    ├── urls.py            # Rutas de la aplicación
    ├── admin.py           # Configuración del administrador
    ├── tests.py           # Pruebas
    ├── migrations/        # Migraciones de base de datos
    └── templates/         # Plantillas HTML
```

## Crear un usuario administrador

Para acceder al panel de administración, crea un superusuario:

```bash
python manage.py createsuperuser
```

Después visita [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Notas para producción

La configuración incluida está orientada al desarrollo. Antes de publicar la aplicación:

- Cambia `SECRET_KEY` y mantenla fuera del repositorio.
- Configura `DEBUG = False`.
- Define `ALLOWED_HOSTS` para los dominios válidos.
- Usa una base de datos y una configuración de archivos estáticos apropiadas para producción.
- Considera servir Tailwind CSS localmente en lugar de depender del CDN.
