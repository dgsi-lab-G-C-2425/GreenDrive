"""
Capa de servicio: valida datos de entrada y llama al DAO
(Adaptado a Pydantic v2)
"""
from datetime import datetime
from typing import Literal, List, Optional

from pydantic import BaseModel, Field, ValidationError, model_validator
from bson.objectid import ObjectId

from Persistencia.DAOS.ReservaDAO import ReservaDAO


# ---------- Esquemas de validación ----------
class Punto(BaseModel):
    lat: float
    lng: float
    direccion: str


class ReservaIn(BaseModel):
    usuario_id: str
    vehiculo_id: str
    fecha_inicio: datetime
    fecha_fin: datetime
    punto_recogida: Punto
    punto_devolucion: Punto

    @model_validator(mode="after")
    def check_dates(cls, model):
        if model.fecha_inicio >= model.fecha_fin:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return model


class ReservaUpdate(BaseModel):
    estado: Optional[Literal["pendiente", "activa", "finalizada", "cancelada"]] = None
    fecha_fin: Optional[datetime] = None


# ---------- Lógica de negocio ----------
class ReservaService:
    @staticmethod
    def crear(datos: dict) -> str:
        reserva = ReservaIn(**datos).model_dump()
        reserva["estado"] = "pendiente"
        reserva["usuario_id"] = ObjectId(reserva["usuario_id"])
        reserva["vehiculo_id"] = ObjectId(reserva["vehiculo_id"])
        return ReservaDAO.create(reserva)

    @staticmethod
    def obtener(reserva_id: str):
        return ReservaDAO.get_by_id(reserva_id)

    @staticmethod
    def listar_por_usuario(user_id: str):
        return ReservaDAO.get_by_user(user_id)

    @staticmethod
    def actualizar(reserva_id: str, datos: dict) -> int:
        validated = ReservaUpdate(**datos).model_dump(exclude_none=True)
        return ReservaDAO.update(reserva_id, validated)

    @staticmethod
    def borrar(reserva_id: str) -> int:
        return ReservaDAO.delete(reserva_id)
