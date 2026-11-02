"""
Servidor base del proyecto.

En los primeros sprints el sitio puede publicarse como frontend estático.
Cuando se incorpore backend, FastAPI servirá los mismos archivos de /public
y se agregarán routers en /src/routes.

IMPORTANTE PARA CLASE:
StaticFiles se monta al final para no interceptar futuras rutas /api/*.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routes.contact import router as contact_router

app = FastAPI(
    title="Padel Almagro",
    version="0.1.0",
)

app.include_router(contact_router, prefix="/api")

# El frontend se monta ÚLTIMO.
app.mount("/", StaticFiles(directory="public", html=True), name="frontend")