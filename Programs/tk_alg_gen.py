import tkinter as tk
from tkinter import font
from tkinter import filedialog
import pandas as pd
from algoritmo_genetico import variables_para_el_algoritmo,seleccionar_carrera,obtener_tres_mejores_tablas


def seleccionar_archivo():
    """
    Abre una ventana de selección de archivo para cargar un archivo CSV, y luego llama a la función 'abrir_ventana_carrera' 
    con el DataFrame cargado.

    Args:
    Ninguno.

    Returns:
    Ninguno.
    """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    if archivo:
        # El archivo es un archivo CSV
        dataframe = pd.read_csv(archivo)
        abrir_ventana_carrera(archivo=dataframe)



def abrir_ventana_carrera(archivo):
    """
    Abre una ventana secundaria para que el usuario seleccione una carrera de una lista de opciones y confirme su selección.

    Args:
    archivo (DataFrame de Pandas): El DataFrame cargado desde el archivo CSV.

    Returns:
    Ninguno.
    """

    # Crear una ventana secundaria
    ventana_carrera = tk.Toplevel(ventana_principal)
    ventana_carrera.title("Seleccionar Carrera")

    # Etiqueta
    etiqueta = tk.Label(ventana_carrera, text="Selecciona la carrera:")
    etiqueta.pack(pady=10)

    # Opciones de carrera como cadenas de texto
    opciones_carrera = ["IG", "IC", "IA", "ICC", "IMM", "ISCH", "IST", "ITP", "IF", "IM"]

    var_carrera = tk.StringVar()
    var_carrera.set(opciones_carrera[0])  # Valor predeterminado

    # Menú desplegable con las opciones de carrera
    menu_carrera = tk.OptionMenu(ventana_carrera, var_carrera, *opciones_carrera)
    menu_carrera.pack()

    # Botón para confirmar la selección de carrera
    boton_confirmar_carrera = tk.Button(ventana_carrera, text="Confirmar", 
                                        command=lambda: mostrar_menu_semestre(var_carrera.get(), archivo))
    boton_confirmar_carrera.pack(pady=20)


# Función para mostrar el menú de selección de semestre
def mostrar_menu_semestre(carrera,archivo):
    """
    Muestra una ventana secundaria para que el usuario seleccione un semestre dentro de la carrera previamente seleccionada.

    Args:
    carrera (str): La carrera seleccionada por el usuario.
    archivo (DataFrame de Pandas): El DataFrame cargado desde el archivo CSV.

    Returns:
    Ninguno.
    """
    ventana_semestre = tk.Toplevel(ventana_principal)
    ventana_semestre.title("Seleccionar Semestre")

    # Etiqueta
    etiqueta = tk.Label(ventana_semestre, text="Selecciona el semestre:")
    etiqueta.pack(pady=10)

    # Definir las opciones de semestre según la carrera seleccionada

    if carrera == "IG":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre","Noveno Semestre"]
    elif carrera == "IC":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre V1","Noveno Semestre V2"]
    elif carrera == "IST":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "IA":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "ICC":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "IMM":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "ISCH":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre Topicos", "Noveno Semestre Ciencias"]
    elif carrera == "ITP":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "IF":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]
    elif carrera == "IM":
        opciones_semestre = ["Primer Semestre", "Segundo Semestre", "Tercer Semestre", "Cuarto Semestre", "Quinto Semestre", "Sexto Semestre", 
                             "Séptimo Semestre", "Octavo Semestre", "Noveno Semestre"]

    var_semestre = tk.StringVar()
    var_semestre.set(opciones_semestre[0])  # Valor predeterminado

    # Menú desplegable con las opciones de semestre
    menu_semestre = tk.OptionMenu(ventana_semestre, var_semestre, *opciones_semestre)
    menu_semestre.pack()

    # Botón para confirmar la selección de semestre
    boton_confirmar = tk.Button(ventana_semestre, text="Confirmar", 
                                command=lambda: ejecutar_algoritmo(carrera, opciones_semestre.index(var_semestre.get()) + 1,archivo))
    boton_confirmar.pack(pady=20)



def ejecutar_algoritmo(carrera, numero_semestre, archivo):
    """
    Abre un archivo CSV, selecciona una carrera y un semestre, ejecuta el algoritmo genético en función de los datos del semestre seleccionado y muestra los resultados en una ventana.

    Args:
    carrera (str): La carrera seleccionada por el usuario.
    numero_semestre (int): El número del semestre seleccionado por el usuario.
    archivo (DataFrame de Pandas): El DataFrame cargado desde el archivo CSV.

    Returns:
    Ninguno.
    """

    # Seleccionar el semestre y obtener las variables necesarias para el algoritmo
    semestre = seleccionar_carrera(carrera, numero_semestre, archivo)
    tabla_vacia, claves, claves_disponibles, horas_por_clave = variables_para_el_algoritmo(semestre)

    # Ejecutar el algoritmo genético para obtener tres mejores tablas
    resultado = obtener_tres_mejores_tablas(50, tabla_vacia, claves, claves_disponibles, horas_por_clave)

    # Crear una ventana para mostrar el resultado
    ventana_resultado = tk.Toplevel(ventana_principal)
    ventana_resultado.title("Resultado del Algoritmo Genético")

    # Crear un Text widget para mostrar la tabla resultado
    texto_resultado = tk.Text(ventana_resultado)
    texto_resultado.pack()

    # Insertar valores en la tabla resultado
    tabla_resultado = resultado

    # Cambiar el tamaño del widget de texto
    texto_resultado.config(width=160, height=13)  # Ancho y Alto

    # Mostrar la tabla resultado en el Text widget
    texto_resultado.insert(tk.END, tabla_resultado.to_string(index=False))

    # Botón para volver a correr el programa
    boton_volver_a_correr = tk.Button(ventana_resultado, text="Volver a Correr",
                                      command=lambda: ejecutar_algoritmo(carrera, numero_semestre, archivo))
    boton_volver_a_correr.pack(pady=10)

    # Botón para seleccionar otro semestre
    boton_menu = tk.Button(ventana_resultado, text="Seleccionar otro semestre",
                           command=lambda: mostrar_menu_semestre(carrera, archivo))
    boton_menu.pack(pady=10)

    boton_cambiar_carrera = tk.Button(ventana_resultado, text="Cambiar de Carrera",
                                      command=lambda: abrir_ventana_carrera(archivo))
    boton_cambiar_carrera.pack(pady=10)

    boton_guardar_csv = tk.Button(ventana_resultado, text="Guardar en CSV",
                                  command=lambda: guardar_tabla_csv(tabla_resultado))
    boton_guardar_csv.pack(pady=10)

    # Botón para salir de la aplicación
    boton_salir = tk.Button(ventana_resultado, text="Salir", command=ventana_principal.destroy)
    boton_salir.pack(pady=10)

    
def guardar_tabla_csv(tabla):
    """
    Guarda una tabla en un archivo CSV y muestra un mensaje de confirmación.

    Args:
    tabla (DataFrame de Pandas): La tabla que se desea guardar en un archivo CSV.

    Returns:
    Ninguno.
    """

    # Solicitar al usuario la ubicación y el nombre del archivo CSV
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    if file_path:
        # Guardar la tabla en el archivo CSV
        tabla.to_csv(file_path, index=False)

        # Mostrar un mensaje de confirmación
        tk.messagebox.showinfo("Guardado", "La tabla se ha guardado exitosamente en:\n" + file_path)


# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Algoritmo Genético")

# Botón para abrir ventana de selección de archivo
boton_abrir = tk.Button(ventana_principal, text="Seleccionar Archivo CSV", command=seleccionar_archivo)
boton_abrir.pack(pady=20,side='top')

# Ejecutar la interfaz
ventana_principal.mainloop()