from datetime import date, datetime, time
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.db import engine

router = APIRouter(tags=["reservas"])


class ReservaNueva(BaseModel):
    id_usuario: int = Field(ge=1)
    id_cancha: int = Field(ge=1)
    fecha: date
    hora_inicio: time
    hora_fin: time


@router.post("/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(datos: ReservaNueva):
    if datos.hora_fin <= datos.hora_inicio:
        raise HTTPException(
            status_code=422, detail="hora_fin debe ser posterior a hora_inicio"
        )
    if datos.fecha < date.today():
        raise HTTPException(status_code=422, detail="La fecha no puede ser pasada")

    tipo_dia = "semana" if datos.fecha.weekday() < 5 else "finde"
    inicio = datetime.combine(datos.fecha, datos.hora_inicio)
    fin = datetime.combine(datos.fecha, datos.hora_fin)
    horas = Decimal((fin - inicio).total_seconds()) / Decimal(3600)

    try:
        with engine.begin() as conexion:
            # Bloquea la fila de la cancha: dos pedidos simultáneos no pueden
            # reservar el mismo horario.
            cancha = conexion.execute(
                text(
                    "SELECT id_cancha FROM cancha "
                    "WHERE id_cancha = :id AND activa = TRUE FOR UPDATE"
                ),
                {"id": datos.id_cancha},
            ).first()
            if cancha is None:
                raise HTTPException(status_code=404, detail="Cancha no encontrada o inactiva")

            usuario = conexion.execute(
                text("SELECT id_usuario FROM usuario WHERE id_usuario = :id"),
                {"id": datos.id_usuario},
            ).first()
            if usuario is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            tarifa = conexion.execute(
                text(
                    "SELECT id_tarifa, precio_hora FROM tarifa "
                    "WHERE tipo_dia = :tipo AND hora_desde <= :inicio "
                    "AND hora_hasta > :inicio LIMIT 1"
                ),
                {"tipo": tipo_dia, "inicio": datos.hora_inicio},
            ).mappings().first()
            if tarifa is None:
                raise HTTPException(
                    status_code=422, detail="Horario fuera del horario de atención"
                )

            ocupada = conexion.execute(
                text(
                    "SELECT 1 FROM reserva "
                    "WHERE id_cancha = :cancha AND fecha = :fecha "
                    "AND estado <> 'cancelada' "
                    "AND hora_inicio < :fin AND hora_fin > :inicio LIMIT 1"
                ),
                {
                    "cancha": datos.id_cancha,
                    "fecha": datos.fecha,
                    "inicio": datos.hora_inicio,
                    "fin": datos.hora_fin,
                },
            ).first()
            if ocupada is not None:
                raise HTTPException(
                    status_code=409, detail="La cancha ya está reservada en ese horario"
                )

            precio_total = (Decimal(tarifa["precio_hora"]) * horas).quantize(Decimal("0.01"))

            resultado = conexion.execute(
                text(
                    "INSERT INTO reserva (id_usuario, id_cancha, id_tarifa, fecha, "
                    "hora_inicio, hora_fin, estado, precio_total) "
                    "VALUES (:usuario, :cancha, :tarifa, :fecha, :inicio, :fin, "
                    "'pendiente', :precio)"
                ),
                {
                    "usuario": datos.id_usuario,
                    "cancha": datos.id_cancha,
                    "tarifa": tarifa["id_tarifa"],
                    "fecha": datos.fecha,
                    "inicio": datos.hora_inicio,
                    "fin": datos.hora_fin,
                    "precio": precio_total,
                },
            )
            nuevo_id = resultado.lastrowid
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo guardar la reserva")

    return {
        "ok": True,
        "id_reserva": nuevo_id,
        "id_cancha": datos.id_cancha,
        "fecha": datos.fecha.isoformat(),
        "hora_inicio": datos.hora_inicio.isoformat(),
        "hora_fin": datos.hora_fin.isoformat(),
        "estado": "pendiente",
        "precio_total": float(precio_total),
    }