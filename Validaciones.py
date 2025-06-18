import csv
import Nodo
import Conexion
import Solicitud
#por ejemplo con nodo: cuando entro a Nodo para verificar que el nodo no exista todavia, eso no deberia ser un metodo de clase dentro de Nodo
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
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    for i in range(len(lista)):
        if isinstance(lista[i], str):
            lista[i] = lista[i].strip().lower()
    if len(lista) != 6:
        raise TypeError('Cantidad de atributos insuficientes para instanciar una conexión')
    lista[4] = None if lista[4] == '' else lista[4]
    lista[5] = None if lista[5] == '' else lista[5]
    if Nodo.Nodo.get_nombre(lista[0]) is None:  
        raise ValueError(f'Nodo "{lista[0]}" inexistente')
    if Nodo.Nodo.get_nombre(lista[1]) is None:  
        raise ValueError(f'Nodo "{lista[1]}" inexistente')
    if lista[2] not in tipos:
        raise ValueError(f'El tipo ingresado "{lista[2]}" es invalido')
    if not isinstance(lista[3], (int, float, str)):
        raise TypeError(f'Tipo de dato incorrecto para el atributo Distancia')
    else:
        try:
            lista[3] = float(lista[3])
        except ValueError:
            raise ValueError('El valor de la restricción debe ser un número válido')
        if lista[3] <= 0:
            raise ValueError(f'La distancia no puede ser negativa o 0')
    if (lista[4] == None and lista[5]) or (lista[5] == None and lista[4]):
        raise ValueError(f'Error en la restricción y el valor de la misma')
    if not (lista[4] == None and lista[5] == None):
        if lista[2] == 'fluvial':
            if not (lista[4] == 'tipo'):
                raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte fluvial')
            else:
                if not isinstance(lista[5],str):
                    raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')
                elif not (lista[5] == 'fluvial' or lista[5] == 'maritimo'):
                    raise ValueError(f'El valor de la restricción {lista[5]} es inválido para la restricción')
        if lista[2] == 'aerea':
            if not (lista[4] == 'prob_mal_tiempo'):
                raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte aéreo')
            else:
                if not isinstance(lista[5], (int, float, str)):
                    raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')                
                else:
                    try:
                        lista[5] = float(lista[5])
                    except ValueError:
                        raise ValueError('El valor de la restricción debe ser un número válido')
                    if not (1 > lista[5] > 0):
                        raise ValueError(f'El valor de la restricción es inválido')
        if lista[2] == 'ferroviaria':
            if not (lista[4] == 'velocidad_max'):
                raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte ferroviario')
            else:
                if not isinstance(lista[5], (int, str, float)):
                    raise ValueError(f'El valor de la restricción es inválido')    
                else:
                    try:
                        lista[5] = float(lista[5])
                    except ValueError:
                        raise ValueError('El valor de la restricción debe ser un número válido')
                    if not (lista[5] > 0):
                        raise ValueError(f'El valor de la restricción es inválido')
        if lista[2] == 'automotor':
            if not (lista[4] == 'peso_max'):
                raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte automotor')
            else:
                if not isinstance(lista[5], (str, int, float)):
                    raise ValueError(f'El valor de la restricción es inválido')    
                else: 
                    try:
                        lista[5] = float(lista[5])
                    except ValueError:
                        raise ValueError('El valor de la restricción debe ser un número válido')
                    if not (lista[5] > 0):
                        raise ValueError(f'El valor de la restricción es inválido')
    if Conexion.Conexion.get_conexion(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5]) is not None:
        raise ValueError(f"La conexion '{lista[0]} a {lista[1]} de tipo: {lista[2]}' ya fue cargado.")
    return lista
                                     
def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    i =1
    for fila in datos:
        if fila:
            try:
                conexion = validar_conexion(fila)
                Conexion.Conexion(conexion[0],conexion[1],conexion[2],conexion[3],conexion[4],conexion[5])
                Conexion.Conexion(conexion[1],conexion[0],conexion[2],conexion[3],conexion[4],conexion[5])
            except (TypeError, ValueError) as e:
                print(f"Error al cargar conexiones '{fila[0]}': {e}")
                i = 0
    if i:
        print('Conexiones cargadas exitosamente.')
def validar_nodo(entrada):
    """
    Valida que la entrada para un nodo sea un string válido y no esté duplicado.
    """
    if not isinstance(entrada, str):
        raise TypeError("El nombre del nodo debe ser un string.")

    nombre = entrada.strip().lower()

    if nombre == "":
        raise ValueError("El nombre del nodo no puede estar vacío.")

    if Nodo.Nodo.get_nombre(nombre) is not None:
        raise ValueError(f"El nodo '{nombre}' ya fue cargado.")

    return nombre

def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    i= 1
    for fila in datos:
        if fila:  # chequea que no esté vacía
            try:
                nombre = validar_nodo(fila[0])
                Nodo.Nodo(nombre)
            except (TypeError, ValueError) as e:
                print(f"Error al cargar nodo '{fila[0].lower()}': {e}")
                i = 0
    if i:
        print('Nodos cargados exitosamente.')            
                
            
def validar_solicitud(fila):
    if len(fila) != 4:
        raise ValueError("La solicitud debe tener exactamente 4 campos: id_carga, peso_kg, origen, destino")

    id_carga, peso, origen, destino = [x.strip() for x in fila]

    # Validar ID duplicado en cola
    for solicitud in Solicitud.Solicitud_Transporte.cola_solicitudes:
        if solicitud.id_carga == id_carga:
            raise ValueError(f"Ya existe una solicitud con ID '{id_carga}'")

    # Validar peso
    peso = float(peso)
    if peso <= 0:
        raise ValueError("El peso debe ser un número positivo")   #PROBAR ESTO

    # Validar nodos
    origen_nodo = Nodo.Nodo.get_nombre(origen)
    destino_nodo = Nodo.Nodo.get_nombre(destino)

    if origen_nodo is None:
        raise ValueError(f"El nodo de origen '{origen}' no existe.")
    if destino_nodo is None:
        raise ValueError(f"El nodo de destino '{destino}' no existe.")
    if origen_nodo == destino_nodo:
        raise ValueError("El nodo de origen y destino no pueden ser el mismo.")

    return id_carga, peso, origen_nodo, destino_nodo


def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    i=1
    for fila in datos:
        if fila:
            try:
                id_carga, peso, origen, destino = validar_solicitud(fila)
                Solicitud.Solicitud_Transporte(id_carga, peso, origen, destino)
            except (ValueError, TypeError) as e:
                print(f"Error al cargar solicitud: {e}")
                i=0
    if i:
        print('Solicitudes cargadas exitosamente.')
        
                
'''
Pensar funciones agregar/borrar conexiones, nodos, vehiculos
Esto se agregaria en los inits (en este caso se sacaria de cargar_conexiones pero sirve para una futura funcion de agregar conexion)

'''