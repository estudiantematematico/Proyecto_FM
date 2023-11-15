import numpy as np
import pandas as pd
import random

def crear_tabla_vacia():
    """
    Crea una tabla vacía con encabezados de días de la semana y horas del día.

    La tabla vacía se representa como una lista de listas, donde cada lista interna representa una fila de la tabla. Los valores de las celdas se inicializan como "VACIO".

    Returns:
    - tabla_vacia (list): Una lista de listas que representa la tabla vacía.
    """
    # Lista de días de la semana
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # Lista de horas del día
    horas_dia = [
        "07:00-08:00", "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
        "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"]

    # Crear una lista de listas con todas las celdas llenas de "VACIO"
    tabla_vacia = [["VACIO" for _ in range(len(dias_semana))] for _ in range(len(horas_dia))]

    # Agregar los encabezados de días de la semana en la primera fila
    tabla_vacia.insert(0, [""] + dias_semana)

    # Agregar las horas en la primera columna
    for i in range(len(horas_dia)):
        tabla_vacia[i + 1].insert(0, horas_dia[i])

    return tabla_vacia


def etiquetar_cambios(tabla):
    """
    Etiqueta las celdas de una tabla según ciertas condiciones.

    Args:
    - tabla (list): Una lista de listas que representa la tabla.

    Returns:
    - tabla_modificada (list): Una nueva lista de listas que representa la tabla con celdas etiquetadas.
    """

    valores_repetidos = []  # Almacenar valores repetidos que ya se han etiquetado

    # Crear un DataFrame a partir de la tabla
    df = pd.DataFrame(tabla)

    # Recorrer cada columna del DataFrame (excepto la primera)
    for col in df.columns[1:]:
        celdas_columna = df[col]
        celdas_unicas = {}  # Diccionario para almacenar celdas únicas y sus ubicaciones

        # Recorrer las celdas de la columna
        for i, celda in enumerate(celdas_columna):
            if celda != "VACIO":
                if celda not in celdas_unicas:
                    celdas_unicas[celda] = [i]
                else:
                    celdas_unicas[celda].append(i)

        # Etiquetar como "EXCESO" si hay 3 o más repeticiones de una clave en la misma columna
        for celda, indices in celdas_unicas.items():
            if len(indices) >= 3:
                for i in indices:
                    df.at[i, col] = "EXCESO"

        # Etiquetar celdas con múltiples repeticiones como "CAMBIO"
        for celda, indices in celdas_unicas.items():
            if len(indices) > 1:
                # Verificar si la celda se repite en la fila siguiente
                repeticion_en_fila_siguiente = False
                for i in range(1, len(indices)):
                    fila_idx = indices[i]
                    fila_anterior_idx = indices[i - 1]
                    if df.at[fila_idx, col] == df.at[fila_anterior_idx + 1, col]:
                        repeticion_en_fila_siguiente = True
                        break

                # Mantener una y cambiar las demás a "CAMBIO" solo si no se repite en la fila siguiente
                if not repeticion_en_fila_siguiente:
                    for i in range(1, len(indices)):
                        fila_idx = indices[i]
                        fila_anterior_idx = indices[i - 1]
                        if celda not in valores_repetidos:
                            valores_repetidos.append(celda)
                        df.at[fila_idx, col] = "CAMBIO"

    # Convertir el DataFrame modificado de nuevo a una tabla (lista de listas)
    tabla_modificada = df.values.tolist()

    return tabla_modificada

def duplicados(df):
    """
    Identifica y maneja los duplicados en un DataFrame.

    Args:
    - df (pandas.DataFrame): El DataFrame en el que se buscan duplicados.

    Returns:
    - df_sin_duplicados (pandas.DataFrame): El DataFrame sin duplicados, si se encontraron duplicados.
    - df (pandas.DataFrame): El mismo DataFrame original, sin cambios, si no se encontraron duplicados.
    """
    duplicates = df[df.duplicated(keep=False)]

    # Si se encontraron duplicados
    if not duplicates.empty:
        # Eliminar duplicados y restablecer el índice del DataFrame
        df_sin_duplicados = df.drop_duplicates(keep="first").reset_index(drop=True)
        return df_sin_duplicados
    else:
        # Si no se encontraron duplicados, devolver el DataFrame original sin cambios
        return df
    
def calcular_aptitud(tabla):
    """
    Calcula la aptitud de una tabla considerando la cantidad de espacios llenos y vacíos, teniendo en cuenta las etiquetas "CAMBIO" y "EXCESO".

    Args:
    - tabla (list): Una lista de listas que representa la tabla a evaluar.

    Returns:
    - aptitud (int): El valor de aptitud calculado para la tabla.
    """
    # Inicializamos un contador de espacios llenos y espacios vacíos
    tabla = etiquetar_cambios(tabla)
    espacios_llenos = 0
    espacios_vacios = 0
    # Recorremos la tabla y contamos los espacios llenos y vacíos
    for fila in tabla:
        for celda in fila:
            if celda == "EXCESO" or celda == "CAMBIO":
                espacios_vacios += 1
            if celda != "VACIO":
                espacios_llenos += 1

    # Verificamos si todavía hay celdas con "CAMBIO" o "EXCESO"
    if espacios_vacios > 0:
        return 0  # Si hay celdas de "CAMBIO" o "EXCESO", aptitud igual a cero
    else:
        return espacios_llenos  # Si no hay celdas de "CAMBIO" ni "EXCESO", aptitud es el número de espacios llenos


def crear_tabla_aleatoria(tabla_vacia, claves, claves_disponibles, horas_por_clave):
    """
    Crea una tabla aleatoria a partir de una tabla vacía, claves disponibles y horas asignadas por clave.

    Args:
    - tabla_vacia (list): Una lista de listas que representa la tabla vacía.
    - claves (list): Una lista de todas las claves de las clases posibles.
    - claves_disponibles (list): Una lista de claves disponibles para insertar en la tabla.
    - horas_por_clave (dict): Un diccionario que mapea claves a la cantidad de horas asignadas.

    Returns:
    - tabla (list): Una tabla aleatoria creada a partir de la tabla vacía y las claves disponibles.
    """
    # Creamos una copia de la tabla vacía
    tabla = [fila[:] for fila in tabla_vacia]
    #Creamos un diccionario para llevar un registro de cuántas veces se ha insertado la clase
    clave_count = {clave: 0 for clave in claves}

    # Copiamos las claves disponibles para insertarlas en la tabla
    claves_disponibles_mezcladas = claves_disponibles.copy()
    # Insertamos las claves en la tabla de manera aleatoria con las horas correspondientes
    for fila in tabla:
        for i in range(len(fila)):
            if fila[i] == "VACIO" and claves_disponibles_mezcladas:
                # Seleccionamos una clave aleatoria de las disponibles
                nueva_clave = random.choice(claves_disponibles_mezcladas)
                #print("clave",nueva_clave)
                # Verificamos las horas asignadas para esa clave
                horas_asignadas = horas_por_clave.get(nueva_clave, 0)
                if clave_count[nueva_clave] < horas_asignadas:
                    fila[i] = nueva_clave
                    clave_count[nueva_clave] += 1
                    # Si se ha insertado la clave las veces necesarias, la eliminamos de las disponibles
                    if clave_count[nueva_clave] == horas_asignadas:
                        claves_disponibles_mezcladas.remove(nueva_clave)
    return tabla


def algoritmo_genetico(num_generaciones, tabla_vacia, claves, claves_disponibles, horas_por_clave):
    """
    Ejecuta un algoritmo genético para encontrar una tabla óptima respetando las restricciones.

    Args:
    - num_generaciones (int): El número de generaciones para ejecutar el algoritmo genético.
    - tabla_vacia (list): Una lista de listas que representa la tabla vacía.
    - claves (list): Una lista de todas las claves de las clases posibles.
    - claves_disponibles (list): Una lista de claves disponibles para insertar en la tabla.
    - horas_por_clave (dict): Un diccionario que mapea claves a la cantidad de horas asignadas.

    Returns:
    - mejor_tabla (DataFrame): La mejor tabla encontrada por el algoritmo genético.
    """
    mejor_tabla = []
    mejor_aptitud = -1

    for _ in range(num_generaciones):
        # Generamos una población de tablas aleatorias
        poblacion = [crear_tabla_aleatoria(tabla_vacia,claves,claves_disponibles,horas_por_clave) for _ in range(3000)]

        # Evaluamos la aptitud de cada tabla
        aptitudes = [calcular_aptitud(tabla) for tabla in poblacion]

        # Encontramos la mejor tabla de la generación
        indice_mejor = aptitudes.index(max(aptitudes))
        mejor_tabla_generacion = poblacion[indice_mejor]
        aptitud_mejor_generacion = aptitudes[indice_mejor]
        #print(aptitudes)
        # Si la mejor tabla de esta generación es mejor que la mejor tabla global, la actualizamos
        if aptitud_mejor_generacion > mejor_aptitud:
            mejor_tabla = mejor_tabla_generacion
            mejor_aptitud = aptitud_mejor_generacion
            #print(mejor_aptitud)
        
        mejor_tabla=pd.DataFrame(mejor_tabla)
        #Tomar la primera fila como nombres de columnas
        mejor_tabla.columns = mejor_tabla.iloc[0]
        #Eliminar la primera fila del DataFrame
        mejor_tabla = mejor_tabla[1:]
        #Restablecer los índices del DataFrame
        mejor_tabla.reset_index(drop=True, inplace=True)
        return mejor_tabla


def crear_horario(horarios):
    """
    Carga un archivo CSV de horarios, filtra y procesa los datos y retorna un DataFrame de Pandas.

    Args:
    - horarios (str): La ruta del archivo CSV que contiene los horarios.

    Returns:
    - dataframe (DataFrame de Pandas): Un DataFrame que contiene los datos procesados de los horarios.
    """
    dataframe = pd.read_csv(horarios, index_col=None)
    
    # Crear una lista vacía para almacenar los nombres que cumplan con el criterio
    claves_a_eliminar = []

    # Iterar a través de la columna 'Nombre' y agregar los nombres que comienzan con 'M' a la lista
    for nombre in dataframe['clave']:
        if nombre.startswith('M'):
            claves_a_eliminar.append(nombre)
    
    # Encuentra los índices de las filas con los grupos que quieres eliminar
    indices_a_eliminar = dataframe[dataframe['clave'].isin(claves_a_eliminar)].index
    
    # Eliminar las filas con los grupos que cumplen con el criterio
    dataframe = dataframe.drop(indices_a_eliminar)
    
    # Eliminar la columna 'materia'
    dataframe = dataframe.drop(['materia'], axis=1)
    
    return dataframe

#Selcciona una Carrera 
def seleccionar_carrera(carrera,x,dataframe):
    if carrera == "IG":
        return seleccionar_semestre_geologia(x,dataframe)
    elif carrera == "IC":
        return seleccionar_semestre_civil(x,dataframe)
    elif carrera == "IA":
        return seleccionar_semestre_aero(x,dataframe)
    elif carrera == "ICC":
        return seleccionar_semestre_cien_comp(x,dataframe)
    elif carrera == "IMM":
        return seleccionar_semestre_minas(x,dataframe)
    elif carrera =="ISCH":
        return seleccionar_semestre_hard(x,dataframe)
    elif carrera == "IST":
        return seleccionar_semestre_topo(x,dataframe)
    elif carrera == "ITP":
        return seleccionar_semestre_procesos(x,dataframe)
    elif carrera ==  "IF":
        return seleccionar_semestre_fisica(x,dataframe)
    elif carrera == "IM":
        return seleccionar_semestre_mate(x,dataframe)

#De la carrera seleccionada
#Como argumentos son el número de semestre y el dataframe
#En cada semestre busca las claves que le corresponden
#Retorna el semestre con las claves sin repetir
def seleccionar_semestre_geologia(x,dataframe):
    if x==1:
        geologia_1 = dataframe.loc[dataframe['clave'].isin(
            ['101','102','103','106','107','108','115','216','I101'])].reset_index(drop=True)
        return duplicados(geologia_1)
    elif x==2:
        geologia_2 = dataframe.loc[dataframe['clave'].isin(
            ['100','104','200','201','202','203','210','211','316','I201'])].reset_index(drop=True)
        return duplicados(geologia_2)
    elif x==3:
        geologia_3 = dataframe.loc[dataframe['clave'].isin(
            ['209','301','302','303','407','451','454','501','I301'])].reset_index(drop=True)
        return duplicados(geologia_3)
    elif x==4:
        geologia_4 = dataframe.loc[dataframe['clave'].isin(
            ['206','403','457','470','471','472','503','772','I401'])].reset_index(drop=True)
        return duplicados(geologia_4)
    elif x==5:
        geologia_5 = dataframe.loc[dataframe['clave'].isin(
            ['416','557','558','571','573','601','634','670','970'])].reset_index(drop=True)
        return duplicados(geologia_5)
    elif x==6:
        geologia_6 = dataframe.loc[dataframe['clave'].isin(
            ['552','676','771','775','872','873','874'])].reset_index(drop=True)
        return duplicados(geologia_6)
    elif x==7:
        geologia_7 = dataframe.loc[dataframe['clave'].isin(
            ['71','716','770','801','870','877','974','981'])].reset_index(drop=True)
        return duplicados(geologia_7)
    elif x==8:
        geologia_8 = dataframe.loc[dataframe['clave'].isin(
            ['510','773','815','856','876','956','971','976'])].reset_index(drop=True)
        return duplicados(geologia_8)
    elif x==9:
        geologia_9 = dataframe.loc[dataframe['clave'].isin(
            ['74','79','80','930','969','966','973','964','965','928','977',
             '982','929','950'])].reset_index(drop=True)
        return duplicados(geologia_9)

def seleccionar_semestre_civil(x, dataframe):
    if x==1:
        civil_1 = dataframe.loc[dataframe['clave'].isin(
            ['CB101','CB102','CB103','I101','IB107','IB108','OC109','UN115','UN216'])].reset_index(drop=True)
        return duplicados(civil_1)
    elif x==2:
        civil_2 = dataframe.loc[dataframe['clave'].isin(
            ['CB201','CB202','CB203','I201','IB210','IB211','OC209','UN200','UN316'])].reset_index(drop=True)
        return duplicados(civil_2)
    elif x==3:
        civil_3 = dataframe.loc[dataframe['clave'].isin(
            ['CB217','CB301','CB303','CB305','CB503','I301','LCB217','OC309','OC407'])].reset_index(drop=True)
        return duplicados(civil_3)
    elif x==4:
        civil_4 = dataframe.loc[dataframe['clave'].isin(
            ['CB402','CB403','CB406','CB410','CB601','CB801','I401','IA703','IB602'])].reset_index(drop=True)
        return duplicados(civil_4)
    elif x==5:
        civil_5 = dataframe.loc[dataframe['clave'].isin(
            ['IA610','IA800','IB502','IB504','IB506','IB704','IB910','IN501','OC509'])].reset_index(drop=True)
        return duplicados(civil_5)
    elif x==6:
        civil_6 = dataframe.loc[dataframe['clave'].isin(
            ['I601','IA505','IA611','IB604','IB605','IB606','IB804','IB806','IB911'])].reset_index(drop=True)
        return duplicados(civil_6)
    elif x==7:
        civil_7 = dataframe.loc[dataframe['clave'].isin(
            ['IA603','IA711','IA712','IB706','IB708','IB803','IB805','IB912','IN701'])].reset_index(drop=True)
        return duplicados(civil_7)
    elif x==8:
        civil_8 = dataframe.loc[dataframe['clave'].isin(
            ['IA612','IA613','IA705','IA706','IA808','IA809','IA811','IA906','IA921'])].reset_index(drop=True)
        return duplicados(civil_8)
    elif x==9:
        civil_9 = dataframe.loc[dataframe['clave'].isin(
            ['OC510','VT04','CU06','CU01','CU02','CU03','HH02','EST05','CU05','VT01',
             'VT03','CU04','EST06'])].reset_index(drop=True)
        return duplicados(civil_9)
    elif x==10:
        civil_10 = dataframe.loc[dataframe['clave'].isin(
            ['OC510','VT02','EST04','EST02','EST01','EST03','HH04','HH08','HH06','HH03',
             'HH05','EST06'])].reset_index(drop=True)
        return duplicados(civil_10)

def seleccionar_semestre_aero(x, dataframe):
    if x==1:
        aero_1 = dataframe.loc[dataframe['clave'].isin(
            ['CB101','CB102','CB103','CI112','I301','LCB103','UN115','UN216'])].reset_index(drop=True)
        return duplicados(aero_1)
    elif x==2:
        aero_2 = dataframe.loc[dataframe['clave'].isin(
            ['CB201','CB203','CB217','CS312','I401','LCB217','UN200','UN316'])].reset_index(drop=True)
        return duplicados(aero_2)
    elif x==3:
        aero_3 = dataframe.loc[dataframe['clave'].isin(
            ['CB301','CB302','CB303','CI209','IN501','LCB302','LCB303','OC206',
             'OC407'])].reset_index(drop=True)
        return duplicados(aero_3)
    elif x==4:
        aero_4 = dataframe.loc[dataframe['clave'].isin(
            ['CB401','CB406','CI405','CI408','CI409','CI417','IN601','LCB406',
             'LCI408','LCI417'])].reset_index(drop=True)
        return duplicados(aero_4)
    elif x==5:
        aero_5 = dataframe.loc[dataframe['clave'].isin(
            ['CI509','CI512','CI531','CI550','CI580','IN701','LCI550','LCI580'])].reset_index(drop=True)
        return duplicados(aero_5)
    elif x==6:
        aero_6 = dataframe.loc[dataframe['clave'].isin(
            ['CI660','CI662','CI664','LCI660','OPAE3','OPAE1','OPAE2'])].reset_index(drop=True)
        return duplicados(aero_6)
    elif x==7:
        aero_7 = dataframe.loc[dataframe['clave'].isin(
            ['IA339','IA362','IA363','OC110','CI407','IA948','IA780'])].reset_index(drop=True)
        return duplicados(aero_7)
    elif x==8:
        aero_8 = dataframe.loc[dataframe['clave'].isin(
            ['IA364','IA419','IA424','IA439','OC112','IA790','IA862','CI764','CI581'])].reset_index(drop=True)
        return duplicados(aero_8)
    elif x==9:
        aero_9 = dataframe.loc[dataframe['clave'].isin(
            ['CI341','IA428','IA450','LIA447','CL13','IA440'])].reset_index(drop=True)
        return duplicados(aero_9)

def seleccionar_semestre_cien_comp(x, dataframe):
    if x==1:
        computacion_1 = dataframe.loc[dataframe['clave'].isin(
            ['CB170','CB171','CB172','CB173','CI174','I101','UN115','UN216'])].reset_index(drop=True)
        return duplicados(computacion_1)
    elif x==2:
        computacion_2 = dataframe.loc[dataframe['clave'].isin(
            ['CB270','CB271','CB272','CI274','I201','UN200','UN316'])].reset_index(drop=True)
        return duplicados(computacion_2)
    elif x==3:
        computacion_3 = dataframe.loc[dataframe['clave'].isin(
            ['CB370','CB371','CB372','CB373','CI374','I301'])].reset_index(drop=True)
        return duplicados(computacion_3)
    elif x==4:
        computacion_4 = dataframe.loc[dataframe['clave'].isin(
            ['CB470','CB471','CB473','CI474','CI475','I401','IA478'])].reset_index(drop=True)
        return duplicados(computacion_4)
    elif x==5:
        computacion_5 = dataframe.loc[dataframe['clave'].isin(
            ['CB571','CI574','CI575','CI576','CI577','CL13','IA578','IN501'])].reset_index(drop=True)
        return duplicados(computacion_5)
    elif x==6:
        computacion_6 = dataframe.loc[dataframe['clave'].isin(
            ['CI671','CI675','CI676','CI677','CI678','CI679','CS680','IN601'])].reset_index(drop=True)
        return duplicados(computacion_6)
    elif x==7:
        computacion_7 = dataframe.loc[dataframe['clave'].isin(
            ['CI771','CI775','CI776','IA778','IN701','OC407','OPC01','OPC02',
             'OPC03','OPC10'])].reset_index(drop=True)
        return duplicados(computacion_7)
    elif x==8:
        computacion_8 = dataframe.loc[dataframe['clave'].isin(
            ['CI871','CI872','CI876','CI877','IA878','OC206','OPC04','OPC05',
             'OPC06','OPC11'])].reset_index(drop=True)
        return duplicados(computacion_8)
    elif x==9:
        computacion_9 = dataframe.loc[dataframe['clave'].isin(
            ['CI972','CI976','CI977','IA978','IA979','OC510','OPC13','OPC07',
             'OPC08','OPC09'])].reset_index(drop=True)
        return duplicados(computacion_9)
 
def seleccionar_semestre_minas(x, dataframe):
    if x==1:
        minas_1 = dataframe.loc[dataframe['clave'].isin(
            ['101','102','103','106','107','108','115','216','I101'])].reset_index(drop=True)
        return duplicados(minas_1)
    elif x==2:
        minas_2 = dataframe.loc[dataframe['clave'].isin(
            ['100','104','200','201','202','203','210','211','316','I201'])].reset_index(drop=True)
        return duplicados(minas_2)
    elif x==3:
        minas_3 = dataframe.loc[dataframe['clave'].isin(
            ['209','301','302','303','407','454','501','I301'])].reset_index(drop=True)
        return duplicados(minas_3)
    elif x==4:
        minas_4 = dataframe.loc[dataframe['clave'].isin(
            ['206','403','406','451','457','503','555','772','I401'])].reset_index(drop=True)
        return duplicados(minas_4)
    elif x==5:
        minas_5 = dataframe.loc[dataframe['clave'].isin(
            ['322','326','502','534','601','609','610'])].reset_index(drop=True)
        return duplicados(minas_5)
    elif x==6:
        minas_6 = dataframe.loc[dataframe['clave'].isin(
            ['323','520','550','553','607','711','775'])].reset_index(drop=True)
        return duplicados(minas_6)
    elif x==7:
        minas_7 = dataframe.loc[dataframe['clave'].isin(
            ['651','710','801','873','876','914','950'])].reset_index(drop=True)
        return duplicados(minas_7)
    elif x==8:
        minas_8 = dataframe.loc[dataframe['clave'].isin(
            ['510','757','810','812','916','956'])].reset_index(drop=True)
        return duplicados(minas_8)
    elif x==9:
        minas_9 = dataframe.loc[dataframe['clave'].isin(
            ['850','917','918','920','071','752','991'])].reset_index(drop=True)
        return duplicados(minas_9)

def seleccionar_semestre_hard(x, dataframe):
    if x==1:
        hard_1 = dataframe.loc[dataframe['clave'].isin(
            ['101','102','103','114','115','216','I101'])].reset_index(drop=True)
        return duplicados(hard_1)
    elif x==2:
        hard_2 = dataframe.loc[dataframe['clave'].isin(
            ['100','104','200','201','202','203','215','316','I201'])].reset_index(drop=True)
        return duplicados(hard_2)
    elif x==3:
        hard_3 = dataframe.loc[dataframe['clave'].isin(
            ['214','301','302','313','315','407','634','I301'])].reset_index(drop=True)
        return duplicados(hard_3)
    elif x==4:
        hard_4 = dataframe.loc[dataframe['clave'].isin(
            ['206','403','413','415','417','440','503','I401'])].reset_index(drop=True)
        return duplicados(hard_4)
    elif x==5:
        hard_5 = dataframe.loc[dataframe['clave'].isin(
            ['515','517','518','540','541','601','643','IC01'])].reset_index(drop=True)
        return duplicados(hard_5)
    elif x==6:
        hard_6 = dataframe.loc[dataframe['clave'].isin(
            ['519','533','615','618','640','746','747'])].reset_index(drop=True)
        return duplicados(hard_6)
    elif x==7:
        hard_7 = dataframe.loc[dataframe['clave'].isin(
            ['725','728','729','741','748','801','846'])].reset_index(drop=True)
        return duplicados(hard_7)
    elif x==8:
        hard_8 = dataframe.loc[dataframe['clave'].isin(
            ['510','727','828','832','833','842','845'])].reset_index(drop=True)
        return duplicados(hard_8)
    elif x==9: #Noveno semestre, optativas de tópicos
        hard_9 = dataframe.loc[dataframe['clave'].isin(
            ['962', '967', '923','948','961','CL13','963'])].reset_index(drop=True)
        return duplicados(hard_9)
    elif x==10: #Noveno semestre, optativas de ciencias 
        hard_10 = dataframe.loc[dataframe['clave'].isin(
            ['OPH02','938','936','OPH01','931'])].reset_index(drop=True)
        return duplicados(hard_10)  
    
def seleccionar_semestre_topo(x, dataframe):
    if x==1:
        topo_1 = dataframe.loc[dataframe['clave'].isin(
            ['CB101','CB102','CB103','I101','IB107','IB108','OC109','UN115','UN216'])].reset_index(drop=True)
        return duplicados(topo_1)
    elif x==2:
        topo_2 = dataframe.loc[dataframe['clave'].isin(
            ['CB201','CB202','CB203','I201','IB210','IB211','IB454','OC209','UN200',
             'UN316'])].reset_index(drop=True)
        return duplicados(topo_2)
    elif x==3:
        topo_3 = dataframe.loc[dataframe['clave'].isin(
            ['CB217','CB301','CB303','CB304','CB305','I301','IB328','IB329','LCB217',
             'OC309'])].reset_index(drop=True)
        return duplicados(topo_3)
    elif x==4:
        topo_4 = dataframe.loc[dataframe['clave'].isin(
            ['CB403','CB507','CS310','I401','IA421','IA431','IA432','IB304',
             'IB330','IB508'])].reset_index(drop=True)
        return duplicados(topo_4)
    elif x==5:
        topo_5 = dataframe.loc[dataframe['clave'].isin(
            ['321','IA322','IA326','IA423','IA426','IA626','IA627','IB321',
             'IB520','IB602'])].reset_index(drop=True)
        return duplicados(topo_5)
    elif x==6:
        topo_6 = dataframe.loc[dataframe['clave'].isin(
            ['IA722','IA723','IA724','IB405','IB433','IB629','IB805','OC207',
             'OC407'])].reset_index(drop=True)
        return duplicados(topo_6)
    elif x==7:
        topo_7 = dataframe.loc[dataframe['clave'].isin(
            ['631','IA522','IA523','IA619','IA621','IA623','IA631','OC505',
             'OC510'])].reset_index(drop=True)
        return duplicados(topo_7)

def seleccionar_semestre_procesos(x, dataframe):
    if x==1:
        procesos_1 = dataframe.loc[dataframe['clave'].isin(
            ['CB103','LCB103','CB102','CB101','CI112','UN216','UN115','I101'])].reset_index(drop=True)
        return duplicados(procesos_1)
    elif x==2:
        procesos_2 = dataframe.loc[dataframe['clave'].isin(
            ['CB217','LCB217','CB201','CB203','CS312','UN316','UN200','I201'])].reset_index(drop=True)
        return duplicados(procesos_2)
    elif x==3:
        procesos_3 = dataframe.loc[dataframe['clave'].isin(
            ['CB301','LCB303','CB303','CB302','LCB302','CI209','OC206','OC407','I301'])].reset_index(drop=True)
        return duplicados(procesos_3)
    elif x==4:
        procesos_4 = dataframe.loc[dataframe['clave'].isin(
            ['CB401','CI409','CB406','LCB406','CB403','CI408','LCI408','CI417','LCI417',
             'I401'])].reset_index(drop=True)
        return duplicados(procesos_4)
    elif x==5:
        procesos_5 = dataframe.loc[dataframe['clave'].isin(
            ['CI509','CI664','CI660','CI665','CI662','CI531','IN501'])].reset_index(drop=True)
        return duplicados(procesos_5)
    elif x==6:
        procesos_6 = dataframe.loc[dataframe['clave'].isin(
            ['CI764','CI762','IA604','CI631','CU01','CS610','IN601'])].reset_index(drop=True)
        return duplicados(procesos_6)
    elif x==7:
        procesos_7 = dataframe.loc[dataframe['clave'].isin(
            ['CB801','CI862','IA704','CI720','CS710','CS715','IN71'])].reset_index(drop=True)
        return duplicados(procesos_7)
    elif x==8:
        procesos_8 = dataframe.loc[dataframe['clave'].isin(
            ['IA861','IA840','IA870','IA959','IA880','IA850','IA890','IN810'])].reset_index(drop=True)
        return duplicados(procesos_8)
    elif x==9:
        procesos_9 = dataframe.loc[dataframe['clave'].isin(
            ['IA830','IA937','IA950','IA860','CL13','IA995','IA980',
             'IA990','IA960','IA820','IA939'])].reset_index(drop=True)
        return duplicados(procesos_9)

def seleccionar_semestre_fisica(x, dataframe):
    if x==1:
        fisica_1 = dataframe.loc[dataframe['clave'].isin(
            ['CS101','CS102','CS103','CS104','I101','UN101','UN102'])].reset_index(drop=True)
        return duplicados(fisica_1)
    elif x==2:
        fisica_2 = dataframe.loc[dataframe['clave'].isin(
            ['CS201','CS202','CS203','CS204','I201','PE201','UN201','UN202'])].reset_index(drop=True)
        return duplicados(fisica_2)
    elif x==3:
        fisica_3 = dataframe.loc[dataframe['clave'].isin(
            ['CI301','CI302','CS301','CS303','CS304','I301','PE301'])].reset_index(drop=True)
        return duplicados(fisica_3)
    elif x==4:
        fisica_4 = dataframe.loc[dataframe['clave'].isin(
            ['CI401','CI402','CI403','CS401','CS404','I401','PE401','SH401'])].reset_index(drop=True)
        return duplicados(fisica_4)
    elif x==5:
        fisica_5 = dataframe.loc[dataframe['clave'].isin(
            ['CI501','CI502','CI503','CS501','SH501','PE501','SH502'])].reset_index(drop=True)
        return duplicados(fisica_5)
    elif x==6:
        fisica_6 = dataframe.loc[dataframe['clave'].isin(
            ['CI601','CI602','CI603','CS601','PE601','SH602','SH601'])].reset_index(drop=True)
        return duplicados(fisica_6)
    elif x==7:
        fisica_7 = dataframe.loc[dataframe['clave'].isin(
            ['CI701','CI702','CI703','CI704','IA701','PE701','SH701'])].reset_index(drop=True)
        return duplicados(fisica_7)
    elif x==8:
        fisica_8 = dataframe.loc[dataframe['clave'].isin(
            ['IA801','SH801','OPIM01','OPIF01','OPIF04','OPIF05','OPIF06','OPIF13','OPIF13'])].reset_index(drop=True)
        return duplicados(fisica_8)
    elif x==9:
        fisica_9 = dataframe.loc[dataframe['clave'].isin(
            ['IA901','SH901','PE901','SH902','OPIM04','OPIF07','OPIF11','OPIF12','OPIF14'])].reset_index(drop=True)
        return duplicados(fisica_9)

def seleccionar_semestre_mate(x, dataframe):
    if x==1:
        mate_1 = dataframe.loc[dataframe['clave'].isin(
            ['CS101','CS102','CS103','CS104','I101','UN101','UN102'])].reset_index(drop=True)
        return duplicados(mate_1)
    elif x==2:
        mate_2 = dataframe.loc[dataframe['clave'].isin(
            ['CS201','CS202','CS204','CS205','I201','PE201','UN201','UN202'])].reset_index(drop=True)
        return duplicados(mate_2)
    elif x==3:
        mate_3 = dataframe.loc[dataframe['clave'].isin(
            ['CI301','CI302','CS301','CS304','CS305','I301','PE301'])].reset_index(drop=True)
        return duplicados(mate_3)
    elif x==4:
        mate_4 = dataframe.loc[dataframe['clave'].isin(
            ['CI401','CI402','CI404','CS401','CS404','I401','PE401','SH401'])].reset_index(drop=True)
        return duplicados(mate_4)
    elif x==5:
        mate_5 = dataframe.loc[dataframe['clave'].isin(
            ['CI504','CI505','CI506','CS501','SH501','PE501','SH502'])].reset_index(drop=True)
        return duplicados(mate_5)
    elif x==6:
        mate_6 = dataframe.loc[dataframe['clave'].isin(
            ['CI604','CI605','CI606','CS601','PE601','SH603','SH601'])].reset_index(drop=True)
        return duplicados(mate_6)
    elif x==7:
        mate_7 = dataframe.loc[dataframe['clave'].isin(
            ['CI705','CI706','CI707','IA702','PE701','SH702'])].reset_index(drop=True)
        return duplicados(mate_7)
    elif x==8:
        mate_8 = dataframe.loc[dataframe['clave'].isin(
            ['IA802','IA803','SH801','OPIM01','OPIM02','OPIM07'])].reset_index(drop=True)
        return duplicados(mate_8)
    elif x==9:
        mate_9 = dataframe.loc[dataframe['clave'].isin(
            ['IA902','SH901','PE901','SH903','OPIM04','OPIM05','OPIM08'])].reset_index(drop=True)
        return duplicados(mate_9)
    

def variables_para_el_algoritmo(semestre):
    """
    Prepara las variables necesarias para el algoritmo genético a partir de los datos de un semestre.

    Args:
    - semestre (DataFrame de Pandas): Un DataFrame que contiene información sobre el semestre, incluyendo claves y horas.

    Returns:
    - tabla_vacia (lista de listas): Una tabla vacía representada como una lista de listas.
    - claves (lista): Una lista de las claves disponibles para asignar en el horario.
    - claves_disponibles (lista): Una copia de la lista de claves disponibles para asignar en el horario.
    - horas_por_clave (dict): Un diccionario que mapea las claves a la cantidad de horas asignadas.
    """
    # Define la tabla vacía
    tabla_vacia = crear_tabla_vacia()

    # Definir las claves disponibles y las horas por clave
    claves = list(semestre["clave"])
    claves_disponibles = claves.copy()
    horas_por_clave = dict(zip(semestre["clave"], semestre["horas"]))
    
    return tabla_vacia, claves, claves_disponibles, horas_por_clave


def obtener_tres_mejores_tablas(num_generaciones, tabla_vacia, claves, claves_disponibles, horas_por_clave):
    """
    Obtiene las tres mejores tablas de horarios generadas por el algoritmo genético.

    Args:
    - num_generaciones (int): El número de generaciones que el algoritmo genético debe ejecutar.
    - tabla_vacia (lista de listas): Una tabla vacía representada como una lista de listas.
    - claves (lista): Una lista de las claves disponibles para asignar en el horario.
    - claves_disponibles (lista): Una copia de la lista de claves disponibles para asignar en el horario.
    - horas_por_clave (dict): Un diccionario que mapea las claves a la cantidad de horas asignadas.

    Returns:
    - df_tres_mejores_tablas (DataFrame de Pandas): Un DataFrame que contiene las tres mejores tablas de horarios.
    """
    tres_mejores_tablas = []

    # Crear una columna vacía llamada "-"
    columna_vacia = pd.DataFrame(columns=["-"])
    
    for _ in range(3):
        mejor_tabla = algoritmo_genetico(num_generaciones, tabla_vacia, claves, claves_disponibles, horas_por_clave)
        tres_mejores_tablas.append(mejor_tabla)

    # Concatenar las tablas y la columna vacía
    df_tres_mejores_tablas = pd.concat([tabla.join(columna_vacia) for tabla in tres_mejores_tablas], axis=1)
    
    return df_tres_mejores_tablas.fillna("-")
