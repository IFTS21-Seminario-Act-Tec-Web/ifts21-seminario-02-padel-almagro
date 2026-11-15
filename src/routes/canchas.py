from datetime import date, time
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.db import engine

router = APIRouter(tags=["canchas"])


@router.get("/canchas")
def listar_canchas():
    consulta = text(
        "SELECT id_cancha, nombre, cubierta FROM cancha "
        "WHERE activa = TRUE ORDER BY id_cancha"
    )
    try:
        with engine.connect() as conexion:
            filas = conexion.execute(consulta).mappings().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudieron obtener las canchas")

    return [
        {"id_cancha": f["id_cancha"], "nombre": f["nombre"], "cubierta": bool(f["cubierta"])}
        for f in filas
    ]


@router.get("/canchas/disponibilidad")
def disponibilidad(
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    id_cancha: Optional[int] = Query(default=None, ge=1),
):
    if hora_fin <= hora_inicio:
        raise HTTPException(
            status_code=422, detail="hora_fin debe ser posterior a hora_inicio"
        )

    sql = (
        "SELECT c.id_cancha, c.nombre, c.cubierta, "
        "NOT EXISTS ("
        "  SELECT 1 FROM reserva r "
        "  WHERE r.id_cancha = c.id_cancha "
        "    AND r.fecha = :fecha "
        "    AND r.estado <> 'cancelada' "
        "    AND r.hora_inicio < :hora_fin "
        "    AND r.hora_fin > :hora_inicio"
        ") AS disponible "
        "FROM cancha c WHERE c.activa = TRUE"
    )
    parametros = {"fecha": fecha, "hora_inicio": hora_inicio, "hora_fin": hora_fin}

    if id_cancha is not None:
        sql += " AND c.id_cancha = :id_cancha"
        parametros["id_cancha"] = id_cancha
    sql += " ORDER BY c.id_cancha"

    try:
        with engine.connect() as conexion:
            filas = conexion.execute(text(sql), parametros).mappings().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudo consultar la disponibilidad")

    if id_cancha is not None and not filas:
        raise HTTPException(status_code=404, detail="Cancha no encontrada o inactiva")

    return {
        "fecha": fecha.isoformat(),
        "hora_inicio": hora_inicio.isoformat(),
        "hora_fin": hora_fin.isoformat(),
        "canchas": [
            {
                "id_cancha": f["id_cancha"],
                "nombre": f["nombre"],
                "cubierta": bool(f["cubierta"]),
                "disponible": bool(f["disponible"]),
            }
            for f in filas
        ],
    }