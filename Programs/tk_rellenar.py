import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from rellenar import crear_horario, llenar_lista_enlazada, contar_vacios_en_tablas, guardar_cambios, bloques
from rellenar import contar_vacios_en_bloques, comparar_y_transferir, grafica_no_vacios, grafica_vacios


def seleccionar_archivo():
    """
    Abre una ventana de selección de archivo y realiza operaciones en función del archivo seleccionado.

    Esta función abre una ventana de selección de archivo que permite al usuario elegir un archivo CSV. Una vez seleccionado el archivo, se realizan las siguientes operaciones:
    - Se llama a la función crear_horario() para crear un horario a partir del archivo CSV.
    - Se llama a la función llenar_lista_enlazada() para llenar una lista enlazada con el horario.
    - Se llama a la función actualizar_graficas() para actualizar las gráficas con el nuevo horario.

    Nota: Esta función asume que existen las funciones crear_horario(), llenar_lista_enlazada() y actualizar_graficas() definidas en otro lugar del código.
    """
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    if archivo:
        # Llamar a la función crear_horario() con el nombre del archivo
        horario, maestros, grupos, materias = crear_horario(archivo)
        
        # Llamar a la función llenar_lista_enlazada() con el horario
        ayuda = llenar_lista_enlazada(horario)
        
        # Llamar a la función actualizar_graficas() con la ayuda
        actualizar_graficas(ayuda)


def salir():
    """
    Cierra la ventana principal de la aplicación y finaliza el programa.

    Esta función se utiliza para cerrar la ventana principal de la aplicación GUI y finalizar el programa de manera ordenada.
    """
    root.destroy()

def guardar_cambios_csv(cam):
    """
    Abre una ventana de selección de archivo para guardar cambios en un archivo CSV.

    Esta función abre una ventana de selección de archivo para que el usuario pueda especificar la ubicación y el nombre del archivo CSV en el que se guardarán los cambios. Luego, llama a la función guardar_cambios() con la lista de cambios y la ubicación del archivo CSV.

    Args:
    - cam (list): Lista de cambios a guardar en el archivo CSV.
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        guardar_cambios(cam, file_path)


def mostrar_grafica_no_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio):
    """
    Muestra una gráfica de comparación de horas no vacías antes y después de un cambio.

    Esta función toma dos conjuntos de horarios, uno antes de un cambio y otro después del cambio, y crea una gráfica de barras para comparar las horas no vacías en ambos conjuntos. La gráfica muestra la cantidad de horas no vacías en diferentes categorías.

    Args:
    - horarios_antes_del_cambio (DataFrame): Conjunto de horarios antes del cambio.
    - horarios_despues_del_cambio (DataFrame): Conjunto de horarios después del cambio.
    """
    grafica_no_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio)


def mostrar_grafica_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio):
    """
    Muestra una gráfica de comparación de horas vacías antes y después de un cambio.

    Esta función toma dos conjuntos de horarios, uno antes de un cambio y otro después del cambio, y crea una gráfica de barras para comparar las horas vacías en ambos conjuntos. La gráfica muestra la cantidad de horas vacías en diferentes categorías.

    Args:
    - horarios_antes_del_cambio (DataFrame): Conjunto de horarios antes del cambio.
    - horarios_despues_del_cambio (DataFrame): Conjunto de horarios después del cambio.
    """
    grafica_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio)

def mostrar_grafica_bloques(bloques_antes, bloques_despues):
    """
    Muestra una gráfica de comparación de horas libres en bloques antes y después de un cambio.

    Esta función toma dos conjuntos de datos que representan las horas libres en bloques antes y después de un cambio, y crea una gráfica de barras horizontales para comparar la cantidad de horas libres en bloques en ambos conjuntos.

    Args:
    - bloques_antes (DataFrame): Conjunto de datos con horas libres en bloques antes del cambio.
    - bloques_despues (DataFrame): Conjunto de datos con horas libres en bloques después del cambio.
    """
    bloques(bloques_antes, bloques_despues)

def actualizar_graficas(ayuda):
    """
    Actualiza las gráficas en ventanas separadas después de realizar una comparación y transferencia de horarios.

    Esta función toma como entrada el resultado de la comparación y transferencia de horarios y crea una ventana separada para mostrar las gráficas antes y después del cambio, así como un botón para guardar los cambios en un archivo CSV.

    Args:
    - ayuda (list): Resultado de la comparación y transferencia de horarios.
    """
    # Contar horas vacías en tablas antes y después del cambio
    horarios_antes_del_cambio = contar_vacios_en_tablas(ayuda)
    bloques_antes = contar_vacios_en_bloques()
    cam,horarios_despues = comparar_y_transferir()
    horarios_despues_del_cambio = contar_vacios_en_tablas(horarios_despues)
    bloques_despues = contar_vacios_en_bloques()

    # Crear una nueva ventana para mostrar las gráficas
    ventana_graficas = tk.Toplevel(root)
    ventana_graficas.title("Resultados")

    # Botón para mostrar la gráfica de horas no vacías antes y después del cambio
    btn_grafica_no_vacios = tk.Button(ventana_graficas, text="Gráfica No Vacíos", 
                                      command=lambda: mostrar_grafica_no_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio))
    btn_grafica_no_vacios.pack()

    # Botón para mostrar la gráfica de horas vacías antes y después del cambio
    btn_grafica_vacios = tk.Button(ventana_graficas, text="Gráfica Vacíos", 
                                   command=lambda: mostrar_grafica_vacios(horarios_antes_del_cambio, horarios_despues_del_cambio))
    btn_grafica_vacios.pack()

    # Botón para mostrar la gráfica de bloques antes y después del cambio
    btn_grafica_bloques = tk.Button(ventana_graficas, text="Gráfica Bloques", 
                                    command=lambda: mostrar_grafica_bloques(bloques_antes, bloques_despues))
    btn_grafica_bloques.pack()

    # Botón para guardar los cambios en un archivo CSV
    btn_guardar_cambios = tk.Button(ventana_graficas, text="Guardar cambios", 
                                    command=lambda: guardar_cambios_csv(cam))
    btn_guardar_cambios.pack()


# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Horarios")

# Botón para abrir archivo CSV
btn_abrir = tk.Button(root, text="Abrir Archivo CSV", command=seleccionar_archivo)
btn_abrir.pack()
# Función para cerrar la aplicación


# Botón para salir
btn_salir = tk.Button(root, text="Salir", command=salir)
btn_salir.pack()

# Iniciar la interfaz de usuario
root.mainloop()