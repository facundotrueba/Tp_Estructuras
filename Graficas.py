import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import Sistema_de_Transporte
from collections import Counter


class Graficos:
    @staticmethod
    def calcular_arrays_distancia_tiempo_acumulados(vehiculo, ruta):
        n_pts = len(ruta) + 1
        distancias = np.empty(n_pts)
        tiempos = np.empty(n_pts)
        distancias[0] = tiempos[0] = 0
        distancia_acum = tiempo_acum = 0
        tipo_transporte = Sistema_de_Transporte.Tipo_transporte.obtener_tipo_vehiculo(vehiculo)

        for idx, conexion in enumerate(ruta, start=1):
            vehiculo_ajustado = Sistema_de_Transporte.Tipo_transporte.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_acum += vehiculo_ajustado.calcular_tiempo(conexion)
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
        
        distancias[0] = 0
        costo_acum = distancia_acum = 0
        
        costo_variable = vehiculo.calcular_costo_variable(carga,ruta)
        costos[0] = costo_variable
        for idx, conexion in enumerate(ruta, start=1):
            costo_fijo = vehiculo.calcular_costo(conexion, cantidad_vehiculos)
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
        
        tiempo_acum = costo_acum = 0
        tipo_transporte = Sistema_de_Transporte.Tipo_transporte.obtener_tipo_vehiculo(vehiculo)
        costo_variable = vehiculo.calcular_costo_variable(carga,ruta)
        tiempos[0] =  0
        costos[0] = costo_variable

        for idx, conexion in enumerate(ruta, start=1):
            vehiculo_ajustado = Sistema_de_Transporte.Tipo_transporte.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is None:
                vehiculo_ajustado = vehiculo
            tiempo_acum +=  vehiculo_ajustado.calcular_tiempo(conexion)
            costo_fijo =  vehiculo.calcular_costo(conexion, cantidad_vehiculos)
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
        print("imprimiendo distancia vs tiempo")
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Sistema_de_Transporte.Tipo_transporte.crear_vehiculo_base(tipo_transporte)
                distancias, tiempos = Graficos.calcular_arrays_distancia_tiempo_acumulados(vehiculo,ruta)
                plt.plot(tiempos, distancias, marker='o', label=f'Ruta{ruta_idx} ({tipo_transporte})')
                print(f"Ruta {ruta_idx}:")
                ruta_idx += 1
                for conexion in ruta: 
                    print(f"{conexion}")
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Distancia acumulada (km)")
        plt.title("Distancia vs. Tiempo - Todas las rutas")
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def graficar_costo_vs_distancia_todas_rutas(dic_rutas, carga):
        print("imprimiendo costo vs distancia")
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Sistema_de_Transporte.Tipo_transporte.crear_vehiculo_base(tipo_transporte)
                cantidad_vehiculos = vehiculo.cantidad_vehiculos(carga, ruta)
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
        print("imprimiendo costo vs tiempo")
        plt.figure(figsize=(10, 6))
        ruta_idx = 1
        for tipo_transporte, rutas in dic_rutas.items():
            for ruta in rutas:
                vehiculo = Sistema_de_Transporte.Tipo_transporte.crear_vehiculo_base(tipo_transporte)
                cantidad_vehiculos = vehiculo.cantidad_vehiculos(carga, ruta)
                tiempos, costos = Graficos.calcular_arrays_costo_tiempo_acumulado(vehiculo, ruta, cantidad_vehiculos, carga)
                plt.plot(tiempos, costos, marker='o', label=f'Ruta {ruta_idx} ({tipo_transporte})')
                ruta_idx += 1
        plt.xlabel("Tiempo acumulado (h)")
        plt.ylabel("Costo acumulado ($)")
        plt.title("Costo vs. Tiempo - Todas las rutas")
        plt.legend()
        plt.grid(True)
        plt.show()    




    @staticmethod
    def graficar_riesgo_total(diccionario_rutas, carga):
        print("Graficando riesgo total por ruta...")

        nombres_rutas = []
        valores_riesgo = []

        idx = 1
        for tipo, rutas in diccionario_rutas.items():
            for ruta in rutas:
                _, _, _, _, riesgo_total = Sistema_de_Transporte.Tipo_transporte.calcular_costo_tiempo_riesgo(
                    ruta, carga, tipo)
                nombre = f"Ruta {idx} ({tipo})"
                nombres_rutas.append(nombre)
                valores_riesgo.append(riesgo_total)
                idx += 1

        colores = cm.get_cmap('tab10', len(valores_riesgo))(np.arange(len(valores_riesgo)))

        plt.figure(figsize=(12, 6))
        plt.bar(nombres_rutas, valores_riesgo, color=colores)
        plt.xlabel("Ruta")
        plt.ylabel("Riesgo Total")
        plt.title("Riesgo Total por Ruta")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    
    
    @staticmethod
    def plot_conexiones_mas_usadas(lista_itinerarios, top_n=None):
        cnt = Counter()
        nodo = lista_itinerarios.cabeza
        while nodo:
            for c in nodo.itinerario.ruta:
                key = f"{c.origen}→{c.destino}"
                cnt[key] += 1
            nodo = nodo.siguiente

        comunes    = cnt.most_common(top_n)
        etiquetas  = [c[0] for c in comunes]
        valores    = [c[1] for c in comunes]

        plt.figure(figsize=(10,6))
        plt.bar(etiquetas, valores)
        plt.xticks(rotation=45, ha="right")

        plt.title("Tramos Más Transitados")
        
        max_y = max(valores, default=0)
        plt.yticks(range(0, max_y+1))
       
        plt.ylabel("Número de recorridos")
        plt.tight_layout()
        plt.show()

  