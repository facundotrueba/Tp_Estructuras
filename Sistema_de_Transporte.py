import csv
class Nodos:
    def __init__(self, nombre,capacidad, soporte_modos):
        self.nombre=nombre
        self.capacidad = capacidad
        self.soporte_modos=soporte_modos

class Conexion:  
    tipos = ("fluvial", "aereo", "terrestre","ferroviario")
    def __init__(self, inicio, destino, tipo, distancia):
        self.inicio=inicio
        self.destino=destino 
        if tipo not in Conexion.tipos:
            raise TypeError("El tipo de conexion es incorrecta")
        self.tipo=tipo #que la via sea una instancia de la clase medio transporte 
        self.distancia=distancia
        self.restricciones={}  #esto es un diccionario que tiene como clave el tipo de vehiculo y valor la restriccion especifica (ej: restriccion de volocidad de 300km/h para los automotres)
    @staticmethod
    def validar(tipo,restriccion,num): #tipo, aereo,fluvial,etc,restriccion velocidad max peso max, cantidad de peso max
        if restriccion == None:
            print("No hay ninguna restriccion")
        
        else:
          if tipo=="ferroviario":
              pass
           # if velocidad_nominal < num
           #         raise ValueError("execede la velocidad")
        

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
        cantidad = -(-peso // self.capacidad)  #cuantos vehiculos se necesitan para transportar esa carga
        costo= cantidad * (self.costo_fijo + self.costo_km * distancia + self.costo_kg * peso)
        return costo

    def calcular_tiempo(self, distancia):
        tiempo=distancia / self.velocidad
        return tiempo

class Automotor(Vehiculo):
    def __init__(self, tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        
    
    
class Aereo(Vehiculo):
  def __init__(self, tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
      super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
      
      

class Maritimo(Vehiculo):
    def __init__(self,tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        super().__init__(tipo, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)


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
        
        
        
def leer_csv(nombre_archivo):
    datos=[]
    try:
        with open(nombre_archivo, mode='r') as file:
            lector = csv.read(file)
            for fila in lector:
                datos.append(fila)
    except FileNotFoundError:
        print("Archivo no encontrado")