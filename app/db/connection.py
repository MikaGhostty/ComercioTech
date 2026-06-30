from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    try:
        client.admin.command("ping")
        print("Conectado a MongoDB")
    except Exception as e:
        print("Error de conexión:", e)
    return client["Comercio"]
