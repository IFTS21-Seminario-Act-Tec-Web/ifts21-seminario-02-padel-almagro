from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.db import engine

router = APIRouter(tags=["clases"])


@router.get("/profesores")
def listar_profesores():
    consulta = text(
        "SELECT id_profesor, nombre, apellido, certificacion "
        "FROM profesor ORDER BY apellido, nombre"
    )
    try:
        with engine.connect() as conexion:
            filas = conexion.execute(consulta).mappings().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudieron obtener los profesores")

    return [dict(f) for f in filas]


@router.get("/clases")
def listar_clases(nivel: Optional[str] = None, dia_semana: Optional[str] = None):
    sql = (
        "SELECT c.id_clase, c.tipo, c.nivel, c.dia_semana, c.hora_inicio, "
        "c.hora_fin, c.cupo, c.precio, "
        "p.id_profesor, p.nombre AS profesor_nombre, p.apellido AS profesor_apellido, "
        "ca.nombre AS cancha, "
        "c.cupo - (SELECT COUNT(*) FROM inscripcion_clase i "
        "          WHERE i.id_clase = c.id_clase AND i.estado = 'activa') "
        "AS cupos_disponibles "
        "FROM clase c "
        "JOIN profesor p ON p.id_profesor = c.id_profesor "
        "JOIN cancha ca ON ca.id_cancha = c.id_cancha "
        "WHERE 1 = 1"
    )
    parametros = {}
    if nivel:
        sql += " AND LOWER(c.nivel) = LOWER(:nivel)"
        parametros["nivel"] = nivel
    if dia_semana:
        sql += " AND LOWER(c.dia_semana) = LOWER(:dia)"
        parametros["dia"] = dia_semana
    sql += " ORDER BY c.id_clase"

    try:
        with engine.connect() as conexion:
            filas = conexion.execute(text(sql), parametros).mappings().all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="No se pudieron obtener las clases")

    return [
        {
            "id_clase": f["id_clase"],
            "tipo": f["tipo"],
            "nivel": f["nivel"],
            "dia_semana": f["dia_semana"],
            "hora_inicio": str(f["hora_inicio"]),
            "hora_fin": str(f["hora_fin"]),
            "cupo": f["cupo"],
            "cupos_disponibles": int(f["cupos_disponibles"]),
            "precio": float(f["precio"]),
            "profesor": {
                "id_profesor": f["id_profesor"],
                "nombre": f["profesor_nombre"],
                "apellido": f["profesor_apellido"],
            },
            "cancha": f["cancha"],
        }
        for f in filas
    ]