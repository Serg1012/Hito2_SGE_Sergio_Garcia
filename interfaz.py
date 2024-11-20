import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import openpyxl
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import os
from operaciones import listar_registros, obtener_conexion  # Importa las funciones necesarias


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Encuestas")
        self.geometry("1200x700")  # Aumenta el tamaño de la ventana para más espacio

        # Widgets básicos
        self.label_titulo = tk.Label(self, text="Gestión de Encuestas", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        # Frame para la tabla y las scrollbars
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Scrollbars
        scrollbar_vertical = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
        scrollbar_horizontal = tk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)

        # Tabla (Treeview)
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=(
                "ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
            ),
            show='headings',
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        # Configuración de las columnas
        columnas = [
            ("ID", 50), ("Edad", 70), ("Sexo", 100), ("BebidasSemana", 120),
            ("CervezasSemana", 120), ("BebidasFinSemana", 130),
            ("BebidasDestiladasSemana", 150), ("VinosSemana", 100),
            ("PerdidasControl", 120), ("DiversionDependenciaAlcohol", 200),
            ("ProblemasDigestivos", 150), ("TensionAlta", 120), ("DolorCabeza", 120)
        ]
        for columna, ancho in columnas:
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=ancho)

        # Posiciona la tabla y las scrollbars
        self.tabla.grid(row=0, column=0, sticky='nsew')
        scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

        # Configuración de las scrollbars
        scrollbar_vertical.config(command=self.tabla.yview)
        scrollbar_horizontal.config(command=self.tabla.xview)

        # Configuración del frame para expandir con la ventana
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        # Botones CRUD
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        self.btn_crear = tk.Button(frame_botones, text="Crear", command=self.crear_registro)
        self.btn_crear.pack(side=tk.LEFT, padx=10)

        self.btn_listar = tk.Button(frame_botones, text="Actualizar", command=self.cargar_tabla)
        self.btn_listar.pack(side=tk.LEFT, padx=10)

        self.btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=self.eliminar_registro)
        self.btn_eliminar.pack(side=tk.LEFT, padx=10)

        self.btn_grafico = tk.Button(frame_botones, text="Mostrar Gráfico", command=self.mostrar_grafico)
        self.btn_grafico.pack(side=tk.LEFT, padx=10)
        # Botón para exportar a Excel
        self.btn_exportar = tk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel)
        self.btn_exportar.pack(side=tk.LEFT, padx=10)

        # Filtros y ordenación
        self.filtro_frame = tk.Frame(self)
        self.filtro_frame.pack(pady=10)

        self.label_filtro = tk.Label(self.filtro_frame, text="Filtrar por:", anchor="w")
        self.label_filtro.pack(side=tk.LEFT, padx=5)

        self.filtro_combobox = ttk.Combobox(
            self.filtro_frame,
            values=["Bebidas Semana", "Pérdidas de Control", "Problemas Digestivos"]
        )
        self.filtro_combobox.pack(side=tk.LEFT, padx=5)

        self.valor_filtro = tk.Entry(self.filtro_frame)
        self.valor_filtro.pack(side=tk.LEFT, padx=5)

        self.btn_filtrar = tk.Button(self.filtro_frame, text="Aplicar Filtro", command=self.aplicar_filtro)
        self.btn_filtrar.pack(side=tk.LEFT, padx=5)

        # Combo para ordenar por campo
        self.label_ordenar = tk.Label(self.filtro_frame, text="Ordenar por:", anchor="w")
        self.label_ordenar.pack(side=tk.LEFT, padx=5)

        self.ordenar_combobox = ttk.Combobox(self.filtro_frame,
                                             values=["Edad", "Sexo", "BebidasSemana", "CervezasSemana"])
        self.ordenar_combobox.pack(side=tk.LEFT, padx=5)

        self.btn_ordenar = tk.Button(self.filtro_frame, text="Ordenar", command=self.ordenar_datos)
        self.btn_ordenar.pack(side=tk.LEFT, padx=5)

        # Carga inicial de datos
        self.cargar_tabla()

        self.grafico_frame = tk.Frame(self)
        self.grafico_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def cargar_tabla(self, filtro_sql=""):
        """
        Carga los datos desde la base de datos y los muestra en la tabla.
        Aplica el filtro y la ordenación si se pasa.
        """
        for item in self.tabla.get_children():
            self.tabla.delete(item)  # Eliminar los registros actuales de la tabla

        try:
            # Conexión a la base de datos
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Consulta base
                consulta = "SELECT * FROM ENCUESTA"

                # Si hay un filtro, agregar la cláusula WHERE
                if filtro_sql:
                    consulta += " WHERE " + filtro_sql

                # Si hay una ordenación, agregar la cláusula ORDER BY
                campo_orden = self.ordenar_combobox.get()
                if campo_orden:
                    consulta += f" ORDER BY {campo_orden}"

                # Ejecutar la consulta con el filtro y la ordenación si se pasan
                cursor.execute(consulta)

                # Insertar los registros obtenidos en la tabla
                registros = cursor.fetchall()
                if registros:  # Si hay registros
                    for registro in registros:
                        self.tabla.insert("", tk.END, values=registro)
                else:
                    print("No se encontraron registros.")

        except Exception as e:
            print(f"Error al cargar los registros: {e}")
        finally:
            conexion.close()

    def exportar_excel(self):
        """
        Exporta los datos mostrados en la tabla a un archivo Excel en una ruta predeterminada.
        """
        try:
            # Obtener los registros de la tabla
            registros = []
            for item in self.tabla.get_children():
                registros.append(self.tabla.item(item)["values"])

            # Crear un DataFrame con los registros
            df = pd.DataFrame(registros, columns=[
                "ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
            ])

            # Definir la ruta del archivo
            ruta_archivo = r"C:\Users\CampusFP\Desktop\Sergio\SDGE\HITO2\registros.xlsx"

            # Guardar el archivo en la ruta definida
            df.to_excel(ruta_archivo, index=False)
            print(f"Archivo Excel guardado en: {ruta_archivo}")

            # Abrir el archivo Excel
            os.startfile(ruta_archivo)  # En Windows esto abrirá el archivo Excel automáticamente.

        except Exception as e:
            print(f"Error al exportar a Excel: {e}")

    def mostrar_grafico(self):
        """
        Muestra un gráfico con los datos de la base de datos.
        Se puede seleccionar diferentes tipos de gráficos.
        """
        # Obtener los registros
        registros = listar_registros()

        # Analizar los datos para gráficos
        edades = []
        bebidas_semana = []

        for registro in registros:
            edades.append(registro[1])  # Edad
            bebidas_semana.append(registro[3])  # Bebidas por semana

        # Generar un gráfico de barras (Consumo promedio por grupo de edad)
        plt.figure(figsize=(10, 6))
        plt.bar(edades, bebidas_semana, color="skyblue")
        plt.title("Consumo Promedio de Bebidas por Edad")
        plt.xlabel("Edad")
        plt.ylabel("Bebidas por Semana")
        plt.xticks(rotation=45)

        # Mostrar el gráfico dentro de la interfaz de Tkinter
        self.dibujar_grafico()

    def dibujar_grafico(self):
        """
        Dibuja el gráfico en el frame de Tkinter usando Matplotlib.
        """
        # Crear el gráfico de Matplotlib
        fig = plt.gcf()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def aplicar_filtro(self):
        """
        Aplica un filtro condicional a los resultados.
        """
        filtro = self.filtro_combobox.get()
        valor = self.valor_filtro.get()

        if filtro == "Frecuencia Alcohol":
            filtro_sql = f"BebidasSemana >= {valor}"
        elif filtro == "Perdidas Control":
            filtro_sql = f"PerdidasControl > {valor}"
        elif filtro == "Problemas Salud":
            if valor.lower() in ["dolores de cabeza", "presión alta"]:
                filtro_sql = f"ProblemasDigestivos = '{valor}' OR TensionAlta = '{valor}'"
            else:
                filtro_sql = ""
        else:
            filtro_sql = ""

        self.cargar_tabla(filtro_sql)

    def crear_registro(self):
        """
        Ventana emergente para crear un nuevo registro.
        """
        ventana_crear = tk.Toplevel(self)
        ventana_crear.title("Crear Registro")
        ventana_crear.geometry("300x400")  # Tamaño más compacto

        # Frame para organizar los campos
        frame_formulario = tk.Frame(ventana_crear, padx=10, pady=10)
        frame_formulario.pack(fill=tk.BOTH, expand=True)

        # Campos para ingresar datos
        campos = [
            ("Edad", "int"), ("Sexo", "str"), ("Bebidas Semana", "int"),
            ("Cervezas Semana", "int"), ("Bebidas Fin Semana", "int"),
            ("Bebidas Destiladas Semana", "int"), ("Vinos Semana", "int"),
            ("Pérdidas de Control", "int"), ("Diversión/Dependencia Alcohol", "char"),
            ("Problemas Digestivos", "char"), ("Tensión Alta", "char"),
            ("Dolor de Cabeza", "char")
        ]

        entradas = {}
        for i, (campo, tipo) in enumerate(campos):
            # Etiqueta
            etiqueta = tk.Label(frame_formulario, text=f"{campo}:", anchor="w")
            etiqueta.grid(row=i, column=0, pady=5, sticky="w")
            # Campo de entrada
            entrada = tk.Entry(frame_formulario, width=20)
            entrada.grid(row=i, column=1, pady=5, sticky="e")
            entradas[campo] = entrada

        def guardar():
            """
            Guarda el registro ingresado en la base de datos.
            """
            datos = {campo: entradas[campo].get() for campo in entradas}
            # Validaciones básicas
            for campo, valor in datos.items():
                if not valor:
                    print(f"El campo {campo} es obligatorio.")
                    return

            try:
                conexion = obtener_conexion()
                with conexion.cursor() as cursor:
                    consulta = """
                    INSERT INTO ENCUESTA 
                    (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                    BebidasDestiladasSemana, VinosSemana, PerdidasControl, 
                    DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    valores = (
                        int(datos["Edad"]), datos["Sexo"], int(datos["Bebidas Semana"]),
                        int(datos["Cervezas Semana"]), int(datos["Bebidas Fin Semana"]),
                        int(datos["Bebidas Destiladas Semana"]), int(datos["Vinos Semana"]),
                        int(datos["Pérdidas de Control"]), datos["Diversión/Dependencia Alcohol"],
                        datos["Problemas Digestivos"], datos["Tensión Alta"], datos["Dolor de Cabeza"]
                    )
                    cursor.execute(consulta, valores)
                    conexion.commit()
                    print("Registro creado correctamente.")
                    self.cargar_tabla()  # Recargar la tabla con los nuevos datos
                    ventana_crear.destroy()  # Cerrar la ventana emergente
            except Exception as e:
                print("Error al crear el registro:", e)
            finally:
                conexion.close()

        # Botón Guardar
        boton_guardar = tk.Button(ventana_crear, text="Guardar", command=guardar)
        boton_guardar.pack(pady=10)

    def eliminar_registro(self):
        """
        Elimina el registro seleccionado de la base de datos.
        """
        # Obtener el item seleccionado en la tabla
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado:
            print("Por favor, selecciona un registro para eliminar.")
            return

        # Obtener el ID de la encuesta seleccionada
        id_encuesta = self.tabla.item(item_seleccionado)["values"][0]

        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                consulta = "DELETE FROM ENCUESTA WHERE idEncuesta = %s"
                cursor.execute(consulta, (id_encuesta,))
                conexion.commit()
                print(f"Registro con ID {id_encuesta} eliminado correctamente.")
                self.cargar_tabla()  # Recargar la tabla después de la eliminación
        except Exception as e:
            print(f"Error al eliminar el registro: {e}")
        finally:
            conexion.close()

    def aplicar_filtro(self):
        """
        Aplica un filtro condicional a los resultados basados en el campo seleccionado.
        """
        filtro = self.filtro_combobox.get()  # Obtiene el campo seleccionado para filtrar
        valor = self.valor_filtro.get()  # Obtiene el valor a filtrar

        # Generar la condición SQL según el filtro seleccionado
        filtro_sql = ""  # Inicializa vacío
        if filtro == "Bebidas Semana":
            try:
                valor = int(valor)  # Convertir a entero para validar
                filtro_sql = f"BebidasSemana >= {valor}"  # Condición SQL
            except ValueError:
                print("Por favor, ingrese un valor numérico válido para Bebidas Semana.")
                return
        elif filtro == "Pérdidas de Control":
            try:
                valor = int(valor)  # Validar que sea numérico
                filtro_sql = f"PerdidasControl >= {valor}"  # Condición SQL
            except ValueError:
                print("Por favor, ingrese un valor numérico válido para Pérdidas de Control.")
                return
        elif filtro == "Problemas Digestivos":
            filtro_sql = f"ProblemasDigestivos = '{valor}'"  # Filtrar texto exacto
        else:
            print("Filtro no válido.")
            return

        # Verificar que el filtro SQL no esté vacío antes de cargar
        if filtro_sql:
            self.cargar_tabla(filtro_sql)
        else:
            print("No se aplicó ningún filtro válido.")

    def ordenar_datos(self):
        """
        Ordena los resultados por el campo seleccionado.
        """
        campo = self.ordenar_combobox.get()  # Obtener el campo por el que se quiere ordenar
        if campo:  # Si hay un campo seleccionado
            # Pasar el campo de ordenación a la función de carga
            self.cargar_tabla(filtro_sql="")  # Limpiar el filtro
        else:
            print("No se ha seleccionado un campo para ordenar.")


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
