import hashlib
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.db import engine

router = APIRouter(tags=["usuarios"])

ITERACIONES = 600_000


def hashear_password(password: str) -> str:
    """Guarda sal + hash PBKDF2; la contraseña nunca queda en texto plano."""
    sal = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), sal, ITERACIONES
    )
    return f"pbkdf2_sha256${ITERACIONES}${sal.hex()}${hash_bytes.hex()}"


class UsuarioNuevo(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(default=None, pattern=r"^[0-9+ ()-]{6,30}$")
    password: str = Field(min_length=8, max_length=72)


@router.post("/usuarios", status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: UsuarioNuevo):
    consulta = text(
        "INSERT INTO usuario (nombre, email, telefono, password_hash, rol) "
        "VALUES (:nombre, :email, :telefono, :password_hash, 'cliente')"
    )
    try:
        with engine.begin() as conexion:
            resultado = conexion.execute(consulta, {
                "nombre": datos.nombre,
                "email": datos.email,
                "telefono": datos.telefono,
                "password_hash": hashear_password(datos.password),
            })
            nuevo_id = resultado.lastrowid
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo registrar el usuario")

    return {
        "ok": True,
        "id_usuario": nuevo_id,
        "nombre": datos.nombre,
        "email": datos.email,
        "telefono": datos.telefono,
        "rol": "cliente",
    }


@router.get("/usuarios/{id_usuario}")
def obtener_usuario(id_usuario: int):
    consulta = text(
        "SELECT id_usuario, nombre, email, telefono, rol, creado_en "
        "FROM usuario WHERE id_usuario = :id"
    )
    try:
        with engine.connect() as conexion:
            fila = conexion.execute(consulta, {"id": id_usuario}).mappings().first()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo consultar el usuario")

    if fila is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id_usuario": fila["id_usuario"],
        "nombre": fila["nombre"],
        "email": fila["email"],
        "telefono": fila["telefono"],
        "rol": fila["rol"],
        "creado_en": fila["creado_en"].isoformat(),
    }