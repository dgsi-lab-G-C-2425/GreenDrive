from Persistencia.AgenteBD import MongoDBAgent

class ReservasDAO:
    COLLECTION = "reservas"
    global mongoDBAgent
    mongoDBAgent = MongoDBAgent()

    @staticmethod
    def insertar_dato(dato):
        return mongoDBAgent.insert_one(ReservasDAO.COLLECTION, dato)

    @staticmethod
    def insertar_varios(datos):
        return mongoDBAgent.insert_many(ReservasDAO.COLLECTION, datos)

    @staticmethod
    def obtener_dato(filtro):
        return mongoDBAgent.find_one(ReservasDAO.COLLECTION, filtro)

    @staticmethod
    def obtener_todos():
        return mongoDBAgent.find(ReservasDAO.COLLECTION)

    @staticmethod
    def actualizar_dato(filtro, nuevo_valor):
        # registrar petición y resultado
        result = mongoDBAgent.update_one(ReservasDAO.COLLECTION, filtro, { "$set": nuevo_valor })
        print(f"[DAO] actualizar_dato filtro={filtro}, set={nuevo_valor}, matched={getattr(result, 'matched_count', None)}, modified={getattr(result, 'modified_count', None)}")
        return result

    @staticmethod
    def borrar_dato(filtro):
        return mongoDBAgent.delete_one(ReservasDAO.COLLECTION, filtro)