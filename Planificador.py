import random
import Conexion
import Solicitud
import Sistema_de_Transporte
import math
import Nodo
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


        # Validacion para evitar errores si los nodos estan desconectados
        origen = solicitud.origen.nombre if isinstance(solicitud.origen, Nodo.Nodo) else solicitud.origen
        destino = solicitud.destino.nombre if isinstance(solicitud.destino, Nodo.Nodo) else solicitud.destino
        
        if origen not in grafo:
            raise TypeError(f" El nodo de origen '{origen}' no está conectado a ninguna ruta.")
            
        if destino not in grafo and not any(con.destino == destino for conexiones in grafo.values() for con in conexiones):
            raise TypeError(f" El nodo de destino '{destino}' no está conectado a ninguna ruta.")
            
        
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
    def es_conexion_valida(conexion, tipo, nodo_actual, nodos_visitados):
       return  (
        conexion.tipo.lower() == tipo.lower() and
        conexion.origen == nodo_actual and
        conexion.destino not in nodos_visitados
        )
    @staticmethod
    def encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, camino_actual=None, nodos_visitados=None):
        tipo = tipo.lower()
        if camino_actual is None:
            camino_actual = []

        if nodos_visitados is None:
            nodo_inicio_str = nodo_inicio.nombre if isinstance(nodo_inicio, Nodo.Nodo) else nodo_inicio
            nodos_visitados = {nodo_inicio_str}

        nodo_actual = camino_actual[-1].destino if camino_actual else nodo_inicio
        if isinstance(nodo_actual, Nodo.Nodo):
            nodo_actual = nodo_actual.nombre

        nodo_fin_str = nodo_fin.nombre if isinstance(nodo_fin, Nodo.Nodo) else nodo_fin

        if nodo_actual == nodo_fin_str:
            return [camino_actual]
        rutas = []
        
        for conexion in grafo.get(nodo_actual, []):       
            origen = conexion.origen.nombre if isinstance(conexion.origen, Nodo.Nodo) else conexion.origen
            destino = conexion.destino.nombre if isinstance(conexion.destino, Nodo.Nodo) else conexion.destino
            if (
            conexion.tipo.lower() == tipo and
            origen == nodo_actual and
            destino not in nodos_visitados
            ):
                nuevo_camino = camino_actual + [conexion]
                nuevos_visitados = set(nodos_visitados)
                nuevos_visitados.add(destino)
                rutas += Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo, nuevo_camino, nuevos_visitados)

    
        return rutas  #esto devuielve una lista de rutas (lista de listas). Cada ruta es una lista de conexiones que hay entre los nodos. 
    @staticmethod   
    def encontrar_todas_rutas(grafo, nodo_inicio, nodo_fin):
        rutas_por_tipo = {}
        for tipo in list(Conexion.Conexion.tipos):
            tipo = tipo.lower()
            rutas = Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo) #va self?
            if rutas:
                rutas_por_tipo[tipo] = rutas
        return rutas_por_tipo #esto si devuelve un diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).

    @staticmethod
    def indice_mas_bajo(lista):
        if not lista:
            raise ValueError("La lista está vacía")
        return min(range(len(lista)), key=lambda i: lista[i])
    
    @staticmethod
    def crear_vehiculo_base(tipo_transporte):
        tipo = tipo_transporte.lower()
        if tipo == "automotor":
            return Sistema_de_Transporte.Automotor()
        elif tipo == "aerea":
            return Sistema_de_Transporte.Aerea()
        elif tipo == "fluvial":
            return Sistema_de_Transporte.Fluvial()
        elif tipo == "ferroviaria":
            return Sistema_de_Transporte.Ferroviaria()
        else:
            raise ValueError("Tipo de transporte no reconocido.")

    @staticmethod
    def calcular_costo_variable(ruta, vehiculo, carga):
        costo_variable_total = 0
        if isinstance(vehiculo, Sistema_de_Transporte.Automotor):
            capacidad_efectiva = vehiculo.capacidad_carga
            for conexion in ruta:
                if getattr(conexion, 'restriccion', None) == "peso_max":
                    valor = getattr(conexion, 'valor_restriccion', None)
                    if valor:
                        capacidad_efectiva = min(capacidad_efectiva, float(valor))
            carga_restante = carga
            while carga_restante > 0:
                carga_vehiculo = min(capacidad_efectiva, carga_restante)
                costo_kg = 2 if carga_vehiculo >= 15000 else 1
                costo_variable_total += carga_vehiculo * costo_kg
                carga_restante -= carga_vehiculo
        else:
            costo_variable_total = vehiculo.costo_kg * carga
        return costo_variable_total

    @staticmethod
    def ajustar_vehiculo_por_conexion(conexion, tipo_transporte):
        tipo = tipo_transporte.lower()
        if tipo == "aerea":
            if getattr(conexion, 'restriccion', None) == 'prob_mal_tiempo':
                prob = float(getattr(conexion, 'valor_restriccion', 0))
                velocidad = Planificador.determinar_vel(prob)
                return Sistema_de_Transporte.Aerea(velocidad)
            else:
                return Sistema_de_Transporte.Aerea()
        elif tipo == "fluvial":
            valor_restriccion = getattr(conexion, 'valor_restriccion', '').lower()
            if valor_restriccion == "fluvial":
                return Sistema_de_Transporte.Fluvial(costo_fijo=500)
            elif valor_restriccion == "maritima":
                return Sistema_de_Transporte.Fluvial(costo_fijo=1500)
            else:
                return Sistema_de_Transporte.Fluvial()
        elif tipo == "ferroviaria":
            if getattr(conexion, 'restriccion', None) == 'velocidad_max':
                velocidad = min(100, float(getattr(conexion, 'valor_restriccion', 100)))
            else:
                velocidad = 100
            if conexion.distancia < 200:
                return Sistema_de_Transporte.Ferroviaria(velocidad, costo_km=20)
            else:
                return Sistema_de_Transporte.Ferroviaria(velocidad, costo_km=15)
        else:

            return None

        
    @staticmethod
    def cantidad_vehiculos(ruta, vehiculo, carga): #ruta es una lista de conexiones
        if isinstance(vehiculo, Sistema_de_Transporte.Automotor) : #carga es la carga que se quiere transportar, capacidad es el peso maximo del vehiculo
            capacidades_posibles=[]
            for conexion in ruta:
                restriccion = getattr(conexion, 'restriccion', None)
                valor_restriccion = getattr(conexion, 'valor_restriccion', None)
                if restriccion == "peso_max" and valor_restriccion is not None: #Si tiene la restriccion de peso maximo, entonces cada camion debe tener la minima entre el "peso maximo" y la capacidad del camion
                     max_peso=min(float(valor_restriccion),vehiculo.capacidad_carga)
                     cantidad = math.ceil(carga /max_peso)
                     capacidades_posibles.append(cantidad)
            if capacidades_posibles:
                return max(capacidades_posibles)
        return math.ceil(carga / vehiculo.capacidad_carga)
            
    @staticmethod
    def calcular_costo(conexion, cantidad_vehiculos, vehiculo): 
        if not isinstance(vehiculo, Sistema_de_Transporte.Tipo_transporte):
             raise ValueError("Tipo de transporte no reconocido")
        costo_km = vehiculo.costo_km
        costo_fijo = vehiculo.costo_fijo
        costo_total = (cantidad_vehiculos * (costo_fijo + costo_km * conexion.distancia)) 
        return costo_total
    
    @staticmethod
    def calcular_tiempo(conexion, vehiculo):
        if not isinstance(vehiculo, Sistema_de_Transporte.Tipo_transporte):
            raise ValueError("Tipo de transporte no reconocido")
        distancia = conexion.distancia
        velocidad = vehiculo.velocidad_nominal
        return (distancia / velocidad)

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
        vehiculo = Planificador.crear_vehiculo_base(tipo_transporte)
        cantidad_vehiculos = Planificador.cantidad_vehiculos(ruta, vehiculo, carga)
        costo_variable_total = Planificador.calcular_costo_variable(ruta, vehiculo, carga)
        for conexion in ruta:
            vehiculo_ajustado = Planificador.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is not None:
                vehiculo = vehiculo_ajustado
            costo_total += Planificador.calcular_costo(conexion,cantidad_vehiculos,vehiculo)
            tiempo_total += Planificador.calcular_tiempo(conexion, vehiculo)
        
        costo_total += costo_variable_total
        return costo_total, tiempo_total, tipo_transporte, cantidad_vehiculos


    @staticmethod
    def determinar_vel(prob_mal_tiempo, velocidad_buen_tiempo = 600, velocidad_mal_tiempo = 400):
        if not 0 <= prob_mal_tiempo <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        if random.random() <= prob_mal_tiempo:
            return velocidad_mal_tiempo
        else:
            return velocidad_buen_tiempo

    @staticmethod
    def obtener_tipo_vehiculo(vehiculo):
        if isinstance(vehiculo, Sistema_de_Transporte.Automotor):
            return "automotor"
        elif isinstance(vehiculo, Sistema_de_Transporte.Aerea):
            return "aerea"
        elif isinstance(vehiculo, Sistema_de_Transporte.Fluvial):
            return "fluvial"
        elif isinstance(vehiculo, Sistema_de_Transporte.Ferroviaria):
            return "ferroviaria"
        else:
            raise ValueError("Tipo de transporte no reconocido")
