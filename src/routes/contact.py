from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.db import engine

router = APIRouter(tags=["contacto"])


class Contacto(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=150)
    message: str = Field(min_length=10, max_length=1000)


@router.post("/contact", status_code=status.HTTP_201_CREATED)
def crear_contacto(contacto: Contacto):
    # Los campos del formulario (inglés) se guardan en las columnas de la tabla (español)
    consulta = text(
        "INSERT INTO contactos (nombre, email, asunto, mensaje) "
        "VALUES (:nombre, :email, :asunto, :mensaje)"
    )
    try:
        with engine.begin() as conexion:
            resultado = conexion.execute(consulta, {
                "nombre": contacto.name,
                "email": contacto.email,
                "asunto": contacto.subject,
                "mensaje": contacto.message,
            })
            nuevo_id = resultado.lastrowid
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo guardar la consulta")

    return {"ok": True, "id": nuevo_id, "mensaje": "Contacto recibido"}