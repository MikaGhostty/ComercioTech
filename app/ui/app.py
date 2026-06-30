from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QFormLayout,
    QDialog, QComboBox, QMessageBox
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import sys
from config import theme
from db import crud

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComercioTech")
        self.resize(900, 600)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(theme.BACKGROUND))
        self.setPalette(palette)

        self.layout_principal = QVBoxLayout()
        self.layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Menú ComercioTech")
        label.setStyleSheet(f"color: {theme.TEXT}; font-size: 20px; font-weight: bold;")
        self.layout_principal.addWidget(label)

        self.selector = QComboBox()
        self.selector.addItems(["clientes", "pedidos", "productos"])
        self.layout_principal.addWidget(self.selector)

        btn_create = QPushButton("Create")
        btn_create.setStyleSheet(self.button_style(theme.ACCENT, theme.TEXT))
        btn_create.clicked.connect(self.show_create)
        self.layout_principal.addWidget(btn_create)

        btn_read = QPushButton("Read")
        btn_read.setStyleSheet(self.button_style(theme.ACCENT, theme.TEXT))
        btn_read.clicked.connect(self.show_read)
        self.layout_principal.addWidget(btn_read)

        btn_update = QPushButton("Update")
        btn_update.setStyleSheet(self.button_style(theme.ACCENT, theme.TEXT))
        btn_update.clicked.connect(self.show_update)
        self.layout_principal.addWidget(btn_update)

        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet(self.button_style(theme.ACCENT, theme.TEXT))
        btn_delete.clicked.connect(self.show_delete)
        self.layout_principal.addWidget(btn_delete)

        self.setLayout(self.layout_principal)

    def button_style(self, bg, fg):
        return f"""
            background-color: {bg};
            color: {fg};
            font-size: {theme.FONT_SIZE}px;
            border: 2px solid {theme.BORDER};
            border-radius: 8px;
            padding: 6px;
        """

    def show_create(self):
        coleccion = self.selector.currentText()
        if coleccion == "clientes":
            datos = crud.listar_clientes()
        elif coleccion == "pedidos":
            datos = crud.listar_pedidos()
        else:
            datos = crud.listar_productos()

        campos_existentes = list(datos[0].keys()) if datos else []

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Crear en {coleccion}")
        form = QFormLayout()

        entradas = {}
        for campo in campos_existentes:
            entrada = QLineEdit()
            form.addRow(f"{campo}:", entrada)
            entradas[campo] = entrada

        btn_agregar = QPushButton("Agregar campo")
        def agregar_campo():
            nuevo_campo = QLineEdit()
            nombre_campo = f"campo_extra_{len(entradas)+1}"
            form.addRow(f"{nombre_campo}:", nuevo_campo)
            entradas[nombre_campo] = nuevo_campo
        btn_agregar.clicked.connect(agregar_campo)
        form.addRow(btn_agregar)

        btn_guardar = QPushButton("Guardar")
        def guardar():
            data = {campo: entrada.text() for campo, entrada in entradas.items()}
            if coleccion == "clientes":
                crud.add_cliente(data)
            elif coleccion == "pedidos":
                crud.add_pedido(data)
            else:
                crud.add_producto(data)
            QMessageBox.information(dialog, "Guardado", "El objeto fue creado correctamente.")
            dialog.close()
        btn_guardar.clicked.connect(guardar)
        form.addRow(btn_guardar)

        dialog.setLayout(form)
        dialog.exec()

    def show_read(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Leer datos")
        form = QFormLayout()

        selector_tabla = QComboBox()
        selector_tabla.addItems(["clientes", "pedidos", "productos"])
        form.addRow("¿Qué tabla usarás?", selector_tabla)

# Opcion 1: cargar tabla completa
        btn_tabla = QPushButton("Cargar tabla")
        def cargar_tabla():
            coleccion = selector_tabla.currentText()
            if coleccion == "clientes":
                datos = crud.listar_clientes()
            elif coleccion == "pedidos":
                datos = crud.listar_pedidos()
            else:
                datos = crud.listar_productos()

            if not datos:
                QMessageBox.warning(dialog, "Sin datos", "No hay datos en la colección seleccionada.")
                return

            columnas = list(datos[0].keys())
            tabla = QTableWidget(len(datos), len(columnas))
            tabla.setHorizontalHeaderLabels(columnas)

            for i, doc in enumerate(datos):
                for j, col in enumerate(columnas):
                    valor = doc.get(col, "")
                    tabla.setItem(i, j, QTableWidgetItem(str(valor)))

            form.addRow(tabla)

        btn_tabla.clicked.connect(cargar_tabla)
        form.addRow(btn_tabla)

# Opcion 2: cargar objeto específico
        btn_objeto = QPushButton("Cargar objeto")
        def cargar_objeto():
            coleccion = selector_tabla.currentText()
            campo_input = QLineEdit()
            valor_input = QLineEdit()
            form.addRow("Campo:", campo_input)
            form.addRow("Valor:", valor_input)

            btn_buscar = QPushButton("Buscar")
            def buscar():
                campo = campo_input.text().strip()
                valor = valor_input.text().strip()
                if not campo or not valor:
                    QMessageBox.warning(dialog, "Error", "Debes indicar campo y valor.")
                    return
                objeto = crud.buscar_objeto(coleccion, {campo: valor})
                if not objeto:
                    QMessageBox.warning(dialog, "No encontrado", "No existe un objeto con ese valor.")
                    return
                columnas = list(objeto.keys())
                tabla = QTableWidget(1, len(columnas))
                tabla.setHorizontalHeaderLabels(columnas)
                for j, col in enumerate(columnas):
                    tabla.setItem(0, j, QTableWidgetItem(str(objeto.get(col, ""))))
                form.addRow(tabla)

            btn_buscar.clicked.connect(buscar)
            form.addRow(btn_buscar)

        btn_objeto.clicked.connect(cargar_objeto)
        form.addRow(btn_objeto)

        dialog.setLayout(form)
        dialog.exec()



    def show_update(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Actualizar datos")
        form = QFormLayout()

        selector_tabla = QComboBox()
        selector_tabla.addItems(["clientes", "pedidos", "productos"])
        form.addRow("¿Qué tabla usarás?", selector_tabla)

# Opcion 1: cargar tabla completa
        btn_tabla = QPushButton("Cargar tabla")
        def cargar_tabla():
            coleccion = selector_tabla.currentText()
            if coleccion == "clientes":
                datos = crud.listar_clientes()
            elif coleccion == "pedidos":
                datos = crud.listar_pedidos()
            else:
                datos = crud.listar_productos()

            if not datos:
                QMessageBox.warning(dialog, "Sin datos", "No hay datos en la colección seleccionada.")
                return

            columnas = list(datos[0].keys())
            tabla = QTableWidget(len(datos), len(columnas))
            tabla.setHorizontalHeaderLabels(columnas)
            tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

            for i, doc in enumerate(datos):
                for j, col in enumerate(columnas):
                    tabla.setItem(i, j, QTableWidgetItem(str(doc.get(col, ""))))

            form.addRow(tabla)

            btn_actualizar = QPushButton("Guardar cambios")
            def actualizar():
                fila = tabla.currentRow()
                columna = tabla.currentColumn()
                if fila >= 0 and columna >= 0:
                    objeto = datos[fila]
                    id_doc = objeto["_id"]
                    campo = columnas[columna]
                    valor = tabla.item(fila, columna).text()
                    if coleccion == "clientes":
                        crud.actualizar_cliente(id_doc, {campo: valor})
                    elif coleccion == "pedidos":
                        crud.actualizar_pedido(id_doc, {campo: valor})
                    else:
                        crud.actualizar_producto(id_doc, {campo: valor})
                    QMessageBox.information(dialog, "Actualizado", f"Se actualizó el campo '{campo}' del objeto seleccionado.")
                else:
                    QMessageBox.warning(dialog, "Error", "Debes seleccionar una celda para actualizar.")
            btn_actualizar.clicked.connect(actualizar)
            form.addRow(btn_actualizar)

        btn_tabla.clicked.connect(cargar_tabla)
        form.addRow(btn_tabla)

# Opcion 2: cargar objeto específico
        btn_objeto = QPushButton("Cargar objeto")
        def cargar_objeto():
            coleccion = selector_tabla.currentText()
            campo_input = QLineEdit()
            valor_input = QLineEdit()
            form.addRow("Campo:", campo_input)
            form.addRow("Valor:", valor_input)

            btn_buscar = QPushButton("Buscar")
            def buscar():
                campo = campo_input.text().strip()
                valor = valor_input.text().strip()
                if not campo or not valor:
                    QMessageBox.warning(dialog, "Error", "Debes indicar campo y valor.")
                    return
                objeto = crud.buscar_objeto(coleccion, {campo: valor})
                if not objeto:
                    QMessageBox.warning(dialog, "No encontrado", "No existe un objeto con ese valor.")
                    return

                columnas = list(objeto.keys())
                tabla = QTableWidget(1, len(columnas))
                tabla.setHorizontalHeaderLabels(columnas)
                tabla.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

                for j, col in enumerate(columnas):
                    tabla.setItem(0, j, QTableWidgetItem(str(objeto.get(col, ""))))
                form.addRow(tabla)

                btn_actualizar = QPushButton("Guardar cambios")
                def actualizar():
                    columna = tabla.currentColumn()
                    if columna >= 0:
                        id_doc = objeto["_id"]
                        campo = columnas[columna]
                        valor = tabla.item(0, columna).text()
                        if coleccion == "clientes":
                            crud.actualizar_cliente(id_doc, {campo: valor})
                        elif coleccion == "pedidos":
                            crud.actualizar_pedido(id_doc, {campo: valor})
                        else:
                            crud.actualizar_producto(id_doc, {campo: valor})
                        QMessageBox.information(dialog, "Actualizado", f"Se actualizó el campo '{campo}' del objeto.")
                    else:
                        QMessageBox.warning(dialog, "Error", "Debes seleccionar una celda para actualizar.")
                btn_actualizar.clicked.connect(actualizar)
                form.addRow(btn_actualizar)

            btn_buscar.clicked.connect(buscar)
            form.addRow(btn_buscar)

        btn_objeto.clicked.connect(cargar_objeto)
        form.addRow(btn_objeto)

        dialog.setLayout(form)
        dialog.exec()


    def show_delete(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Eliminar datos")
        form = QFormLayout()

        selector_tabla = QComboBox()
        selector_tabla.addItems(["clientes", "pedidos", "productos"])
        form.addRow("¿Qué tabla usarás?", selector_tabla)

# Eliminar objeto
        btn_objeto = QPushButton("Eliminar objeto")
        def eliminar_objeto():
            coleccion = selector_tabla.currentText()
            if coleccion == "clientes":
                datos = crud.listar_clientes()
            elif coleccion == "pedidos":
                datos = crud.listar_pedidos()
            else:
                datos = crud.listar_productos()

            if not datos:
                QMessageBox.warning(dialog, "Sin datos", "No hay datos en la colección seleccionada.")
                return

            tabla = QTableWidget(len(datos), len(datos[0].keys()))
            tabla.setHorizontalHeaderLabels(list(datos[0].keys()))
            for i, doc in enumerate(datos):
                for j, col in enumerate(doc.keys()):
                    tabla.setItem(i, j, QTableWidgetItem(str(doc.get(col, ""))))
            form.addRow(tabla)

            btn_confirmar = QPushButton("Confirmar eliminación")
            def confirmar():
                fila = tabla.currentRow()
                if fila >= 0:
                    objeto = datos[fila]
                    nombre_objeto = objeto.get("nombre", str(objeto.get("_id")))
                    reply = QMessageBox.question(
                        dialog,
                        "Confirmar",
                        f"¿Estás seguro que quieres eliminar a: {nombre_objeto}?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        id_doc = objeto["_id"]
                        if coleccion == "clientes": crud.eliminar_cliente(id_doc)
                        elif coleccion == "pedidos": crud.eliminar_pedido(id_doc)
                        else: crud.eliminar_producto(id_doc)
                        tabla.removeRow(fila)
                        QMessageBox.information(dialog, "Eliminado", f"Se eliminó a: {nombre_objeto}")
            btn_confirmar.clicked.connect(confirmar)
            form.addRow(btn_confirmar)

        btn_objeto.clicked.connect(eliminar_objeto)
        form.addRow(btn_objeto)

# Eliminar campo individual
        btn_campo_individual = QPushButton("Eliminar campo de un objeto")
        def eliminar_campo_individual():
            coleccion = selector_tabla.currentText()
            if coleccion == "clientes":
                datos = crud.listar_clientes()
            elif coleccion == "pedidos":
                datos = crud.listar_pedidos()
            else:
                datos = crud.listar_productos()

            if not datos:
                QMessageBox.warning(dialog, "Sin datos", "No hay datos en la colección seleccionada.")
                return

            tabla = QTableWidget(len(datos), len(datos[0].keys()))
            columnas = list(datos[0].keys())
            tabla.setHorizontalHeaderLabels(columnas)
            for i, doc in enumerate(datos):
                for j, col in enumerate(columnas):
                    tabla.setItem(i, j, QTableWidgetItem(str(doc.get(col, ""))))
            form.addRow(tabla)

            campo_input = QLineEdit()
            form.addRow("Campo a eliminar:", campo_input)

            btn_confirmar = QPushButton("Eliminar campo")
            def confirmar():
                fila = tabla.currentRow()
                campo = campo_input.text().strip()
                if fila >= 0 and campo:
                    objeto = datos[fila]
                    id_doc = objeto["_id"]
                    if campo in objeto:
                        if coleccion == "clientes":
                            crud.actualizar_cliente(id_doc, {campo: None})
                        elif coleccion == "pedidos":
                            crud.actualizar_pedido(id_doc, {campo: None})
                        else:
                            crud.actualizar_producto(id_doc, {campo: None})
                        QMessageBox.information(dialog, "Campo eliminado", f"Se eliminó el campo '{campo}' del objeto seleccionado.")
                        dialog.close()
                    else:
                        QMessageBox.warning(dialog, "Error", f"El campo '{campo}' no existe en el objeto.")
            btn_confirmar.clicked.connect(confirmar)
            form.addRow(btn_confirmar)

        btn_campo_individual.clicked.connect(eliminar_campo_individual)
        form.addRow(btn_campo_individual)

# Eliminar campo en masa
        btn_campo_masa = QPushButton("Eliminar campo de todos los objetos")
        def eliminar_campo_masa():
            campo, ok = QMessageBox.getText(dialog, "Eliminar campo en masa", "Nombre del campo a eliminar:")
            if ok and campo:
                coleccion = selector_tabla.currentText()
                reply = QMessageBox.question(
                    dialog,
                    "Advertencia",
                    f"¿Seguro que quieres eliminar el campo '{campo}' de todos los objetos? Esta acción puede afectar la base de datos sin arreglo.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    if coleccion == "clientes":
                        crud.eliminar_campo_clientes(campo)
                    elif coleccion == "pedidos":
                        crud.eliminar_campo_pedidos(campo)
                    else:
                        crud.eliminar_campo_productos(campo)
                    QMessageBox.information(dialog, "Campo eliminado", f"Se eliminó el campo '{campo}' de todos los objetos.")
        btn_campo_masa.clicked.connect(eliminar_campo_masa)
        form.addRow(btn_campo_masa)

# Eliminar tabla completa
        btn_tabla = QPushButton("Eliminar tabla completa")
        def eliminar_tabla():
            QMessageBox.critical(dialog, "No autorizado", "No tienes autorización para eliminar tablas completas.")
        btn_tabla.clicked.connect(eliminar_tabla)
        form.addRow(btn_tabla)

        dialog.setLayout(form)
        dialog.exec()


def run_app():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
