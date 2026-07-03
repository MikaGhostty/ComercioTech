# ComercioTech
App para Evaluacion de Base de Datos No Estructurados 
Aquí tienes un resumen claro y atractivo para tu **README de GitHub** sobre la app **ComercioTech**:

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
