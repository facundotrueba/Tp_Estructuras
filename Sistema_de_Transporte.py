import csv
import math

class Planificador: #se instancia una vez
    '''
    metodos:
    encontrar rutas

    calcular 



    
    '''


#self.nodos["Buenos Aires"].agregarConexion(conexion)

class Nodos:
    #almacenar nodos
    #almacenar conexiones

    def __init__(self, nombre):
        self.nombre=nombre
    #self.conexiones
        
    
    
#DICCIONARIO: CLAVE 1 TIPO, CLAVE 2 NODO, CLAVE 3 DESTINO, lista (dist, restriccion, valor_restriccion)
class Conexion: #Crear un diccionario cuyas claves sean los inicios y dentro del mismo tenga el origen y el tipo (asi podemos buscar mas facil conexiones)
    conexiones = []
    tipos = ("fluvial", "aereo", "terrestre","ferroviario")
    restricciones_validas = {"velocidad_max", "peso_max" , "tipo", "prob_mal_tiempo"}
    def __init__(self, inicio, destino, tipo, distancia , restriccion=None,valor_restriccion = None):
        if restriccion == None:                                 
            self.inicio=inicio
            self.destino=destino 
            if tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
            self.tipo=tipo #que la via sea una instancia de la clase medio transporte 
            self.distancia=distancia
            Conexion.conexiones.append(self)
            return("No hay ninguna restriccion")
        else:
            self.inicio=inicio
            self.destino=destino 
            if tipo not in Conexion.tipos:
                raise TypeError("El tipo de conexion es incorrecta")
            self.tipo=tipo #que la via sea una instancia de la clase medio transporte 
            self.distancia=distancia
            self.restriccion = restriccion 
            self.valor_restriccion = valor_restriccion
            Conexion.conexiones.append(self)

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
    def __init__(self, id_carga, peso_kg, origen, destino):
        if peso_kg <= 0: #Validaciones
            raise ValueError("El peso debe ser mayor a cero.")
        if origen == destino:
            raise ValueError("El destino debe ser distinto del origen.")
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

    
    def leer_csv(nombre_archivo): #NO TERMINADO
        datos=[]
        try:
            with open(nombre_archivo, mode='r') as file:
                lector = csv.read(file)
                for fila in lector:
                    datos.append(fila)
        except FileNotFoundError:
            print("Archivo no encontrado")
            


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
                
                

    

def encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual=None):
    if camino_actual is None:
        camino_actual = []

    camino_actual = camino_actual + [nodo_inicio]

    if nodo_inicio == nodo_fin:
        return [camino_actual]

    rutas = []
    for vecino in grafo.get(nodo_inicio,[]):
        if vecino not in camino_actual:
            nuevas_rutas = encontrar_todas_las_rutas(grafo, vecino, nodo_fin, camino_actual)
            rutas.extend(nuevas_rutas)
    return rutas
grafo = {
    "Buenos Aires": ["Azul", "Junin", "Mar del Plata","Zarate"],
    "Azul": ["Mar del Plata", "Junin", "Buenos Aires"],
    "Junin": ["Azul","Buenos Aires", "Zarate"],
    "Zarate":["Buenos Aires","Junin"],
    "Mar del Plata":["Buenos Aires", "Azul"]
}

rutas = encontrar_todas_las_rutas(grafo, "Buenos Aires", "Mar del Plata")
for r in rutas:
    print(r)               
        
        
def calcular_costos_tiempo(recorrido,tipo_transporte,peso):
    for i in range(len(recorrido)-1):
        inicio = i
        destino = i+1
        conexion = Conexion.getConexion(recorrido[inicio], recorrido[destino],tipo_transporte)
        distancia = conexion.distancia
        costo_total += Vehiculo.calcular_costo(distancia,peso)
        tiempo_total += Vehiculo.calcular_tiempo(distancia)
    return costo_total,tiempo_total
