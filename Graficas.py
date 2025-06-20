import matplotlib.pyplot as plt
import numpy as np
import Planificador

class Graficos:
    """
    @staticmethod
    def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
        n_pts = len(ruta) + 1 #Sumo 1 para que el punto inicial (0,0)
        distancias   = np.empty(n_pts) #Creo arreys vacios
        tiempos      = np.empty(n_pts)
        distancias[0] = 0
        tiempos[0]    = 0
        distancia_acum = 0
        tiempo_acum    = 0
        tipo_transporte = Planificador.Planificador.obtener_tipo_vehiculo(vehiculo)
        for idx, conexion in enumerate(ruta, start=1):# empezamos el enumerate en 1
            vehiculo_ajustado = Planificador.Planificador.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_acum  += Planificador.Planificador.calcular_tiempo(conexion, vehiculo_ajustado)
            distancia_acum += conexion.distancia
            distancias[idx] = distancia_acum
            tiempos[idx]    = tiempo_acum

        return distancias, tiempos

    @staticmethod
    def graficar_distancia_vs_tiempo(vehiculo, ruta):
        distancias, tiempos = Graficos.calcular_arrays_distancia_tiempo_acumulados(vehiculo,ruta) #Calculamos los arrays
        print("Mostrando grafico: Distancia Acumulada vs. Tiempo Acumulado")
        plt.plot(tiempos, distancias, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()
   
    @staticmethod
    def calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos,carga):
        n_pts = len(ruta) + 1 #Sumo 1 para que el punto inicial (0,0)
        costos = np.empty(n_pts)
        distancias = np.empty(n_pts)
        costos[0]= 0
        distancias[0] = 0
        costo_acum = 0
        distancia_acum= 0
        costo_variable = Planificador.Planificador.calcular_costo_variable(ruta, vehiculo, carga)
        for idx, conexion in enumerate(ruta, start=1): # llenamos desde el índice 1
            costo_fijo = Planificador.Planificador.calcular_costo(conexion, cantidad_vehiculos,vehiculo)
            costo_acum += costo_fijo
            distancia_acum += conexion.distancia
            costos[idx] = costo_acum + costo_variable
            distancias[idx] = distancia_acum
        return costos, distancias

    @staticmethod
    def graficar_costo_vs_distancia( vehiculo, ruta, cantidad_vehiculos, carga):
        costos, distancias = Graficos.calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos, carga)
        print("Mostrando grafico: Costo Acumulado vs. Distancia Acumulada")
        plt.plot(distancias, costos, marker="o")
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos,carga):
        n_pts  = len(ruta) + 1 #Sumo 1 para que el punto inicial (0,0)
        tiempos= np.empty(n_pts)
        costos = np.empty(n_pts)
        tiempos[0] = 0 
        costos[0]  = 0
        tiempo_acum = 0
        costo_acum  = 0
        tipo_transporte = Planificador.Planificador.obtener_tipo_vehiculo(vehiculo)
        costo_variable = Planificador.Planificador.calcular_costo_variable(ruta, vehiculo, carga)
        for idx, conexion in enumerate(ruta, start=1): # llenamos desde el índice 1

            vehiculo_ajustado = Planificador.Planificador.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
        
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_i= Planificador.Planificador.calcular_tiempo(conexion, vehiculo_ajustado)
            
            costo_fijo= Planificador.Planificador.calcular_costo(conexion, cantidad_vehiculos, vehiculo)
            tiempo_acum += tiempo_i
            costo_acum += costo_fijo
            tiempos[idx] = tiempo_acum
            costos[idx] = costo_acum + costo_variable

        return tiempos, costos
    
    @staticmethod
    def graficar_costo_vs_tiempo(vehiculo, ruta, cantidad_vehiculos,carga):
        costos, tiempos = Graficos.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos,carga)
        print("Mostrando grafico: Costo Acumulado vs. Tiempo Acumulado")
        plt.plot(tiempos, costos, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo Acumulado vs. Tiempo Acumulado")
        plt.grid(True)
        plt.show()
        """
    @staticmethod
    def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
        n_pts = len(ruta) + 1
        distancias = np.empty(n_pts)
        tiempos = np.empty(n_pts)
        distancias[0] = tiempos[0] = 0
        distancia_acum = tiempo_acum = 0
        tipo_transporte = Planificador.Planificador.obtener_tipo_vehiculo(vehiculo)

        for idx, conexion in enumerate(ruta, start=1):
            vehiculo_ajustado = Planificador.Planificador.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_acum += Planificador.Planificador.calcular_tiempo(conexion, vehiculo_ajustado)
            distancia_acum += conexion.distancia
            tiempos[idx] = tiempo_acum
            distancias[idx] = distancia_acum

        return distancias, tiempos

    @staticmethod
    def graficar_distancia_vs_tiempo(vehiculo, ruta):
        distancias, tiempos = Graficos.calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta)
        print("Mostrando gráfico: Distancia Acumulada vs. Tiempo Acumulado")
        plt.plot(tiempos, distancias, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia vs. Tiempo")
        plt.grid(True)
        plt.show()

    @staticmethod
    def calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos, carga):
        n_pts = len(ruta) + 1
        costos = np.empty(n_pts)
        distancias = np.empty(n_pts)
        costos[0] = distancias[0] = 0
        costo_acum = distancia_acum = 0
        costo_variable = Planificador.Planificador.calcular_costo_variable(ruta, vehiculo, carga)

        for idx, conexion in enumerate(ruta, start=1):
            costo_fijo = Planificador.Planificador.calcular_costo(conexion, cantidad_vehiculos, vehiculo)
            costo_acum += costo_fijo
            distancia_acum += conexion.distancia
            costos[idx] = costo_acum + costo_variable
            distancias[idx] = distancia_acum

        return costos, distancias

    @staticmethod
    def graficar_costo_vs_distancia(vehiculo, ruta, cantidad_vehiculos, carga):
        costos, distancias = Graficos.calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos, carga)
        print("Mostrando gráfico: Costo Acumulado vs. Distancia Acumulada")
        plt.plot(distancias, costos, marker="o")
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo vs. Distancia")
        plt.grid(True)
        plt.show()

    @staticmethod
    def calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos, carga):
        n_pts = len(ruta) + 1
        tiempos = np.empty(n_pts)
        costos = np.empty(n_pts)
        tiempos[0] = costos[0] = 0
        tiempo_acum = costo_acum = 0
        tipo_transporte = Planificador.Planificador.obtener_tipo_vehiculo(vehiculo)
        costo_variable = Planificador.Planificador.calcular_costo_variable(ruta, vehiculo, carga)

        for idx, conexion in enumerate(ruta, start=1):
            vehiculo_ajustado = Planificador.Planificador.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_acum += Planificador.Planificador.calcular_tiempo(conexion, vehiculo_ajustado)
            costo_fijo = Planificador.Planificador.calcular_costo(conexion, cantidad_vehiculos, vehiculo)
            costo_acum += costo_fijo
            tiempos[idx] = tiempo_acum
            costos[idx] = costo_acum + costo_variable

        return tiempos, costos

    @staticmethod
    def graficar_costo_vs_tiempo(vehiculo, ruta, cantidad_vehiculos, carga):
        tiempos, costos = Graficos.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos, carga)
        print("Mostrando gráfico: Costo Acumulado vs. Tiempo Acumulado")
        plt.plot(tiempos, costos, marker="o")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo vs. Tiempo")
        plt.grid(True)
        plt.show()


    @staticmethod
    def graficar_distancia_vs_tiempo_todas_rutas(dic_rutas):
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Planificador.Planificador.crear_vehiculo_base(tipo_transporte)
                distancias, tiempos = Graficos.calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta)
                plt.plot(tiempos, distancias, marker='o', label=f'Ruta {ruta_idx} ({tipo_transporte})')
                ruta_idx += 1
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia vs. Tiempo - Todas las rutas")
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def graficar_costo_vs_distancia_todas_rutas(dic_rutas, carga):
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Planificador.Planificador.crear_vehiculo_base(tipo_transporte)
                cantidad_vehiculos = Planificador.Planificador.cantidad_vehiculos(ruta, vehiculo, carga)
                costos, distancias = Graficos.calcular_arrays_costo_distancia_acumulada(vehiculo, ruta, cantidad_vehiculos, carga)
                plt.plot(distancias, costos, marker='o', label=f'Ruta {ruta_idx} ({tipo_transporte})')
                ruta_idx += 1
        plt.xlabel("Distancia acumulada (km)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo vs. Distancia - Todas las rutas")
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def graficar_costo_vs_tiempo_todas_rutas(dic_rutas, carga):
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Planificador.Planificador.crear_vehiculo_base(tipo_transporte)
                cantidad_vehiculos = Planificador.Planificador.cantidad_vehiculos(ruta, vehiculo, carga)
                tiempos, costos = Graficos.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos, carga)
                plt.plot(tiempos, costos, marker='o', label=f'Ruta {ruta_idx} ({tipo_transporte})')
                ruta_idx += 1
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo vs. Tiempo - Todas las rutas")
        plt.legend()
        plt.grid(True)
        plt.show()    