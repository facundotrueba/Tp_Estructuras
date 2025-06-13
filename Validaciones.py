import csv
import Sistema_de_Transporte
import auxiliar

def leer_csv(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, mode="r") as file:
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

def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        if i and i[0].strip().lower():
            Sistema_de_Transporte.Nodo(i[0].strip().lower())
            
def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        Sistema_de_Transporte.Solicitud_Transporte(i[0], i[1], i[2], i[3])


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