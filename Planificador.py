import random
import Conexion
import Solicitud
import Sistema_de_Transporte
import math
class Planificador: #se instancia UNA VEZ.
    def __init__(self, nombre):
        self.nombre=nombre
        print(f"Planificador: {self.nombre}")

    def procesar_siguiente(self):
        """
        Desencola y retorna la siguiente solicitud.
        """
        if not Solicitud.Solicitud_Transporte.cola_solicitudes:
            print("No hay solicitudes pendientes.")
            return None, None, None
        solicitud = Solicitud.Solicitud_Transporte.cola_solicitudes.popleft()

        grafo=Planificador.construir_grafo(Conexion.Conexion.conexiones_por_tipo)

        dic_rutas=Planificador.encontrar_todas_rutas(grafo,solicitud.origen, solicitud.destino)
        
        tupla_menor_costo, tupla_menor_tiempo= Planificador.analisis_costo_tiempo(dic_rutas,solicitud.peso_kg) #las tuplas van: (costo,tiempo,ruta,tipo)
        return solicitud.id_carga,tupla_menor_costo, tupla_menor_tiempo
    @staticmethod
    def construir_grafo(diccionario):
        grafo = {}
        for conexiones in diccionario.values():
            for conexion in conexiones:
                if conexion.origen not in grafo:
                    grafo[conexion.origen] = []
                grafo[conexion.origen].append(conexion)
    
        return grafo #devuelve el grafo usado en  encontrar todas rutas
    @staticmethod
    def encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, camino_actual=None, nodos_visitados=None):
        if camino_actual is None:
            camino_actual = []
        if nodos_visitados is None:
            nodos_visitados = {nodo_inicio}
        nodo_actual = nodo_inicio if not camino_actual else camino_actual[-1].destino
        if nodo_actual == nodo_fin:
            return [camino_actual]

        rutas = []
        print(grafo)
        
        print(grafo.get(nodo_actual, []))
        for conexion in grafo.get(nodo_actual, []):
            
            if Planificador.es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados): #va self?
                nuevo_camino = camino_actual + [conexion]
                nuevos_visitados = set(nodos_visitados)
                nuevos_visitados.add(conexion.destino)
                rutas += Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, nuevo_camino, nuevos_visitados) #va self?
            
        return rutas  #esto devuielve una lista de rutas (lista de listas). Cada ruta es una lista de conexiones que hay entre los nodos. 
    @staticmethod   
    def encontrar_todas_rutas(grafo, nodo_inicio, nodo_fin):
        rutas_por_tipo = {}
        for tipo in Conexion.Conexion.tipos:
            rutas = Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo) #va self?
            #print(rutas)
            if rutas:
                rutas_por_tipo[tipo] = rutas
            
        return rutas_por_tipo #esto si devuelve un diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).

    @staticmethod
    def indice_mas_bajo(lista):
        if not lista:
            raise ValueError("La lista está vacía")
        return min(range(len(lista)), key=lambda i: lista[i])
    
    @staticmethod
    def es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
        return (
            conexion.tipo == tipo and
            conexion.origen == nodo_actual and
            conexion.destino not in nodos_visitados
        )
    @staticmethod
    def cantidad_vehiculos(ruta, vehiculo, carga): #ruta es una lista de conexiones
        if isinstance(vehiculo, Sistema_de_Transporte.Automotor) : #carga es la carga que se quiere transportar, capacidad es el peso maximo del vehiculo
            capacidades_posibles=[]
            for conexion in ruta:
                if conexion.restriccion == "peso_max": #Si tiene la restriccion de peso maximo, entonces cada camion debe tener la minima entre el "peso maximo" y la capacidad del camion
                    cantidad = math.ceil(carga / min(float(conexion.valor_restriccion),vehiculo.capacidad)) 
                    capacidades_posibles.append(cantidad)
            if capacidades_posibles:
                return max(capacidades_posibles)
        return math.ceil(carga / vehiculo.capacidad)
            
    @staticmethod
    def calcular_costo(conexion, cantidad_vehiculos, vehiculo, carga): #funcion GENERAL para calcular el costo de un tipo de vehiculo especifico para una conexion especifica
        if not isinstance(vehiculo, Sistema_de_Transporte.Tipo_transporte):
             raise ValueError("Tipo de transporte no reconocido")
        costo_x_km = vehiculo.costo_km
        costo_fijo = vehiculo.costo_fijo
        if isinstance(vehiculo, Sistema_de_Transporte.Automotor):
            capacidad_max_por_vehiculo = vehiculo.capacidad
            if conexion.restriccion == "peso_max":
                capacidad_max_por_vehiculo = min(vehiculo.capacidad, float(conexion.valor_restriccion))

            carga_restante = carga
            costo_variable_total = 0
            while carga_restante > 0:
                carga_vehiculo = min(capacidad_max_por_vehiculo, carga_restante)
                costo_kg = 2 if carga_vehiculo > 15000 else 1
                costo_variable_total += carga_vehiculo * costo_kg
                carga_restante -= carga_vehiculo
            
            costo_total = cantidad_vehiculos * (costo_fijo + costo_x_km * conexion.distancia) + costo_variable_total
        else:
            costo_total = (cantidad_vehiculos * (costo_fijo + costo_x_km * conexion.distancia)) + vehiculo.costo_kg * carga
        return costo_total
     
    def calcular_tiempo(conexion, vehiculo):
        distancia = conexion.distancia
        if not isinstance(vehiculo, Sistema_de_Transporte.Tipo_transporte):
            velocidad = vehiculo.velocidad_nominal
        else:
            raise ValueError("Tipo de transporte no reconocido")
        tiempo_total = distancia / velocidad
        return tiempo_total
    
    @staticmethod
    def analisis_costo_tiempo(diccionario_rutas,carga):# el diccionario_rutas es un diccionario de encontrar_todas_rutas
        lista_costo = []
        lista_tiempo = []
        lista_rutas = []
        lista_tipos=[]
        lista_cantidad_vehiculos = []
        
        for tipo_transporte,lista_rutas_dic in diccionario_rutas.items() :
            for ruta in lista_rutas_dic:
                costo_total, tiempo_total,tipo, cantidad_vehiculos = Planificador.calcular_costo_tiempo(ruta,carga,tipo_transporte)
                lista_rutas.append(ruta)
                lista_costo.append(costo_total)
                lista_tiempo.append(tiempo_total)
                lista_tipos.append(tipo)
                lista_cantidad_vehiculos.append(cantidad_vehiculos)
                
        if not lista_costo or not lista_tiempo:
             print(" No hay rutas válidas para calcular.")
             return None, None
       
        i_costo = Planificador.indice_mas_bajo(lista_costo)
        i_tiempo = Planificador.indice_mas_bajo(lista_tiempo)
        
        tupla_menor_costo=(lista_costo[i_costo],lista_tiempo[i_costo],lista_rutas[i_costo],lista_tipos[i_costo],lista_cantidad_vehiculos[i_costo], carga)
        tupla_menor_tiempo=(lista_costo[i_tiempo],lista_tiempo[i_tiempo],lista_rutas[i_tiempo],lista_tipos[i_tiempo],lista_cantidad_vehiculos[i_tiempo], carga)
        return tupla_menor_costo, tupla_menor_tiempo
    @staticmethod
    def calcular_costo_tiempo(ruta,carga,tipo_transporte): # ruta es lista de conexiones. #ruta= [zarate->bsas, bsas->mdp] cada uno es un objeto conexion
        costo_total = 0
        tiempo_total = 0
        cantidad_vehiculos = Planificador.cantidad_vehiculos(ruta, tipo_transporte, carga)
        
        for conexion in ruta:
            if tipo_transporte=="Aerea":  #CHEQUEAR COMO SE ESCRIBEN LOS STRINGS ESTOS
                if conexion.restriccion == 'prob_mal_tiempo':
                    prob = float(conexion.valor_restriccion)
                    velocidad = Planificador.determinar_vel(prob)
                    vehiculo=Sistema_de_Transporte.Aerea(velocidad)
                else:
                    vehiculo=Sistema_de_Transporte.Aerea()
                    
            elif tipo_transporte=="Fluvial":
                if conexion.valor_restriccion.lower() == "fluvial":
                    vehiculo=Sistema_de_Transporte.Fluvial(costo_fijo = 500)
                elif conexion.valor_restriccion.lower() == "maritima":
                    vehiculo=Sistema_de_Transporte.Fluvial(costo_fijo = 1500)
                else:
                    vehiculo=Sistema_de_Transporte.Fluvial()
                
            elif tipo_transporte=="Automotor":
                vehiculo=Sistema_de_Transporte.Automotor(costo_x_kg=2)              
                
            elif tipo_transporte == "Ferroviaria":
                if conexion.restriccion == 'velocidad_max':
                    velocidad = min(100, float(conexion.valor_restriccion))
                    if conexion.distancia < 200:
                        vehiculo=Sistema_de_Transporte.Ferroviaria(velocidad,costo_x_km = 20)
                    else:
                        vehiculo=Sistema_de_Transporte.Ferroviaria(velocidad,costo_x_km = 15)
                else:
                    vehiculo=Sistema_de_Transporte.Ferroviaria()
            costo_total += Planificador.calcular_costo(conexion,cantidad_vehiculos,vehiculo, carga) # va self?
            tiempo_total += Planificador.calcular_tiempo(conexion, vehiculo)
        return costo_total,tiempo_total,tipo_transporte, cantidad_vehiculos
        
    @staticmethod
    def determinar_vel(prob_mal_tiempo, velocidad_buen_tiempo = 600, velocidad_mal_tiempo = 400):
        
        if not 0 <= prob_mal_tiempo <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        if random.random() <= prob_mal_tiempo:
            return velocidad_mal_tiempo
        else:
            return velocidad_buen_tiempo