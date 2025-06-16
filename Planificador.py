#import todoooo
from collections import deque
import Conexion
class Planificador: #se instancia UNA VEZ.
    
    
    def procesar_siguiente(self):
        """
        Desencola y retorna la siguiente solicitud.
        """
        if not self.cola:
            print("No hay solicitudes pendientes.")
            return None
        solicitud = self.cola.popleft()
        grafo=self.construir_grafo(Conexion.conexiones_por_tipo)
        dic_rutas=self.encontrar_todas_rutas(grafo,solicitud.origen, solicitud.destino)
        tupla_menor_costo, tupla_menor_tiempo=self.analisis_costo_tiempo(dic_rutas,solicitud.peso_kg) #las tuplas van: (costo,tiempo,ruta,tipo)
                                          
        
        
        return tupla_menor_costo, tupla_menor_tiempo
    

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
            velocidad = vehiculo.velocidad_nominal
        else:
            raise ValueError("Tipo de transporte no reconocido")

        tiempo_total = distancia / velocidad

        return tiempo_total
    
    
    def analisis_costo_tiempo(self, diccionario_rutas,carga):# el diccionario_rutas es un diccionario de encontrar_todas_rutas
        lista_costo = []
        lista_tiempo = []
        lista_rutas = []
        lista_tipos=[]
        for tipo_transporte,lista_rutas_dic in diccionario_rutas.items() :
            for ruta in lista_rutas_dic:
                
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
        
        #las tuplas van: (costo,tiempo,ruta,tipo)
        tupla_menor_costo=(menor_costo,tiempo_menor_costo,ruta_menor_costo,tipo_menor_costo)
        tupla_menor_tiempo=(costo_menor_tiempo,menor_tiempo, ruta_menor_tiempo,tipo_menor_tiempo)
        return tupla_menor_costo, tupla_menor_tiempo
    
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