# ComercioTech
App para Evaluacion de Base de Datos No Estructurados 

"ComercioTech"

ComercioTech es una aplicación CRUD desarrollada en **Python (PyQt6)** con conexión a **MongoDB**, diseñada para la gestión de clientes, pedidos y productos en un entorno de comercio electrónico.  

Características principales
- *Interfaz gráfica moderna* con PyQt6.  
- *Conexión segura* a MongoDB mediante `pymongo`.  
- *Funciones CRUD completas*:
  - **Create**: Inserción de nuevos documentos con campos dinámicos.  
  - **Read**: Visualización de colecciones completas o búsqueda puntual de un objeto mediante `find_one`.  
  - **Update**: Edición directa en tablas o actualización específica de un objeto.  
  - **Delete**: Eliminación de objetos con confirmación, campos individuales o en masa (con advertencias).
  -  
- *Validaciones y seguridad*:
  - Confirmaciones antes de eliminar.  
  - Restricción de operaciones críticas (ej. no se permite borrar colecciones completas).  
- *Documentación modular* del código (`app.py`, `crud.py`, `config.py`, `connection.py`).  

Estructura de la base de datos
- *clientes*: información personal y de contacto.  
- *productos*: catálogo con nombre, precio, stock y categoría.  
- *pedidos*: transacciones que enlazan clientes y productos.  


Objetivo
ComercioTech busca ser un prototipo funcional y escalable para la gestión de datos en un sistema de ventas, integrando buenas prácticas de modelado, conexión segura y documentación clara para proyectos académicos y profesionales.  

## Instalación y ejecución

Requisitos previos
- **Python 3.10+** (idealmente 3.11).  
- **MongoDB** instalado localmente o en la nube (ej. MongoDB Atlas).  
- Conexión configurada en `connection.py` para tu base de datos.  

Dependencias
Instala las librerías necesarias con:

--------------
pip install PyQt6 pymongo
--------------
Clonar el repositorio
--------------
git clone https://github.com/MikaGhostty/ComercioTech
cd ComercioTech
--------------

Configuración
1. Edita el archivo `connection.py` para apuntar a tu base de datos MongoDB.  
   Ejemplo para local:
--------------
   from pymongo import MongoClient
   def get_db():
       client = MongoClient("mongodb://localhost:27017/")
       return client["Comercio"]
--------------

2. Asegúrate de tener las colecciones `clientes`, `pedidos` y `productos` creadas en la base de datos.

Ejecución
Inicia la aplicación con:
--------------
python app.py
--------------
La interfaz gráfica se abrirá mostrando el menú principal de **ComercioTech**, desde donde podrás realizar operaciones CRUD sobre clientes, pedidos y productos.
