import Sistema_de_Transporte
import csv
import matplotlib.pyplot as plt
import numpy as np

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
        if i and i[0].strip().lower():
            Sistema_de_Transporte.Nodo(i[0].strip().lower())
            
def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        restriccion = i[4] if len(i) > 4 and i[4] else None
        valor_restriccion = i[5] if len(i) > 5 and i[5] else None

        origen = Sistema_de_Transporte.Nodo.get_nombre(i[0])
        destino = Sistema_de_Transporte.Nodo.get_nombre(i[1])

        tipo = i[2].strip().lower() if len(i) > 2 else None

        if tipo not in Sistema_de_Transporte.Conexion.tipos:
            print(f"Tipo desconocido: '{tipo}'")

        
        
        Sistema_de_Transporte.Conexion(origen, destino, tipo, i[3], restriccion, valor_restriccion)
        Sistema_de_Transporte.Conexion(destino, origen, tipo, i[3], restriccion, valor_restriccion)

def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        Sistema_de_Transporte.Solicitud_Transporte(i[0], i[1], i[2], i[3])

def inicializar_sistema(nodos_path, conexiones_path):
    cargar_nodos(nodos_path)
    cargar_conexiones(conexiones_path)
    grafo = Sistema_de_Transporte.construir_grafo(Sistema_de_Transporte.Conexion.conexiones_por_tipo)
    return grafo


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
            tiempo_conexion = Sistema_de_Transporte.Planificador.calcular_tiempo(conexion, vehiculo)
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
            costo_conexion = Sistema_de_Transporte.Planificador.calcular_costo(conexion, self.cantidad_vehiculos, vehiculo, self.carga)
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
