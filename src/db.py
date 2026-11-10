"""
Conexión a MySQL.

La dirección de la base se lee de la variable DATABASE_URL del archivo .env
(ese archivo no se sube a GitHub).
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Falta DATABASE_URL en el archivo .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)