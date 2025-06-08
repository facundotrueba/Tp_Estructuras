import csv
import math

class Planificador: #se instancia MUCHAS VECES. UN PLANIFICADOR POR CADA SOLICITUD.(segun lo que dice ne la consigna en objetivo general)
    '''
    metodos:
    encontrar rutas

    calcular 



    
    '''



class Nodo:
    lista_nodos = []

    def __init__(self, nombre):
        self.nombre = nombre
        Nodo.lista_nodos.append(self)
        
    def __str__(self):
        return self.nombre

    @classmethod
    def get_nombre(cls, nombre):
        if not isinstance(nombre, str):
            return None
        nombre = nombre.strip().lower()
        for nodo in cls.lista_nodos:
            if nodo.nombre.strip().lower() == nombre:
                return nodo
        return None


        
    
    
#DICCIONARIO: CLAVE 1 TIPO, CLAVE 2 NODO, CLAVE 3 DESTINO, lista (dist, restriccion, valor_restriccion)
class Conexion: 
    conexiones_por_tipo = {}#clave=tipo, valor=set de conexiones del tipo
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max", "tipo", "prob_mal_tiempo"}

    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion):
        self.origen = origen
        self.destino = destino

        self.tipo = tipo.strip().lower()
        if self.tipo not in Conexion.tipos:
            raise TypeError("El tipo de conexión es incorrecto.")
        

        self.distancia = float(distancia)

        if restriccion:
            restriccion = restriccion.strip().lower()
            if restriccion not in Conexion.restricciones_validas:
                raise ValueError(f"Restricción no válida: {restriccion}")
            self.restriccion = restriccion
            self.valor_restriccion = valor_restriccion
        else:
            self.restriccion = None
            self.valor_restriccion = None

        if self.tipo not in Conexion.conexiones_por_tipo:
            Conexion.conexiones_por_tipo[self.tipo] = {self}
        else:
            Conexion.conexiones_por_tipo[self.tipo].add(self)

    def __str__(self):
        return f"De {self.origen} a {self.destino}. Tipo: {self.tipo}"

    def __eq__(self, other):
        return (
            self.origen == other.origen and
            self.destino == other.destino and
            self.tipo == other.tipo and
            self.distancia == other.distancia and
            self.restriccion == other.restriccion and
            self.valor_restriccion == other.valor_restriccion
        )

    def __hash__(self): #el gordo me dice que lo tenga ni idea
        return hash((self.origen, self.destino, self.tipo, self.distancia, self.restriccion, self.valor_restriccion))
    
        

class Tipo_transporte:
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg): #lo de los costos hacer archivo csv CHEQUEAR LUCAS
        
        if velocidad_nominal<= 0:
            ValueError("La velocidad no puede ser negativa")
        if capacidad_carga<= 0:
            ValueError("La capacidad de carga no puede ser negativa")
        self.velocidad_nominal=velocidad_nominal
        self.capacidad_carga=capacidad_carga
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg
    
    def calcular_costo(self, distancia, peso): #funcion GENERAL para calcular el costo de un tipo de vehiculo especifico para una conexion especifica
        cantidad = math.ceil(peso / self.capacidad_carga)  #cuantos vehiculos se necesitan para transportar esa carga EN ESA CONEXION 
        costo_total= cantidad * (self.costo_fijo + self.costo_km * distancia + self.costo_kg * peso)
        return costo_total

    def calcular_tiempo(self, distancia, tipo): #funcion GENERAL para calcular el costo de un tipo de vehiculo especifico para una conexion especifica
        tiempo= distancia / self.velocidad_nominal 
        return tiempo

#restricciones: 
# velocidad max: tipo ferroviario (costo por km)
# carga max: tipo automotor (costo por kg)
# fluvial o maritima distinta taza fija
# conexion aerea hace algo raro con probabilidad del tiempo


class Automotor(Tipo_transporte): # el codigo va a funcionar de tal manera que si se arranca una ruta con 8 automotores, Si se puede despues hacer con 10 automotores y despues 8 de vuelta en otra conexion
    def __init__(self,  velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__( velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
    
    def calcular_costo (self, distancia, peso): 
        pass
    
    
class Aerea(Tipo_transporte):
  def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
      super().__init__( velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
  def calcular_tiempo(self, distancia, tipo): 
      pass  
      

class Fluvial(Tipo_transporte):
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__( velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

    def calcular_costo (self, distancia, peso): 
        pass
class Ferroviaria(Tipo_transporte):
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__( velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
    def calcular_tiempo(self, distancia, tipo): 
        pass  
    
    

class Solicitud_Transporte:
    def __init__(self, id_carga,nombre, peso_kg, origen, destino):
        if peso_kg <= 0: #Validaciones
            raise ValueError("El peso debe ser mayor a cero.")
        if origen == destino:
            raise ValueError("El destino debe ser distinto del origen.")
        self.nombre=nombre
        self.id_carga=id_carga
        self.peso_kg=peso_kg
        self.origen=origen
        self.destino=destino
        

class Itinerario:
    def __init__(self, secuencia_tramos, costo, tiempo, destino):
        self.secuencia_tramos=secuencia_tramos
        self.costo=costo
        self.tiempo=tiempo
        self.destino=destino
    
    def mostrar_resumen(self):
        return f"Itinerario hacia {self.destino} | Tramos: {len(self.secuencia_tramos)} | Tiempo: {self.tiempo} min | Costo: ${self.costo}"


class Red_Transporte:
        pass
                

def calcular_costo_tiempo(ruta,peso,tipo_transporte): # ruta es lista de conexiones. #ruta= [zarate->bsas, bsas->mdp]
    for i in range(len(ruta)):
        distancia = i.distancia
        costo_total += Tipo_transporte.calcular_costo(distancia,peso,tipo_transporte)
        tiempo_total += Tipo_transporte.calcular_tiempo(distancia,tipo_transporte)
    return costo_total,tiempo_total
    
#ex-tobi: del dicc de encontrar_todas_rutas tengo que llamar a calcular_costos_tiempo para que le calcule el costo y tiempo a cada una de esas rutas. de todos esos tiemposy costos tengo que buscar la ruta con tiempo y costo mas bajo. 
#diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).
# Cada ruta es una lista de conexiones que hay entre los nodos. 

""""
diccionario_rutas = {
ferroviaria = { [[Zarate>Buenos_aires,Buenos_aires>Azul,Azul>Mar_del_Plata]
[Zarate,Azul,Mar_del_Plata]}
}
}
"""
def indice_mas_bajo(lista):
    if not lista:
        raise ValueError("La lista está vacía")
    return min(range(len(lista)), key=lambda i: lista[i])

def analisis_costo_tiempo(diccionario_rutas):# el diccionario_rutas es un diccionario de encontrar_todas_rutas
    lista_costo = []
    lista_tiempo = []
    lista_rutas = []
    for ruta in diccionario_rutas.values :
        costo_total, tiempo_total = calcular_costo_tiempo(ruta)
        lista_rutas.append(ruta)
        lista_costo.append(costo_total)
        lista_tiempo.append(tiempo_total)
    menor_costo = lista_costo[indice_mas_bajo(lista_costo)]
    ruta_menor_costo = lista_costo[indice_mas_bajo(lista_costo)]
    menor_tiempo = lista_tiempo[indice_mas_bajo(lista_tiempo)]
    ruta_menor_tiempo = lista_tiempo[indice_mas_bajo(lista_tiempo)]
    return menor_costo, ruta_menor_costo, menor_tiempo, ruta_menor_tiempo
    


    
def es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
    return (
        conexion.tipo == tipo and
        conexion.origen == nodo_actual and
        conexion.destino not in nodos_visitados
    )
def encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, camino_actual=None, nodos_visitados=None):
    if camino_actual is None:
        camino_actual = []
    if nodos_visitados is None:
        nodos_visitados = {nodo_inicio}

    nodo_actual = nodo_inicio if not camino_actual else camino_actual[-1].destino
    if nodo_actual == nodo_fin:
        return [camino_actual]

    rutas = []
    for conexion in grafo.get(nodo_actual, []):
        if es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
            nuevo_camino = camino_actual + [conexion]
            nuevos_visitados = set(nodos_visitados)
            nuevos_visitados.add(conexion.destino)
            rutas += encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, nuevo_camino, nuevos_visitados)
    return rutas  #esto devuielve una lista de rutas (lista de listas). Cada ruta es una lista de conexiones que hay entre los nodos. 

def encontrar_todas_rutas(grafo, nodo_inicio, nodo_fin):
    rutas_por_tipo = {}
    for tipo in Conexion.tipos:
        rutas = encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo)
        if rutas:
            rutas_por_tipo[tipo] = rutas
    return rutas_por_tipo #esto si devuelve un diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).
  

def construir_grafo(diccionario):
    grafo = {}
    for conexiones in diccionario.values():
        for conexion in conexiones:
            if conexion.origen not in grafo:
                grafo[conexion.origen] = []
            grafo[conexion.origen].append(conexion)
    return grafo #devuelve el grafo usado en  encontrar todas rutas

def testear_funciones(grafo, nombre_origen, nombre_destino):
    origen = Nodo.get_nombre(nombre_origen)
    destino = Nodo.get_nombre(nombre_destino)

    if origen is None or destino is None:
        print("Origen o destino no existen.")
        return

    rutas_por_tipo = encontrar_todas_rutas(grafo, origen, destino)

    if not rutas_por_tipo:
        print(f"No se encontraron rutas de {nombre_origen} a {nombre_destino}.")
        return

    for tipo, rutas in rutas_por_tipo.items():
        print(f"\nRUTAS DE TIPO: {tipo.upper()} ({len(rutas)} ruta(s))")
        for i, ruta in enumerate(rutas, 1):
            nodos_en_ruta = [ruta[0].origen] + [c.destino for c in ruta]
            print(f"  Ruta {i}:")
            for conexion in ruta:
                print(f"    {conexion}")

            if len(nodos_en_ruta) != len(set(nodos_en_ruta)):
                print("    ❌ Error: Se repite algún nodo.")
