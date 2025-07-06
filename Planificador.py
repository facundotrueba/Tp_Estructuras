import Sistema_de_Transporte
import Conexion
import Solicitud
import Nodo
import Itinerario

class Planificador: #se instancia UNA VEZ.
    def __init__(self, nombre):
        self.nombre=nombre
        print(f"Planificador: {self.nombre}")
        self.historial_solicitudes_procesadas = Itinerario.Lista_enlazada()
       
    def procesar_siguiente(self):
        #Desencola y retorna la siguiente solicitud.
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

        tupla_menor_costo, tupla_menor_tiempo, tupla_menor_riesgo= Planificador.analisis_costo_tiempo_riesgo(dic_rutas,solicitud.peso_kg) #las tuplas van: (costo,tiempo,ruta,tipo)
        
        return solicitud.id_carga,tupla_menor_costo, tupla_menor_tiempo, tupla_menor_riesgo
    
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
            rutas = Planificador.encontrar_rutas_tipo(grafo, nodo_inicio, nodo_fin, tipo) 
            if rutas:
                rutas_por_tipo[tipo] = rutas
        return rutas_por_tipo #esto si devuelve un diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).

    @staticmethod
    def indice_mas_bajo(lista):
        if not lista:
            raise ValueError("La lista está vacía")
        return min(range(len(lista)), key=lambda i: lista[i])
    
    @staticmethod
    def analisis_costo_tiempo_riesgo(diccionario_rutas,carga):# el diccionario_rutas es un diccionario de encontrar_todas_rutas
        lista_costo = []
        lista_tiempo = []
        lista_rutas = []
        lista_tipos=[]
        lista_cantidad_vehiculos = []
        lista_riesgo = []
        
        for tipo_transporte,lista_rutas_dic in diccionario_rutas.items() :
            for ruta in lista_rutas_dic:
                costo_total, tiempo_total,tipo, cantidad_vehiculos, riesgo_total = Sistema_de_Transporte.Tipo_transporte.calcular_costo_tiempo_riesgo(ruta,carga,tipo_transporte)
                lista_rutas.append(ruta)
                lista_costo.append(costo_total)
                lista_tiempo.append(tiempo_total)
                lista_tipos.append(tipo)
                lista_cantidad_vehiculos.append(cantidad_vehiculos)
                lista_riesgo.append(riesgo_total)
                
        if not lista_costo or not lista_tiempo:
             print("No hay rutas válidas para calcular.")
             return None, None, None
       
        i_costo = Planificador.indice_mas_bajo(lista_costo)
        i_tiempo = Planificador.indice_mas_bajo(lista_tiempo)
        i_riesgo = Planificador.indice_mas_bajo(lista_riesgo)
        
        tupla_menor_costo=(lista_costo[i_costo],lista_tiempo[i_costo],lista_rutas[i_costo],lista_tipos[i_costo],lista_cantidad_vehiculos[i_costo], lista_riesgo[i_costo], carga)
        tupla_menor_tiempo=(lista_costo[i_tiempo],lista_tiempo[i_tiempo],lista_rutas[i_tiempo],lista_tipos[i_tiempo],lista_cantidad_vehiculos[i_tiempo], lista_riesgo[i_tiempo], carga)
        tupla_menor_riesgo=(lista_costo[i_riesgo],lista_tiempo[i_riesgo],lista_rutas[i_riesgo],lista_tipos[i_riesgo],lista_cantidad_vehiculos[i_riesgo], lista_riesgo[i_riesgo], carga)
        return tupla_menor_costo, tupla_menor_tiempo,tupla_menor_riesgo
    
    
    