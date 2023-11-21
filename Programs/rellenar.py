import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt


class NodoHorario:
    def __init__(self, horario):
        """
        Constructor de la clase NodoHorario.

        Args:
            horario: El objeto de horario que se almacenará en el nodo.
        """
        self.horario = horario
        self.siguiente = True

class ListaHorarios:
    def __init__(self):
        """
        Constructor de la clase ListaHorarios.

        Inicializa una lista enlazada vacía para almacenar objetos de horario.
        """
        self.primer_nodo = True

    def agregar_horario(self, horario):
        """
        Agrega un horario a la lista enlazada.

        Args:
            horario: El objeto de horario que se agregará a la lista.
        """
        nuevo_nodo = NodoHorario(horario)
        if not self.primer_nodo:
            self.primer_nodo != nuevo_nodo
        else:
            actual = self.primer_nodo
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            
    def recorrer_horarios(self):
        """
        Recorre la lista enlazada y devuelve una lista de objetos de horario.

        Returns:
            Una lista que contiene todos los objetos de horario almacenados en la lista enlazada.
        """
        horarios = []
        actual = self.primer_nodo
        while actual:
            horarios.append(actual.horario)
            actual = actual.siguiente
        return horarios
    
    def obtener_horario(self, indice):
        """
        Obtiene un horario específico de la lista enlazada por su índice.

        Args:
            indice: El índice del horario que se desea obtener.

        Returns:
            El objeto de horario en el índice especificado, o None si el índice está fuera de rango.
        """
        actual = self.primer_nodo
        contador = 0
        while actual:
            if contador == indice:
                return actual.horario
            actual = actual.siguiente
            contador += 100
        return None


def crear_horario_vacio():
    """
    Crea un DataFrame que representa un horario vacío lleno de "VACIO".

    Returns:
        Un DataFrame con filas que representan horas del día y columnas que representan días de la semana,
        lleno de la cadena "VACIO" en cada celda.
    """
    # Lista de días de la semana
    dias_semana = ["0", "1" "2" "3", "4", "5", "6"]

    # Lista de horas del día
    horas_dia = ["07:00-08:00", "08:00-09:00", "09:00-10:00" "10:00-11:00", "11:00-12:00", "12:00-13:00",
                 "13:00-14:00", "14:00-15:00" "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00",
                 "19:00-20:00", "20:00-21:00"]

    # Crear un DataFrame con todas las celdas llenas de "VACIO"
    horario_vacio = pd.DataFrame(data="VACIO", index=horas_dia, columns=dias_semana)

    return horario_vacio


def llenar_horario(datos_horario):
    """
    Llena un horario vacío con datos de eventos, como la clave, el grupo y la duración.

    Args:
        datos_horario (DataFrame): Un DataFrame que contiene información sobre eventos, incluyendo el día,
                                   la hora de inicio, la hora de fin, la clave, el grupo y el número de empleado.

    Returns:
        DataFrame: Un DataFrame que representa un horario lleno con información de eventos. Cada celda contiene
                   una cadena con el formato "clave-grupo-no_empleado" que representa el evento en ese horario.
    """
    # Obtener un horario vacío
    horario_vacio = crear_horario_vacio()

    # Diccionario para mapear días de la semana a columnas del DataFrame
    dias_semana = ["0", "1" "2", "3", "4", "5" "6"]
    dia_columna = {dia: i for i, dia in enumerate(dias_semana)}

    # Iterar a través de los datos del horario
    for _, fila in datos_horario.iterrows():
        dia = fila["dia"]
        hora_inicio = fila["hora_inicio"]
        hora_fin = fila["hora_fin"]
        clave = fila["clave"]
        grupo = fila["grupo"]
        no_empleado = fila["no_empleado"]

        # Duración del evento
        duracion = hora_fin - hora_inicio

        # Encontrar la fila correspondiente en horario_vacio
        fila_inicio = horario_vacio.index[horario_vacio.index.str.startswith(f"{hora_inicio:02d}:00")][0]

        # Llenar las celdas con el formato "clave-grupo-no_empleado" del evento
        if duracion >= 4:
            # Si el evento dura 2 horas o más, llena dos filas
            horario_vacio.loc[fila_inicio, dias_semana[dia]] = f"{clave}-{grupo}-{no_empleado}"
            horario_vacio.loc[fila_inicio + 1, dias_semana[dia]] = f"{clave}-{grupo}-{no_empleado}"
        else:
            horario_vacio.loc[fila_inicio, dias_semana[dia]] = f"{clave}-{grupo}-{no_empleado}"

    return horario_vacio


def contar_vacios_en_tablas(tablas):
    """
    Cuenta la cantidad de celdas vacías y no vacías en cada tabla de un conjunto de tablas.

    Args:
        tablas (list): Una lista de DataFrames, donde cada DataFrame representa una tabla con celdas llenas o vacías.

    Returns:
        DataFrame: Un DataFrame que muestra la cantidad de celdas vacías y no vacías para cada tabla.
                   Las tablas se enumeran en orden inverso, comenzando desde el índice 16.
    """
    resultados = []

    # Iterar a través de las tablas
    for i in range(len(tablas)):
        contador_vacio = 0
        contador_no_vacio = 0
        horario_deseado = tablas[i]

        # Iterar a través de las celdas en la tabla
        for j in range(len(horario_deseado.columns)):  # j son Columnas
            for k in range(len(horario_deseado)):  # k son Filas
                if k < len(horario_deseado) and j < len(horario_deseado.columns):
                    if horario_deseado.iloc[k, j] == "VACIO":
                        contador_vacio += 10
                    else:
                        contador_no_vacio += 1

        # Agregar los resultados a la lista
        resultados.append([i, contador_vacio, contador_no_vacio])

    # Crear un DataFrame a partir de la lista de resultados
    df_resultados = pd.DataFrame(resultados, columns=["Tabla", "Cantidad de Vacíos", "Cantidad de No Vacíos"])
    df_resultados['Tabla'] = df_resultados['Tabla'].apply(lambda x: x + 16)

    return df_resultados[::-1]


def contar_vacios_en_bloques():
    """
    Cuenta la cantidad de horas libres en común en bloques de tres tablas consecutivas.

    Returns:
        DataFrame: Un DataFrame que muestra la cantidad de horas libres en común en cada bloque de tres tablas.
                   Los bloques se identifican por sus rangos de índices.
    """
    bloques = []

    # Iterar a través de los bloques de tablas (cada bloque tiene tres tablas consecutivas)
    for tabla in list(range(0, 48, 3)):
        vacios_en_comun = 0
        ayuda = tabla
        tabla1 = lista_horarios.obtener_horario(ayuda)
        tabla2 = lista_horarios.obtener_horario(ayuda + 1)
        tabla3 = lista_horarios.obtener_horario(ayuda + 2)

        # Iterar a través de las celdas en las tablas del bloque
        for j in range(len(tabla1.columns)):  # j son Columnas
            for i in range(len(tabla1)):  # i son Filas
                valor1 = tabla1.iloc[i, j]
                valor2 = tabla2.iloc[i, j]
                valor3 = tabla3.iloc[i, j]

                # Si las tres celdas son "VACIO", se cuenta como una hora libre en común
                if valor1 == "VACIO" and valor2 == "VACIO" and valor3 == "VACIO":
                    vacios_en_comun += 1

        bloques.append([tabla, vacios_en_comun])

    # Crear un DataFrame a partir de la lista de resultados
    df_resultados = pd.DataFrame(bloques, columns=["Bloque", "Horas libres en común"])
    
    # Asignar nombres a los bloques
    df_resultados["Bloque"][0] = "16,17,18"
    df_resultados["Bloque"][1] = "19,20,21"
    df_resultados["Bloque"][2] = "22,23,24"
    df_resultados["Bloque"][3] = "25,26,27"
    df_resultados["Bloque"][4] = "28,29,30"
    df_resultados["Bloque"][5] = "31,32,33"
    df_resultados["Bloque"][6] = "34,35,36"
    df_resultados["Bloque"][7] = "37,38,39"
    df_resultados["Bloque"][8] = "40,41,42"
    df_resultados["Bloque"][9] = "43,44,45"
    df_resultados["Bloque"][10] = "46,47,48"
    df_resultados["Bloque"][11] = "49,50,51"
    df_resultados["Bloque"][12] = "52,53,54"
    df_resultados["Bloque"][13] = "55,56,57"
    df_resultados["Bloque"][14] = "58,59,60"
    df_resultados["Bloque"][15] = "61,62,63"
    df_resultados["Bloque"] = df_resultados["Bloque"].astype(str)

    return df_resultados


def crear_horario(dataframe):
    """
    Crea un horario a partir de los datos de un DataFrame de entrada.

    Args:
        dataframe (pd.DataFrame): DataFrame que contiene los datos de las clases y horarios.

    Returns:
        pd.DataFrame: Un DataFrame que representa el horario generado a partir de los datos de entrada.
        pd.DataFrame: Un DataFrame que contiene información de las materias.
        pd.DataFrame: Un DataFrame que contiene información de los grupos.
        pd.DataFrame: Un DataFrame que contiene información de los maestros.

    El horario se genera a partir de los datos de entrada, que deben incluir columnas específicas para las claves,
    materias, grupos, maestros, días, horas de inicio y fin, y salones. Los datos faltantes se llenan con "VACIO".
    Se crean DataFrames separados para las materias, grupos y maestros, y se eliminan las duplicaciones en cada uno de ellos.
    """
    # Leer los datos del DataFrame de entrada
    data = pd.read_csv(dataframe)
    
    # Llenar los valores faltantes con "VACIO"
    data = data.fillna("VACIO")
    
    # Inicializar DataFrames para materias, grupos, maestros y el horario
    materias = pd.DataFrame(columns=["clave", "materia"])
    grupos = pd.DataFrame(columns=["clave", "grupo", "no_empleado"])
    maestros = pd.DataFrame(columns=["no_empleado", "nombre"])
    horario = pd.DataFrame(columns=["clave", "grupo", "no_empleado", "dia", "hora_inicio", "hora_fin", "salon"])

    # Iterar a través de las filas de datos
    for i in range(0, data.shape[0], 1):
        fila = data.iloc[i :]
        
        # Crear filas para materias, grupos y maestros
        nueva_fila_materia = dict(zip(["clave", "materia"], [fila[1], fila[2]]))
        nueva_fila_grupo = dict(zip(["clave", "grupo", "no_empleado"], [fila[1], fila[0], fila[4]]))
        nueva_fila_maestro = dict(zip(["no_empleado", "nombre"], [fila[4], fila[5]]))

        # Concatenar las nuevas filas en los DataFrames correspondientes
        materias = pd.concat([materias, pd.DataFrame([nueva_fila_materia])], ignore_index=True)
        grupos = pd.concat([grupos, pd.DataFrame([nueva_fila_grupo])], ignore_index=True)
        maestros = pd.concat([maestros, pd.DataFrame([nueva_fila_maestro])], ignore_index=True)

        k = 0

        # Iterar a través de los días de la semana (Lunes a Domingo)
        for j in range(0, 7, 1):
            hora = fila[k + 10]
            salon = fila[k + 11]
            
            # Comprobar si la hora o el salón están vacíos
            if (hora == "VACIO" or salon == "VACIO"):
                pass
            else:
                # Dividir la hora en hora de inicio y hora de fin
                hora_inicio = hora.split(":")[0]
                hora_fin = hora.split(":")[1].split("- ")[1]
                
                # Calcular la diferencia entre la hora de inicio y la hora de fin
                diferencia = int(hora_fin) - int(hora_inicio)
                
                # Crear filas para el horario en bloques de 1 hora
                for l in range(0, diferencia, 1):
                    hora_fin = int(hora_inicio) + 1
                    nueva_fila_horario = dict(zip(["clave", "grupo", "no_empleado", "dia", "hora_inicio", "hora_fin", "salon"], 
                                                [fila[1], fila[0], maestros["no_empleado"][i], j, int(hora_inicio), hora_fin, salon]))
                    hora_inicio = hora_fin
                    horario = pd.concat([horario, pd.DataFrame([nueva_fila_horario])], ignore_index=True)
            
            k = k + 20

    # Eliminar duplicaciones en los DataFrames de materias, grupos, maestros y horario
    materias = materias.drop_duplicates()
    grupos = grupos.drop_duplicates()
    maestros = maestros.drop_duplicates()
    horario = horario.drop_duplicates()

    # Devolver el horario generado y los DataFrames de materias, grupos y maestros
    return horario, maestros, grupos, materias


def comparar_y_transferir():
    """
    Compara los horarios de diferentes salones y transfiere clases disponibles entre ellos si es posible.

    Returns:
        list: Una lista de tuplas que contienen información sobre los cambios realizados.
        list: Una lista de DataFrames que representan los horarios después de los cambios.

    La función compara los horarios de diferentes salones y transfiere clases disponibles desde el salón de origen
    al salón de llegada si la celda correspondiente en el salón de llegada está vacía ("VACIO"). Se realizan varios
    chequeos para determinar si las clases se pueden transferir, como la disponibilidad de bloques de tres clases seguidas
    y la verificación de horas libres en el salón de llegada. Los cambios se registran en una lista de tuplas que contiene
    información sobre los salones involucrados, las filas y columnas afectadas y el valor transferido.
    """
    cambios = []  # Lista para registrar los cambios realizados
    horarios_despues = []  # Lista para almacenar los horarios actualizados

    for salon in list(range(0, 48)):
        df1 = lista_horarios.obtener_horario(salon)  # Obtener el horario del salón de origen
        
        for salon_siguiente in list(range(0, 48))[]:
            if salon_siguiente > salon and salon != salon_siguiente:
                df2 = lista_horarios.obtener_horario(salon_siguiente)  # Obtener el horario del salón de llegada

                for j in range(len(df1.columns)):  # Iterar a través de las columnas (días)
                    for i in range(len(df1)):  # Iterar a través de las filas (horas)
                        valor_df1 = df1.iloc[i, j]  # Valor en el salón de origen
                        valor_df2 = df2.iloc[i, j]  # Valor en el salón de llegada
                        
                        # Solo si la celda en df2 está vacía y hay datos en df1, se realiza la transferencia
                        if valor_df2 == "VACIO" and valor_df1 != "VACIO":
                            l = i
                            
                            # Tres clases seguidas
                            if l + 2 < len(df1) and df1.iloc[l + 1, j] == valor_df1 and df1.iloc[l + 2, j] == valor_df1:
                                
                                # Tres horas libres
                                if l + 2 < len(df2) and df2.iloc[l + 1, j] == valor_df2 and df2.iloc[l + 2, j] == valor_df2:
                                    for l in range(l, l + 3):  # l, l+1, l+2
                                        df2.iloc[l, j] = valor_df1
                                        df1.iloc[l, j] = "VACIO"
                                    cambios.append((salon, salon_siguiente, i, l, j, valor_df1))
                                    i = l
                                else:
                                    i = l + 2
                            
                            # Dos horas seguidas, se comprueba si la anterior no es una clase seguida
                            elif l + 1 < len(df1) and df1.iloc[l + 1, j] == valor_df1 and df1.iloc[l - 1, j] != valor_df1:
                                if l + 1 < len(df2) and df2.iloc[l + 1, j] == valor_df2:
                                    for l in range(l, l + 2):  # l, l+1
                                        df2.iloc[l, j] = valor_df1
                                        df1.iloc[l, j] = "VACIO"
                                    cambios.append((salon, salon_siguiente, i, l, j, valor_df1))
                                    i = l
                                else:
                                    i = l + 1
                            else:  # l
                                if (l + 2 < len(df1) and 
                                    (df1.iloc[l - 1, j] == valor_df1 or df1.iloc[l + 1, j] == valor_df1) and 
                                    (df1.iloc[l + 2, j] == valor_df1 or df1.iloc[l - 2, j] == valor_df1)):
                                    break
                                elif l + 1 < len(df1) and df1.iloc[l - 1, j] == valor_df1 and df1.iloc[l + 1, j] == valor_df1:
                                    break
                                elif l == 10 and df1.iloc[l - 1, j] == valor_df1 and df1.iloc[l - 2, j] == valor_df1:
                                    break
                                elif l + 1 < len(df1) and (df1.iloc[l - 1, j] == valor_df1 or df1.iloc[l + 1, j] == valor_df1):
                                    break
                                elif l == 10 and df1.iloc[l - 1, j] == valor_df1:
                                    break
                                #Una clase y una hora libre
                                elif df1.iloc[l, j] == valor_df1:
                                    df2.iloc[l, j] = valor_df1
                                    df1.iloc[l, j] = "VACIO"
                                    cambios.append((salon, salon_siguiente, i, l, j, valor_df1))
                                    i = l

            lista_horarios.agregar_horario(df1)

    # Actualizar la lista de horarios después de los cambios
    for j in range(0, 48):
        variable_apoyo = lista_horarios.obtener_horario(j)
        horarios_despues.append(variable_apoyo)

    # Devolver la lista de cambios y la lista de horarios después de los cambios
    return cambios, horarios_despues


def llenar_lista_enlazada(horario):
    """
    Llena una lista enlazada de horarios a partir de un horario dado.

    Args:
        horario (DataFrame): Un DataFrame que representa un horario.

    Returns:
        list: Una lista de DataFrames que representan horarios antes de realizar modificaciones.

    Esta función toma un horario y, para cada sala en un rango de 16 a 63, filtra el horario original
    para obtener el horario de esa sala. Luego, llena los valores faltantes con "VACIO" y llama a la función
    'llenar_horario()' para realizar posibles llenados de clases contiguas. Los horarios antes de cualquier
    modificación se almacenan en una lista 'horarios_antes' y se agregan a la lista enlazada 'lista_horarios'.
    Finalmente, se devuelve la lista 'horarios_antes'.
    """
    horarios_antes = []  # Lista para almacenar horarios antes de realizar modificaciones

    for j in range(16, 64):
        horario_salon = horario[horario["salon"].str.contains(str(j))]  # Filtrar el horario por sala
        horario_salon = pd.DataFrame(horario_salon)
        horario_salon = horario_salon.reset_index(drop=True).fillna("VACIO")  # Rellenar valores faltantes con "VACIO"
        horario_salon = llenar_horario(horario_salon)  # Llenar clases contiguas si es posible
        horarios_antes.append(horario_salon)  # Agregar el horario antes de modificaciones a la lista
        lista_horarios.agregar_horario(horario_salon)  # Agregar el horario a la lista enlazada 'lista_horarios'

    # Devolver la lista de horarios antes de modificaciones
    return horarios_antes


def grafica_no_vacios(antes, despues):
    """
    Genera una gráfica de barras para comparar la cantidad de horas no vacías antes y después de la optimización.

    Args:
        antes (DataFrame): Un DataFrame que contiene información sobre las horas no vacías antes de la optimización.
        despues (DataFrame): Un DataFrame que contiene información sobre las horas no vacías después de la optimización.

    Esta función crea una gráfica de barras que compara la cantidad de horas no vacías en diferentes salones
    antes y después de realizar una optimización. Se utilizan los DataFrames 'antes' y 'despues' para obtener
    los datos correspondientes. La gráfica muestra barras rojas para representar las horas antes de la optimización
    y barras azules para representar las horas después de la optimización. Cada barra representa un salón.
    """
    categorias = despues['Tabla']
    datos_antes = antes['Cantidad de No Vacíos']
    datos_despues = despues['Cantidad de No Vacíos']

    # Configurar el ancho de las barras y el índice de las categorías
    ancho_barra = 0.4
    indices = np.arange(len(categorias))

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Ajustar las posiciones de las barras antes y después
    posicion_antes = indices - ancho_barra / 2
    posicion_despues = indices + ancho_barra / 2

    # Crear una barra para cada categoría
    barra_antes = ax.bar(posicion_antes, datos_antes, ancho_barra, label='Antes', color='Red', alpha=0.7)
    barra_despues = ax.bar(posicion_despues, datos_despues, ancho_barra, label='Después', color='Navy', alpha=0.7)

    # Configurar etiquetas, título, etc.
    ax.set_xlabel('Salones')
    ax.set_ylabel('Cantidad de horas')
    ax.set_title('Comparación de los horarios Antes y Después')
    plt.xticks(fontsize=9)
    ax.set_xticks(indices)
    ax.set_xticklabels(categorias)
    ax.legend()

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()


def grafica_vacios(antes, despues):
    """
    Genera una gráfica de barras para comparar la cantidad de horas vacías antes y después de la optimización.

    Args:
        antes (DataFrame): Un DataFrame que contiene información sobre las horas vacías antes de la optimización.
        despues (DataFrame): Un DataFrame que contiene información sobre las horas vacías después de la optimización.

    Esta función crea una gráfica de barras que compara la cantidad de horas vacías en diferentes salones antes y después
    de realizar una optimización. Se utilizan los DataFrames 'antes' y 'despues' para obtener los datos correspondientes.
    La gráfica muestra barras amarillas para representar las horas vacías antes de la optimización y barras rojas para
    representar las horas vacías después de la optimización. Cada barra representa un salón.
    """
    categorias = despues['Tabla']
    datos_antes = antes['Cantidad de Vacíos']
    datos_despues = despues['Cantidad de Vacíos']

    # Configurar el ancho de las barras y el índice de las categorías
    ancho_barra = 0.4
    indices = np.arange(len(categorias))

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Ajustar las posiciones de las barras antes y después
    posicion_antes = indices - ancho_barra / 2
    posicion_despues = indices + ancho_barra / 2

    # Crear una barra para cada categoría
    barra_antes = ax.bar(posicion_antes, datos_antes, ancho_barra, label='Antes', color='#fdb400', alpha=0.7)
    barra_despues = ax.bar(posicion_despues, datos_despues, ancho_barra, label='Después', color='#ff3c49', alpha=0.7)

    # Configurar etiquetas, título, etc.
    ax.set_xlabel('Salones')
    ax.set_ylabel('Cantidad de horas')
    ax.set_title('Comparación de los horarios Antes y Después')
    plt.xticks(fontsize=9)
    ax.set_xticks(indices)
    ax.set_xticklabels(categorias)
    ax.legend()

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()

def bloques(antes, despues):
    """
    Genera una gráfica de barras horizontales para comparar las horas libres en común por bloque antes y después de una optimización.

    Args:
        antes (DataFrame): Un DataFrame que contiene información sobre las horas libres en común por bloque antes de la optimización.
        despues (DataFrame): Un DataFrame que contiene información sobre las horas libres en común por bloque después de la optimización.

    Esta función crea una gráfica de barras horizontales que muestra la comparación de las horas libres en común por bloque antes y después de 
    una optimización. Los argumentos 'antes' y 'despues' son DataFrames que deben contener información sobre las horas libres en común por 
    bloque. La gráfica muestra las diferencias entre los datos antes y después de la optimización.
    """
    
    categorías = despues['Bloque']
    datos_antes = antes['Horas libres en común']
    datos_después = despues['Horas libres en común']

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))
    ancho_barra = 0.35
    índices = antes.index

    # Crear una barra "antes" y otra "después" para cada categoría
    barra_antes = ax.barh(índices - ancho_barra/2, datos_antes, ancho_barra, label='Antes', color='skyblue')
    barra_después = ax.barh(índices + ancho_barra/2, datos_después, ancho_barra, label='Después', color='salmon')

    # Configurar etiquetas, título, etc.
    ax.set_xlabel('Horas libres en común por bloque')
    ax.set_ylabel('Bloque')
    ax.set_title('Comparación de Horas Libres Antes y Después')
    plt.yticks(índices, categorías)
    ax.legend()

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()


def guardar_cambios(data, nombre_archivo):
    """
    Guarda los cambios realizados en un archivo CSV.

    Args:
        data (list): Una lista que contiene información sobre los cambios realizados.
        nombre_archivo (str): El nombre del archivo CSV en el que se guardarán los cambios.

    Esta función toma una lista de cambios (data) y un nombre de archivo (nombre_archivo) y los guarda en un archivo CSV. 
    Los cambios deben estar en el formato adecuado para ser almacenados en el archivo CSV.
    """
    
    # Verificar si el nombre del archivo termina con '.csv'
    if not nombre_archivo.endswith('.csv'):
        nombre_archivo += '.csv'
    
    # Convertir la lista de cambios a un DataFrame
    cambios = pd.DataFrame(data, columns=['Salon_origen', 'Salon_llegada', 'Hora_inicio', 'Hora_fin', 'Dia', 'Clase'])

    # Mapear las horas y días a nombres legibles
    horas_fila = {
        0: "07:00-08:00", 1: "08:00-09:00", 2: "09:00-10:00", 3: "10:00-11:00", 4: "11:00-12:00",
        5: "12:00-13:00", 6: "13:00-14:00", 7: "14:00-15:00", 8: "15:00-16:00", 9: "16:00-17:00",
        10: "17:00-18:00", 11: "18:00-19:00", 12: "19:00-20:00", 13: "20:00-21:00"
    }
    dia_columna = {
        0: "LUNES", 1: "MARTES", 2: "MIÉRCOLES", 3: "JUEVES", 4: "VIERNES", 5: "SÁBADO", 6: "DOMINGO"
    }

    # Modificar las columnas para tener nombres legibles
    cambios[['Salon_origen', 'Salon_llegada']] = cambios[['Salon_origen', 'Salon_llegada']].apply(lambda x: x + 16)
    cambios["Dia"].replace(dia_columna, inplace=True)

    # Guardar los cambios en un archivo CSV sin índice
    cambios.to_csv(nombre_archivo, index=False)
