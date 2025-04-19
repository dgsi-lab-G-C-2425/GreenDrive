"""
DAO para la colección 'reservas'
"""
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId
from Persistencia.AgenteBD import MongoDBAgent

_DB_NAME = "turismo_db"
_COLLECTION = "reservas"


class ReservaDAO:
    """Métodos CRUD sobre la colección reservas"""

    @staticmethod
    def _col():
        db = MongoDBAgent().get_db(_DB_NAME)
        return db[_COLLECTION]

    # ---------- CREATE ----------
    @classmethod
    def create(cls, data: dict) -> str:
        result = cls._col().insert_one(data)
        return str(result.inserted_id)

    # ---------- READ ----------
    @classmethod
    def get_by_id(cls, reserva_id: str) -> Optional[dict]:
        return cls._col().find_one({"_id": ObjectId(reserva_id)})

    @classmethod
    def get_by_user(cls, user_id: str) -> List[dict]:
        return list(cls._col().find({"usuario_id": ObjectId(user_id)}))

    # ---------- UPDATE ----------
    @classmethod
    def update(cls, reserva_id: str, data: dict) -> int:
        res = cls._col().update_one(
            {"_id": ObjectId(reserva_id)}, {"$set": data}
        )
        return res.modified_count

    # ---------- DELETE ----------
    @classmethod
    def delete(cls, reserva_id: str) -> int:
        res = cls._col().delete_one({"_id": ObjectId(reserva_id)})
        return res.deleted_count