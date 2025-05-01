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
        # Usar pipeline de actualización para aplicar el $set
        return mongoDBAgent.update_one(VehiculoDAO.COLLECTION, filtro, [ { "$set": nuevo_valor } ])

    @staticmethod
    def borrar_dato(filtro):
        return mongoDBAgent.delete_one(VehiculoDAO.COLLECTION, filtro)