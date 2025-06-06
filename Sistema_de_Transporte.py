import csv
import math

class Planificador: #se instancia MUCHAS VECES. UN PLANIFICADOR POR CADA SOLICITUD.(segun lo que dice ne la consigna en objetivo general)
    '''
    metodos:
    encontrar rutas

    calcular 



    
    '''


#self.nodos["Buenos Aires"].agregarConexion(conexion)

class Nodos:
    #almacenar nodos
    #almacenar conexiones
    lista_nodos = []
    def __init__(self, nombre):
        self.nombre=nombre
    #self.conexiones
        
    
    
#DICCIONARIO: CLAVE 1 TIPO, CLAVE 2 NODO, CLAVE 3 DESTINO, lista (dist, restriccion, valor_restriccion)
class Conexion: 
    conexiones_por_tipo = {}
    tipos = ("fluvial", "aerea", "automotor","ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max" , "tipo", "prob_mal_tiempo"}
    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion):
        self.origen = origen
        self.destino = destino
        if tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
        self.tipo = tipo
        self.distancia = float(distancia)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

        # Actualiza el diccionario de clase
       if tipo not in Conexion.conexiones_por_tipo:
            Conexion.conexiones_por_tipo[tipo] = {self}
        else:
            Conexion.conexiones_por_tipo[tipo].add(self)
        
    def __str__(self):
        return (f"De {self.origen} a {self.destino}. Tipo: {self.tipo}")
    
    def __eq__(self, other):
    def __hash__(self): #el gordo me dice que esta mal tener eq y no tener hash, preguntarle a lucas.
        return hash((self.origen, self.destino, self.tipo, self.distancia, self.restriccion, self.valor_restriccion))
        if not isinstance(other, Conexion):
            return False
        return (self.origen == other.origen and
                self.destino == other.destino and
                self.tipo == other.tipo and
                self.distancia == other.distancia and
                self.restriccion == other.restriccion and
                self.valor_restriccion == other.valor_restriccion)
    
    ''' def __init__(self, inicio, destino, tipo, distancia , restriccion=None,valor_restriccion = None):
        if restriccion == None:                                 
            self.inicio=inicio
            self.destino=destino 
            if tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
            self.tipo=tipo #que la via sea una instancia de la clase medio transporte 
            self.distancia=distancia
            
            # return("No hay ninguna restriccion") (init no puede devolver un str)
        else:de
            self.inicio=inicio
            self.destino=destino 
            if tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
            self.tipo=tipo #que la via sea una instancia de la clase medio transporte 
            self.distancia=distancia
            self.restriccion = restriccion 
            self.valor_restriccion = valor_restriccion
            Conexion.conexiones.append(self) '''

    def __str__(self):
            return f"Inicio:{self.inicio}, Destino:{self.destino}"
    def getConexion(inicio, destino,tipo_transporte):
        for conexion in Conexion.conexiones:
            if (conexion.inicio == inicio and conexion.destino == destino and conexion.tipo==tipo_transporte)or(conexion.inicio == destino and conexion.destino == inicio and conexion.tipo==tipo_transporte):
                return conexion

        

class Vehiculo:
    def __init__(self, tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg): #lo de los costos hacer archivo csv CHEQUEAR LUCAS
        self.tipo=tipo
        if velocidad_nominal<= 0:
            ValueError("La velocidad no puede ser negativa")
        if capacidad_carga<= 0:
            ValueError("La capacidad de carga no puede ser negativa")
        self.velocidad_nominal=velocidad_nominal
        self.capacidad_carga=capacidad_carga
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg
    
    def calcular_costo(self, distancia, peso): #funcion para calcular el costo de un tipo de vehiculo especifico para un tramo especifico
        cantidad = math.ceil(peso / self.capacidad_carga)  #cuantos vehiculos se necesitan para transportar esa carga
        costo_total= cantidad * (self.costo_fijo + self.costo_km * distancia + self.costo_kg * peso)
        return costo_total

    def calcular_tiempo(self, distancia):
        tiempo= distancia / self.velocidad
        return tiempo

class Automotor(Vehiculo):
    def __init__(self, tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        
    
    
class Aereo(Vehiculo):
  def __init__(self, tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
      super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
      
      

class Fluvial(Vehiculo):
    def __init__(self,tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)



#DICCIONARIO ID: SELF
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
            

    def cargar_conexiones_csv(ruta_archivo):
        with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                origen = fila['origen']
                destino = fila['destino']
                tipo = fila['tipo']
                distancia = float(fila['distancia_km'])

                restriccion = fila['restriccion'] if fila['restriccion'] else None
                valor_restriccion = fila['valor_restriccion']
                if valor_restriccion :  #Falta validar esto bien
                    try:
                        valor_restriccion = float(valor_restriccion)
                    except ValueError:
                        pass  # Si es texto como "maritimo"
                else:
                    valor_restriccion = 0

                Conexion(origen, destino, tipo, distancia, restriccion, valor_restriccion)
                
                

    



        
        
def calcular_costos_tiempo(recorrido,tipo_transporte,peso):
    for i in range(len(recorrido)-1):
        inicio = i
        destino = i+1
        conexion = Conexion.getConexion(recorrido[inicio], recorrido[destino],tipo_transporte)
        distancia = conexion.distancia
        costo_total += Vehiculo.calcular_costo(distancia,peso)
        tiempo_total += Vehiculo.calcular_tiempo(distancia)
    return costo_total,tiempo_total

def encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual=None):
    if camino_actual is None:
        camino_actual = []

    rutas = []

    # Si no hay ninguna conexión en el camino aún, estamos empezando
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