import matplotlib.pyplot as plt
import numpy as np
import Planificador

class Graficos:
    @staticmethod
    def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
        n = len(ruta)
        distancias = np.empty(n)
        distancias[i] = distancia_acum
        
        tiempos = np.empty(n)
        distancia_acum = 0
        tiempo_acum = 0

        for i, conexion in enumerate(ruta):
            distancia_acum += conexion.distancia
            tiempo_conexion = Planificador.calcular_tiempo(conexion, vehiculo)
            tiempo_acum += tiempo_conexion
            distancias[i] = distancia_acum
            tiempos[i] = tiempo_acum
        return distancias, tiempos
    
    def graficar_distancia_vs_tiempo(self, vehiculo, ruta):
        distancias, tiempos = self.calcular_arrays_distancia_tiempo_acumulados(vehiculo,ruta)
        print("Mostrando grafico: Distancia Acumulada vs. Tiempo Acumulado")
        plt.plot(tiempos, distancias, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()
   
    @staticmethod
    def calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos, carga):
        n = len(ruta)
        costos = np.empty(n)
        distancias = np.empty(n)
        costo_acum = 0
        distancia_acum = 0
        for i, conexion in enumerate(ruta):
            costo_conexion = Planificador.calcular_costo(conexion, cantidad_vehiculos, vehiculo, carga)
            costo_acum += costo_conexion
            distancia_acum += conexion.distancia
            costos[i] = costo_acum
            distancias[i] = distancia_acum
        return costos, distancias

    def graficar_costo_vs_distancia(self, vehiculo, ruta):
        costos, distancias = self.calcular_arrays_costo_distancia_acumulada(vehiculo, ruta)
        print("Mostrando grafico: Costo Acumulado vs. Distancia Acumulada")
        plt.plot(distancias, costos, marker="o")
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.grid(True)
        plt.show()
    
    def calcular_arrays_costo_tiempo_acumulado(self, vehiculo, ruta, cantidad_vehiculos, ):
        n=len(ruta)
        costos = np.empty(n)
        tiempos = np.empty(n)
        costo_acum = 0
        tiempo_acum = 0
        for i, conexion in enumerate(ruta):
            costo_conexion = Planificador.calcular_costo(conexion, cantidad_vehiculos, vehiculo, self.carga)
            costo_acum += costo_conexion
            tiempo_conexion = Planificador.calcular_tiempo(conexion, vehiculo)
            tiempo_acum += tiempo_conexion
            costos[i] = costo_acum
            tiempos[i] = tiempo_acum
        return np.array(costos), np.array(tiempos)
    
    @staticmethod
    def graficar_costo_vs_tiempo(self, vehiculo, ruta):
        costos, tiempos = self.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta)
        print("Mostrando grafico: Costo Acumulado vs. Tiempo Acumulado")
        plt.plot(tiempos, costos, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()