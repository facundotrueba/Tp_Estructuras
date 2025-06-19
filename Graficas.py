import matplotlib.pyplot as plt
import numpy as np
import Planificador

class Graficos:
    @staticmethod
    # def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
    #     n = len(ruta)
    #     distancias = np.empty(n)
    #     tiempos    = np.empty(n)

    #     distancia_acum = 0
    #     tiempo_acum    = 0

    #     for i, conexion in enumerate(ruta):
    #         distancia_acum += conexion.distancia
    #         tiempo_conexion = Planificador.Planificador.calcular_tiempo(conexion, vehiculo)
    #         tiempo_acum    += tiempo_conexion

    #         distancias[i] = distancia_acum
    #         tiempos[i]    = tiempo_acum

    #     return distancias, tiempos
    @staticmethod
    def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
        # un punto extra para (0,0)
        n_pts = len(ruta) + 1

        distancias   = np.empty(n_pts)
        tiempos      = np.empty(n_pts)

        # punto inicial
        distancias[0] = 0
        tiempos[0]    = 0

        distancia_acum = 0
        tiempo_acum    = 0

        # empezamos el enumerate en 1
        for idx, conexion in enumerate(ruta, start=1):
            distancia_acum += conexion.distancia
            tiempo_acum    += Planificador.Planificador.calcular_tiempo(conexion, vehiculo)

            distancias[idx] = distancia_acum
            tiempos[idx]    = tiempo_acum

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
    def calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos):
        # un punto extra para (0,0)
        n_pts     = len(ruta) + 1
        costos    = np.empty(n_pts)
        distancias= np.empty(n_pts)

        # punto inicial
        costos[0]     = 0
        distancias[0] = 0

        costo_acum     = 0
        distancia_acum = 0

        # llenamos desde el índice 1
        for idx, conexion in enumerate(ruta, start=1):
            costo_i = Planificador.Planificador.calcular_costo(
                conexion,
                cantidad_vehiculos,
                vehiculo
            )
            costo_acum     += costo_i
            distancia_acum += conexion.distancia

            costos[idx]     = costo_acum
            distancias[idx] = distancia_acum

        return costos, distancias

    def graficar_costo_vs_distancia(self, vehiculo, ruta, cantidad_vehiculos):
        costos, distancias = self.calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos)
        print("Mostrando grafico: Costo Acumulado vs. Distancia Acumulada")
        plt.plot(distancias, costos, marker="o")
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos):
        # un punto extra para (0,0)
        n_pts  = len(ruta) + 1
        tiempos= np.empty(n_pts)
        costos = np.empty(n_pts)

        # punto inicial
        tiempos[0] = 0
        costos[0]  = 0

        tiempo_acum = 0
        costo_acum  = 0

        # llenamos desde el índice 1
        for idx, conexion in enumerate(ruta, start=1):
            dt = Planificador.Planificador.calcular_tiempo(conexion, vehiculo)
            dc = Planificador.Planificador.calcular_costo(
                conexion,
                cantidad_vehiculos,
                vehiculo
            )

            tiempo_acum   += dt
            costo_acum    += dc

            tiempos[idx]  = tiempo_acum
            costos[idx]   = costo_acum

        return tiempos, costos
    
    def graficar_costo_vs_tiempo(self, vehiculo, ruta, cantidad_vehiculos):
        costos, tiempos = self.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos)
        print("Mostrando grafico: Costo Acumulado vs. Tiempo Acumulado")
        plt.plot(tiempos, costos, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()