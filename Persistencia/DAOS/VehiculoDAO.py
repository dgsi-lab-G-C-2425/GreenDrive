from Persistencia.AgenteBD import MongoDBAgent

class VehiculoDAO:
    COLLECTION = "vehiculos"
    global mongoDBAgent
    mongoDBAgent = MongoDBAgent()

    @staticmethod
    def insertar_dato(dato):
        return mongoDBAgent.insert_one(VehiculoDAO.COLLECTION, dato)

    @staticmethod
    def insertar_varios(datos):
        return mongoDBAgent.insert_many(VehiculoDAO.COLLECTION, datos)

    @staticmethod
    def obtener_dato(filtro):
        return mongoDBAgent.find_one(VehiculoDAO.COLLECTION, filtro)

    @staticmethod
    def obtener_todos():
        return mongoDBAgent.find(VehiculoDAO.COLLECTION)

    @staticmethod
    def actualizar_dato(filtro, nuevo_valor):
        # registrar petición y resultado
        result = mongoDBAgent.update_one(VehiculoDAO.COLLECTION, filtro, { "$set": nuevo_valor })
        print(f"[DAO] actualizar_dato filtro={filtro}, set={nuevo_valor}, matched={getattr(result, 'matched_count', None)}, modified={getattr(result, 'modified_count', None)}")
        return result

    @staticmethod
    def borrar_dato(filtro):
        return mongoDBAgent.delete_one(VehiculoDAO.COLLECTION, filtro)