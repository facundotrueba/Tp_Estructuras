import csv

'''
class Ciudad:
    pass

Buenos_Aires = Ciudad()
Azul = Ciudad()
Mar_del_Plata = Ciudad()
Zarate = Ciudad()
Junin = Ciudad()

grafo = {
    Buenos_Aires: [Azul, Junin, Mar_del_Plata,Zarate],
    Azul: [Mar_del_Plata, Junin, Buenos_Aires],
    Junin: [Azul,Buenos_Aires, Zarate],
    Zarate:[Buenos_Aires,Junin],
    Mar_del_Plata:[Buenos_Aires, Azul]
}
grafo = {
    "Buenos Aires": ["Azul", "Junin", "Mar del Plata","Zarate"],
    "Azul": ["Mardel Plata", "Junin", "Buenos Aires"],
    "Junin": ["Azul","Buenos Aires", "Zarate"],
    "Zarate":["Buenos Aires","Junin"],
    "Mar del Plata":["Buenos Aires", "Azul"]
}

rutas = encontrar_todas_las_rutas(grafo2, Buenos_Aires, Buenos_Aires)
for r in rutas:
    print(r)  

def construir_grafo():
    grafo = {}
    for conexiones in Conexion.conexiones_por_tipo.values():
        for conexion in conexiones:
            if conexion.origen not in grafo:
                grafo[conexion.origen] = []
            grafo[conexion.origen].append(conexion)
    return grafo



def encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual=None):
    if camino_actual is None:
        camino_actual = []

    rutas = []

    if not camino_actual:
        conexiones_posibles = grafo.get(nodo_inicio, [])
    else:
        ultimo_nodo = camino_actual[-1].destino
        if ultimo_nodo == nodo_fin:
            return [camino_actual]
        conexiones_posibles = grafo.get(ultimo_nodo, [])

    for conexion in conexiones_posibles:
        siguiente_nodo = conexion.destino
        if siguiente_nodo not in [c.destino for c in camino_actual] and (not camino_actual or conexion.origen == camino_actual[-1].destino):
            nuevas_rutas = encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual + [conexion])
            rutas.extend(nuevas_rutas)

    return rutas

grafo3 = {
    "Buenos Aires": ["Azul", "Junin"],
    "Azul": [, "Junin", "Buenos Aires"],
    "Junin": ["Azul","Buenos Aires"]
    
    
}
'''  '''
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

  
def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        if i and i[0].strip():
            Nodo(i[0].strip())
def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        restriccion = i[4] if len(i) > 4 and i[4] else None
        valor_restriccion = i[5] if len(i) > 5 and i[5] else None
        origen = Nodo.get_nombre(i[0])
        destino = Nodo.get_nombre(i[1])
        
        tipo = i[2].strip().lower() if len(i) > 2 else None
        if tipo not in Conexion.tipos:
            print(f"Tipo desconocido: '{tipo}'")
        ida = Conexion(origen, destino, tipo, i[3], restriccion, valor_restriccion)
        vuelta = Conexion(destino, origen, tipo, i[3], restriccion, valor_restriccion)
        


class Nodo:
    lista_nodos = []

    def __init__(self, nombre):
        self.nombre = nombre
        Nodo.lista_nodos.append(self)

    def __str__(self):
        return self.nombre

    @classmethod
    def get_nombre(cls, nombre):
        for nodo in cls.lista_nodos:
            if nodo.nombre == nombre:
                return nodo
        return None


   
class Conexion: 
    conexiones_por_tipo = {}
    tipos = ("fluvial", "aerea", "automotor","ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max" , "tipo", "prob_mal_tiempo"}
    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion):
        self.origen = origen
        self.destino = destino
        
        self.tipo = tipo.strip().lower()
        if self.tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
        self.distancia = float(distancia)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

        if self.tipo not in Conexion.conexiones_por_tipo:
            Conexion.conexiones_por_tipo[self.tipo] = {self}
        else:
            Conexion.conexiones_por_tipo[self.tipo].add(self)
        
    def __str__(self):
        return (f"De {self.origen} a {self.destino}. Tipo: {self.tipo}")
    
    def __eq__(self, other):
        return (self.origen == other.origen and self.destino == other.destino and self.tipo == other.tipo and self.distancia == other.distancia and self.restriccion == other.restriccion and self.valor_restriccion == other.valor_restriccion)

    def __hash__(self):
        return hash((self.origen, self.destino, self.tipo, self.distancia, self.restriccion, self.valor_restriccion))


def encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual=None):
    if camino_actual is None:
        camino_actual = []

    rutas = []

    if not camino_actual:
        conexiones_posibles = grafo.get(nodo_inicio, [])
    else:
        ultimo_nodo = camino_actual[-1].destino
        if ultimo_nodo == nodo_fin:
            return [camino_actual]
        conexiones_posibles = grafo.get(ultimo_nodo, [])

    for conexion in conexiones_posibles:
        # Nos aseguramos de que las conexiones se encadenen correctamente
        if not camino_actual or conexion.origen == camino_actual[-1].destino:

            # 🚧 Armamos una lista de nodos ya visitados de forma clara
            nodos_visitados = []
            if camino_actual:
                nodos_visitados.append(camino_actual[0].origen)
                for c in camino_actual:
                    nodos_visitados.append(c.destino)

            # ✅ Solo seguimos si el nodo destino no está en la lista de visitados
            if conexion.destino not in nodos_visitados:
                nuevas_rutas = encontrar_todas_las_rutas(
                    grafo, nodo_inicio, nodo_fin, camino_actual + [conexion]
                )
                rutas.extend(nuevas_rutas)

    return rutas




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


cargar_nodos("nodos.csv")
cargar_conexiones("conexiones.csv")
grafo = construir_grafo(Conexion.conexiones_por_tipo)




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
            tipos_en_ruta = set(c.tipo for c in ruta)

            print(f"  Ruta {i}:")
            for conexion in ruta:
                print(f"    {conexion}")

            if len(nodos_en_ruta) != len(set(nodos_en_ruta)):
                print("    Error: Se repite algún nodo en la ruta.")
            if len(tipos_en_ruta) > 1:
                print("    Error: Se mezclan tipos de transporte.")


testear_funciones(grafo,"Zarate","Mar_del_Plata")'''


''' 
def testear_funciones(grafo, nombre_origen, nombre_destino):
    origen = Sistema_de_Transporte.Nodo.get_nombre(nombre_origen)
    destino = Sistema_de_Transporte.Nodo.get_nombre(nombre_destino)

    if origen is None or destino is None:
        print("Origen o destino no existen.")
        return

    rutas_por_tipo = Sistema_de_Transporte.encontrar_todas_rutas(grafo, origen, destino)

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
import auxiliar
import Sistema_de_Transporte

grafo = auxiliar.inicializar_sistema("nodos.csv", "conexiones.csv")
#origen = Sistema_de_Transporte.Nodo.get_nombre("Buenos Aires")
#destino = Sistema_de_Transporte.Nodo.get_nombre("Mar del Plata")



Sistema_de_Transporte.testear_funciones(grafo, "Buenos_Aires", "Mar_del_Plata") #los nombres de nodos escribirlos tal cual estan en csv