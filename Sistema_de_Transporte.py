
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import Planificador
import Nodo

class Tipo_transporte:
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg): #lo de los costos hacer archivo csv CHEQUEAR LUCAS
        if velocidad_nominal <= 0:
            ValueError("La velocidad no puede ser negativa")
        if capacidad_carga <= 0:
            ValueError("La capacidad de carga no puede ser negativa")
        self.velocidad_nominal=velocidad_nominal
        self.capacidad_carga=capacidad_carga
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg
    


class Automotor(Tipo_transporte): # el codigo va a funcionar de tal manera que si se arranca una ruta con 8 automotores, Si se puede despues hacer con 10 automotores y despues 8 de vuelta en otra conexion
    def __init__(self,  velocidad_nominal=80, capacidad_carga= 30000, costo_fijo=30, costo_km= 5, costo_kg= 1):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

    
class Aerea(Tipo_transporte):
    def __init__(self, velocidad_nominal = 600, capacidad_carga = 5000, costo_fijo = 750, costo_km = 40, costo_kg = 10, velocidad_mal_tiempo = 400):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        self.velocidad_mal_tiempo = velocidad_mal_tiempo


class Fluvial(Tipo_transporte):
    def __init__(self, velocidad_nominal = 40, capacidad_carga = 100000, costo_fijo = 500, costo_km = 15, costo_kg = 2):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

class Ferroviaria(Tipo_transporte):
    def __init__(self, velocidad_nominal = 100, capacidad_carga = 150000, costo_fijo = 100, costo_km = 20, costo_kg = 3):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        



        

    
#ex-tobi: del dicc de encontrar_todas_rutas tengo que llamar a calcular_costos_tiempo para que le calcule el costo y tiempo a cada una de esas rutas. de todos esos tiemposy costos tengo que buscar la ruta con tiempo y costo mas bajo. 
#diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).
# Cada ruta es una lista de conexiones que hay entre los nodos. 

def testear_funciones(grafo, nombre_origen, nombre_destino):
    origen = Nodo.Nodo.get_nombre(nombre_origen)
    destino = Nodo.Nodo.get_nombre(nombre_destino)

    if origen is None or destino is None:
        print("Origen o destino no existen.")
        return

    rutas_por_tipo = Planificador.encontrar_todas_rutas(grafo, origen, destino)

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

