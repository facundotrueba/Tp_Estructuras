import csv
import Sistema_de_Transporte
import auxiliar

def leer_csv(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, mode="r",encoding="utf-8") as file:
            lector = csv.reader(file)
            next(lector) 
            for fila in lector:
                datos.append(fila)
        return datos
    except FileNotFoundError:
        print("Archivo no encontrado")

def validar_conexion(lista):
    atributos = ['Origen', 'Destino', 'Tipo', 'Distancia', 'Restricción', 'Valor restricción']
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    conexion_valida = True
    for i in range(len(lista)):
        if isinstance(lista[i], str):
            lista[i] = lista[i].strip().lower()
    if len(lista) != 6:
        raise TypeError('Cantidad de atributos insuficientes para instanciar una conexión')
    for i in range(len(lista)):
        if i == 0 or i == 1 or i == 2:
            if not isinstance(lista[i], str):
                conexion_valida = False
                raise TypeError(f'Tipo de dato incorrecto para el atributo {atributos[i]}') 
            if i == 2: 
                if lista[i] not in tipos:
                    conexion_valida = False
                    raise ValueError(f'El tipo ingresado "{lista[i]}" es invalido')
            else:
                if Sistema_de_Transporte.Nodo.get_nombre(lista[i]) not in Sistema_de_Transporte.Nodo.lista_nodos:  
                    conexion_valida = False
                    raise ValueError(f'Nodos inexistente')
        elif i == 3:
            if not isinstance(lista[i], (int, float, str)):
                conexion_valida = False
                raise TypeError(f'Tipo de dato incorrecto para el atributo {atributos[i]}')
            else:
                lista[i] = float(lista[i])
                if lista[i] <= 0:
                    conexion_valida = False
                    raise ValueError(f'La distancia no puede ser negativa o 0')                
        elif i == 4 or i == 5:
            if lista[i] == '':
                lista[i] = None
    if (lista[4] == None and lista[5]) or (lista[5] == None and lista[4]):
        conexion_valida = False
        raise ValueError(f'Error en la restricción y el valor de la misma')
    if lista[2] == 'fluvial':
        if not (lista[4] or lista [5]):
            pass
        elif not (lista[4] == 'tipo'):
            conexion_valida = False
            raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte fluvial')
        else:
            if not isinstance(lista[5],str):
                conexion_valida = False
                raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')
            elif not (lista[5] == 'fluvial' or lista[5] == 'maritimo'):
                conexion_valida = False
                raise ValueError(f'El valor de la restricción {lista[5]} es inválido para la restricción')
    if lista[2] == 'aerea':
        if not (lista[4] or lista [5]):
            pass
        elif not (lista[4] == 'prob_mal_tiempo'):
            conexion_valida = False
            raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte aéreo')
        else:
            if not isinstance(lista[5], (int, float, str)):
                raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')                
            else:
                lista[5] = float(lista[5])
                if not (1 > lista[5] > 0):
                    conexion_valida = False
                    raise ValueError(f'El valor de la restricción es inválido')
    if lista[2] == 'ferroviaria':
        if not (lista[4] or lista [5]):
            pass
        elif not (lista[4] == 'velocidad_max'):
            conexion_valida = False
            raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte ferroviario')
        else:
            if not isinstance(lista[5], (int, str, float)):
                conexion_valida = False
                raise ValueError(f'El valor de la restricción es inválido')    
            else:
                lista[5] = float(lista[5])
                if not (lista[5] > 0):
                    conexion_valida = False
                    raise ValueError(f'El valor de la restricción es inválido')
    if lista[2] == 'automotor':
        if not (lista[4] or lista [5]):
            pass
        elif not (lista[4] == 'peso_max'):
            conexion_valida = False
            raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte automotor')
        else:
            lista[5] = float(lista[5])
            if not isinstance(lista[5], (str, int, float)):
                conexion_valida = False
                raise ValueError(f'El valor de la restricción es inválido')    
            else: 
                if not (lista[5] > 0):
                    conexion_valida = False
                    raise ValueError(f'El valor de la restricción es inválido')
    return lista, conexion_valida
                                        
def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        conexion,es_valida = validar_conexion(i)
        if es_valida:
            Sistema_de_Transporte.Conexion(conexion[0],conexion[1],conexion[2],conexion[3],conexion[4],conexion[5])
            Sistema_de_Transporte.Conexion(conexion[1],conexion[0],conexion[2],conexion[3],conexion[4],conexion[5])

def validar_nodo(entrada):
    """
    Valida que la entrada para un nodo sea un string válido y no esté duplicado.
    """
    if not isinstance(entrada, str):
        raise TypeError("El nombre del nodo debe ser un string.")

    nombre = entrada.strip().lower()

    if nombre == "":
        raise ValueError("El nombre del nodo no puede estar vacío.")

    if Sistema_de_Transporte.Nodo.get_nombre(nombre) is not None:
        raise ValueError(f"El nodo '{nombre}' ya fue cargado.")

    return nombre

def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for fila in datos:
        if fila:  # chequea que no esté vacía
            try:
                nombre = validar_nodo(fila[0])
                Sistema_de_Transporte.Nodo(nombre)
            except (TypeError, ValueError) as e:
                print(f"Error al cargar nodo '{fila[0]}': {e}")

# def cargar_nodos(nombre_archivo):
#     datos = leer_csv(nombre_archivo)
#     for i in datos:
#         if i and i[0].strip().lower():
#             Sistema_de_Transporte.Nodo(i[0].strip().lower())
            
# para validar nodos solamente q sean str y hacer funcion validar nodos donde lo hagas y que no esten
# ya en la lista de nodos creados en la propia clase 
            
def validar_solicitud(fila):
    if len(fila) != 4:
        raise ValueError("La solicitud debe tener exactamente 4 campos: id_carga, peso_kg, origen, destino")

    id_carga, peso, origen, destino = [x.strip() for x in fila]

    # Validar ID
    if not isinstance(id_carga, str):
        raise TypeError("El ID de carga debe ser un string.")
    
    if not id_carga.startswith("CARGA_"):
        raise ValueError(f"ID de carga inválido: {id_carga}")     # SACAR ESTA PORONGA Y QUE VALIDE QUE TODOS LOS IDS SEAN DISITNTOS Y CHAU
    sufijo = id_carga[6:]
    if not sufijo.isdigit():
        raise ValueError(f"ID de carga debe terminar en número entero: {id_carga}")
    if int(sufijo) <= 0:
        raise ValueError("El número de ID de carga debe ser mayor a 0")

    # Validar ID duplicado en cola
    for solicitud in Sistema_de_Transporte.Solicitud_Transporte.cola_solicitudes:
        if solicitud.id_carga == id_carga:
            raise ValueError(f"Ya existe una solicitud con ID '{id_carga}'")

    # Validar peso
    try:
        peso = float(peso)
        if peso <= 0:
            raise ValueError("El peso debe ser un número positivo")   #PROBAR ESTO
    except:
        raise TypeError("El peso debe ser un número (int o float)")

    # Validar nodos
    origen_nodo = Sistema_de_Transporte.Nodo.get_nombre(origen)
    destino_nodo = Sistema_de_Transporte.Nodo.get_nombre(destino)

    if origen_nodo is None:
        raise ValueError(f"El nodo de origen '{origen}' no existe.")
    if destino_nodo is None:
        raise ValueError(f"El nodo de destino '{destino}' no existe.")
    if origen_nodo == destino_nodo:
        raise ValueError("El nodo de origen y destino no pueden ser el mismo.")

    return id_carga, peso, origen_nodo, destino_nodo


def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for fila in datos:
        try:
            id_carga, peso, origen, destino = validar_solicitud(fila)
            Sistema_de_Transporte.Solicitud_Transporte(id_carga, peso, origen, destino)
        except (ValueError, TypeError) as e:
            print(f"Error al cargar solicitud: {e}")
            
            
# def cargar_solicitudes(nombre_archivo):
#     datos = leer_csv(nombre_archivo)
#     for i in datos:
#         Sistema_de_Transporte.Solicitud_Transporte(i[0], i[1], i[2], i[3])

# validar que peso que sea num int o float y positivo, que origen y destino antes que sea str
# y luego isinstance nodos y que no sean el mismo, por ultimo, id_carga,
# validar que los primeros 6 chars sean CARGA_ y despues que sea un numero int 


# print(Sistema_de_Transporte.Nodo.lista_nodos)


# l = validar_conexion(l)
# print (l)


auxiliar.cargar_nodos('nodos.csv')
cargar_conexiones('conexiones.csv')
print(Sistema_de_Transporte.Conexion.conexiones_por_tipo)



'''
Pensar funciones agregar/borrar conexiones, nodos, vehiculos
Esto se agregaria en los inits (en este caso se sacaria de cargar_conexiones pero sirve para una futura funcion de agregar conexion)

'''