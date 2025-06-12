
import math
import random
import matplotlib.pyplot as plt
import numpy as np

class Planificador: #se instancia UNA VEZ.
    
    def construir_grafo(diccionario):
        grafo = {}
        for conexiones in diccionario.values():
            for conexion in conexiones:
                if conexion.origen not in grafo:
                    grafo[conexion.origen] = []
                grafo[conexion.origen].append(conexion)
        return grafo #devuelve el grafo usado en  encontrar todas rutas
        
    def encontrar_todas_rutas(grafo, nodo_inicio, nodo_fin):
        rutas_por_tipo = {}
        for tipo in Conexion.tipos:
            rutas = Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo)
            if rutas:
                rutas_por_tipo[tipo] = rutas
        return rutas_por_tipo #esto si devuelve un diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).

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
            if Planificador.es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
                nuevo_camino = camino_actual + [conexion]
                nuevos_visitados = set(nodos_visitados)
                nuevos_visitados.add(conexion.destino)
                rutas += Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, nuevo_camino, nuevos_visitados)
        return rutas  #esto devuielve una lista de rutas (lista de listas). Cada ruta es una lista de conexiones que hay entre los nodos. 

    def indice_mas_bajo(lista):
        if not lista:
            raise ValueError("La lista está vacía")
        return min(range(len(lista)), key=lambda i: lista[i])
    

    def es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
        return (
            conexion.tipo == tipo and
            conexion.origen == nodo_actual and
            conexion.destino not in nodos_visitados
        )
#restricciones: 
# velocidad max: tipo ferroviario (costo por km)
# carga max: tipo automotor (costo por kg)
# fluvial o maritima distinta taza fija
# conexion aerea hace algo raro con probabilidad del tiempo
    """
diccionario_rutas = {
ferroviaria = { [[Zarate>Buenos_aires,Buenos_aires>Azul,Azul>Mar_del_Plata]
[Zarate,Azul,Mar_del_Plata]}
}
}
"""
    def cantidad_vehiculos(self, ruta, vehiculo, carga): #ruta es una lista de conexiones
        if isinstance(vehiculo, Automotor) : #carga es la carga que se quiere transportar, capacidad es el peso maximo del vehiculo
            capacidades_posibles=[]
            for conexion in ruta:
                if conexion.restriccion == "peso_max": #Si tiene la restriccion de peso maximo, entonces cada camion debe tener la minima entre el "peso maximo" y la capacidad del camion
                    cantidad = math.ceil(carga / min(float(conexion.valor_restriccion),vehiculo.capacidad)) 
                    capacidades_posibles.append(cantidad)
            if capacidades_posibles:
                return max(capacidades_posibles)
        return math.ceil(carga / vehiculo.capacidad)
            
    
    def calcular_costo(conexion, cantidad_vehiculos, vehiculo, carga): #funcion GENERAL para calcular el costo de un tipo de vehiculo especifico para una conexion especifica
        if not isinstance(vehiculo, Tipo_transporte):
             raise ValueError("Tipo de transporte no reconocido")
        costo_x_km = vehiculo.costo_km
        costo_fijo = vehiculo.costo_fijo
         # CASO AUTOMOTOR: costo por kg depende de la carga por vehículo
        if isinstance(vehiculo, Automotor):
            # Determinar la capacidad máxima real por vehículo (limitada por conexión si aplica)
            capacidad_max_por_vehiculo = vehiculo.capacidad
            if conexion.restriccion == "peso_max":
                capacidad_max_por_vehiculo = min(vehiculo.capacidad, float(conexion.valor_restriccion))

            carga_restante = carga
            costo_variable_total = 0

            # Repartir la carga en vehículos y calcular el costo por kg de cada uno
            while carga_restante > 0:
                carga_vehiculo = min(capacidad_max_por_vehiculo, carga_restante)
    
                # Determinar el costo por kg según carga del automotor
                costo_kg = 2 if carga_vehiculo > 15000 else 1
                # Sumar costo de esta parte
                costo_variable_total += carga_vehiculo * costo_kg
                carga_restante -= carga_vehiculo
            # Costo total = fijos por cada vehículo + variable por kg
            costo_total = cantidad_vehiculos * (costo_fijo + costo_x_km * conexion.distancia) + costo_variable_total

            # CASO GENERAL (no automotor): aplicar costo fijo por kg
        else:
            costo_total = (cantidad_vehiculos * (costo_fijo + costo_x_km * conexion.distancia)) + vehiculo.costo_kg * carga
        return costo_total
            
    def calcular_tiempo(conexion, vehiculo):
        distancia = conexion.distancia

        if not isinstance(vehiculo, Tipo_transporte):
            raise ValueError("Tipo de transporte no reconocido")
        velocidad = vehiculo.velocidad_nominal
        tiempo_total = distancia / velocidad

        return tiempo_total
    
    
    def analisis_costo_tiempo(self, diccionario_rutas,carga,tipo_transporte):# el diccionario_rutas es un diccionario de encontrar_todas_rutas
        lista_costo = []
        lista_tiempo = []
        lista_rutas = []
        lista_tipos=[]
        for ruta in diccionario_rutas.values() :
            costo_total, tiempo_total,tipo = Planificador.calcular_costo_tiempo(ruta,carga,tipo_transporte)
            lista_rutas.append(ruta)
            lista_costo.append(costo_total)
            lista_tiempo.append(tiempo_total)
            lista_tipos.append(tipo)

        menor_costo = lista_costo[Planificador.indice_mas_bajo(lista_costo)]
        ruta_menor_costo = lista_rutas[Planificador.indice_mas_bajo(lista_costo)]
        tiempo_menor_costo = lista_tiempo[Planificador.indice_mas_bajo(lista_costo)]
        tipo_menor_costo = lista_tipos[Planificador.indice_mas_bajo(lista_costo)]

        menor_tiempo = lista_tiempo[Planificador.indice_mas_bajo(lista_tiempo)]
        ruta_menor_tiempo = lista_rutas[Planificador.indice_mas_bajo(lista_tiempo)]
        costo_menor_tiempo = lista_costo[Planificador.indice_mas_bajo(lista_tiempo)]
        tipo_menor_tiempo = lista_tipos[Planificador.indice_mas_bajo(lista_tiempo)]
        return menor_costo,tiempo_menor_costo,ruta_menor_costo,tipo_menor_costo, menor_tiempo, costo_menor_tiempo, ruta_menor_tiempo,tipo_menor_tiempo
    
    def calcular_costo_tiempo(self, ruta,carga,tipo_transporte): # ruta es lista de conexiones. #ruta= [zarate->bsas, bsas->mdp] cada uno es un objeto conexion
        costo_total = 0
        tiempo_total = 0
        
        cantidad_vehiculos = Planificador.cantidad_vehiculos(ruta, tipo_transporte, carga)
        
        for conexion in ruta:
            if tipo_transporte=="Aerea":  #CHEQUEAR COMO SE ESCRIBEN LOS STRINGS ESTOS
                if conexion.restriccion == 'prob_mal_tiempo':
                    prob = float(conexion.valor_restriccion)
                    velocidad = Planificador.determinar_vel(prob)
                    vehiculo=Aerea(velocidad)
                else:
                    vehiculo=Aerea()
                    
            elif tipo_transporte=="Fluvial":
                if conexion.valor_restriccion.lower() == "fluvial":
                    vehiculo=Fluvial(costo_fijo = 500)
                elif conexion.valor_restriccion.lower() == "maritima":
                    vehiculo=Fluvial(costo_fijo = 1500)
                else:
                    vehiculo=Fluvial()
                
            elif tipo_transporte=="Automotor":
                vehiculo=Automotor(costo_x_kg=2)              
                
                
            elif tipo_transporte == "Ferroviaria":
                if conexion.restriccion == 'velocidad_max':
                    velocidad = min(100, float(conexion.valor_restriccion))
                    if conexion.distancia < 200:
                        vehiculo=Ferroviaria(velocidad,costo_x_km = 20)
                    else:
                        vehiculo=Ferroviaria(velocidad,costo_x_km = 15)
                else:
                    vehiculo=Ferroviaria()
            costo_total += Planificador.calcular_costo(conexion,cantidad_vehiculos,vehiculo, carga)
            tiempo_total += Planificador.calcular_tiempo(conexion, vehiculo)
        return costo_total,tiempo_total,tipo_transporte
        
    
    @staticmethod
    def determinar_vel(prob_mal_tiempo, velocidad_buen_tiempo = 600, velocidad_mal_tiempo = 400):
        
        if not 0 <= prob_mal_tiempo <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        if random.random() <= prob_mal_tiempo:
            return velocidad_mal_tiempo
        else:
            return velocidad_buen_tiempo
    
class Nodo:
    lista_nodos = []
    def __init__(self, nombre):
        self.nombre = nombre
        Nodo.lista_nodos.append(self)
        self.tipos_disponibles = set()#almacena el tipo disponible de nodo
        
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
    conexiones_por_tipo = {} #clave=tipo, valor=set de conexiones del tipo
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max", "tipo", "prob_mal_tiempo"}

    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion):

        if self.tipo not in Conexion.tipos:
            raise TypeError("El tipo de conexión es incorrecto.")
        self.origen = origen
        self.destino = destino
        self.tipo = tipo.strip().lower()
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

        self.origen.tipos_disponibles.add(self.tipo)#agrega los tipos al nodo
        self.destino.tipos_disponibles.add(self.tipo)

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

class Tipo_transporte:
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg): #lo de los costos hacer archivo csv CHEQUEAR LUCAS
        if velocidad_nominal <= 0:
            ValueError("La velocidad no puede ser negativa")
        if capacidad_carga <= 0:
            ValueError("La capacidad de carga no puede ser negativa")
        self.velocidad_nominal=velocidad_nominal
        self.capacidad_carga=capacidad_carga
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg
    


class Automotor(Tipo_transporte): # el codigo va a funcionar de tal manera que si se arranca una ruta con 8 automotores, Si se puede despues hacer con 10 automotores y despues 8 de vuelta en otra conexion
    def __init__(self,  velocidad_nominal=80, capacidad_carga= 30000, costo_fijo=30, costo_km= 5, costo_kg= 1):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

    
class Aerea(Tipo_transporte):
    def __init__(self, velocidad_nominal = 600, capacidad_carga = 5000, costo_fijo = 750, costo_km = 40, costo_kg = 10, velocidad_mal_tiempo = 400):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        self.velocidad_mal_tiempo = velocidad_mal_tiempo


class Fluvial(Tipo_transporte):
    def __init__(self, velocidad_nominal = 40, capacidad_carga = 100000, costo_fijo = 500, costo_km = 15, costo_kg = 2):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

class Ferroviaria(Tipo_transporte):
    def __init__(self, velocidad_nominal = 100, capacidad_carga = 150000, costo_fijo = 100, costo_km = 20, costo_kg = 3):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        


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
    def __init__(self, id_solicitud, ruta, costo, tiempo, optimizacion, vehiculo, cantidad_vehiculos, carga):#revisar este print
        self.id_solicitud =id_solicitud
        self.ruta=ruta
        self.costo=costo
        self.tiempo=tiempo
        self.optimizacion= optimizacion
        self.vehiculo = vehiculo
    
    def calcular_arrays_distancia_tiempo_acumulados(self, vehiculo):
        distancias = []
        tiempos = []
        distancia_acum = 0
        tiempo_acum = 0

        for conexion in self.ruta: 
            distancia_acum += conexion.distancia
            tiempo_conexion = Planificador.calcular_tiempo(conexion, vehiculo)
            tiempo_acum += tiempo_conexion
            distancias.append(distancia_acum)
            tiempos.append(tiempo_acum)
        
        return np.array(distancias), np.array(tiempos)
    
    def graficar_distancia_vs_tiempo(self,vehiculo):
        distancias, tiempos = self.calcular_arrays_distancia_tiempo_acumulados(vehiculo)
        plt.plot(tiempos, distancias, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()
    
    def calcular_arrays_costo_distancia_acumulada(self, vehiculo):
        costos = []
        distancias = []
        costo_acum = 0
        distancia_acum = 0
        
        for conexion in self.ruta:
            costo_conexion = Planificador.calcular_costo(conexion, self.cantidad_vehiculos, vehiculo, self.carga)
            costo_acum += costo_conexion
            distancia_acum += conexion.distancia
            costos.append(costo_acum)
            distancias.append(distancia_acum)
            
        return np.array(costos), np.array(distancias)
       
    def graficar_costo_vs_distancia(self,vehiculo):
        costos, distancias = self.calcular_arrays_costo_distancia_acumulada(vehiculo)
        plt.plot(distancias, costos, marker="o")
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.grid(True)
        plt.show()
        
    def mostrar_resumen(self):
        return f"Itinerario: {self.ruta} | cantidad de conexion: {len(self.ruta)} | Tiempo: {self.tiempo} min | Costo: ${self.costo}"

    
#ex-tobi: del dicc de encontrar_todas_rutas tengo que llamar a calcular_costos_tiempo para que le calcule el costo y tiempo a cada una de esas rutas. de todos esos tiemposy costos tengo que buscar la ruta con tiempo y costo mas bajo. 
#diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).
# Cada ruta es una lista de conexiones que hay entre los nodos. 

def testear_funciones(grafo, nombre_origen, nombre_destino):
    origen = Nodo.get_nombre(nombre_origen)
    destino = Nodo.get_nombre(nombre_destino)

    if origen is None or destino is None:
        print("Origen o destino no existen.")
        return

    rutas_por_tipo = Planificador.encontrar_todas_rutas(grafo, origen, destino)

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


'''
Agregar capacidad multimodal en la clase nodo
Agregar validaciones (Preguntar)
Cambiar calculo de costos teniendo en cuenta que hay que llenar cada camion antes de empezar a cargar el proximo (corregir)
Calcular velocidad
Revisar print Itinerario
hacer gráficos
Mandar tiempo y costos en las dos rutas posibles (tiempo en la optimizada por costo y costo en la optimizada por tiempo)
Hacer main

'''