from .connection import get_db

db = get_db()

# CRUD Clientes
def add_cliente(cliente): return db.clientes.insert_one(cliente)
def listar_clientes(): return list(db.clientes.find())
def actualizar_cliente(id, nuevos_datos): return db.clientes.update_one({"_id": id}, {"$set": nuevos_datos})
def eliminar_cliente(id): return db.clientes.delete_one({"_id": id})

# CRUD Pedidos
def add_pedido(pedido): return db.pedidos.insert_one(pedido)
def listar_pedidos(): return list(db.pedidos.find())
def actualizar_pedido(id, nuevos_datos): return db.pedidos.update_one({"_id": id}, {"$set": nuevos_datos})
def eliminar_pedido(id): return db.pedidos.delete_one({"_id": id})

# CRUD Productos
def add_producto(producto): return db.productos.insert_one(producto)
def listar_productos(): return list(db.productos.find())
def actualizar_producto(id, nuevos_datos): return db.productos.update_one({"_id": id}, {"$set": nuevos_datos})
def eliminar_producto(id): return db.productos.delete_one({"_id": id})

# Búsqueda puntual (find_one)
def buscar_objeto(coleccion, filtro):
    if coleccion == "clientes":
        return db.clientes.find_one(filtro)
    elif coleccion == "pedidos":
        return db.pedidos.find_one(filtro)
    else:
        return db.productos.find_one(filtro)
