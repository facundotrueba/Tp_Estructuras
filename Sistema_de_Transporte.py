
class Tipo_transporte:
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg): #lo de los costos hacer archivo csv CHEQUEAR LUCAS
        if velocidad_nominal <= 0:
            raise ValueError("La velocidad no puede ser negativa")
        if capacidad_carga <= 0:
            raise ValueError("La capacidad de carga no puede ser negativa")
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
        

#diccionario con cada clave siendo cada tipo y cada valor siendo una lista de rutas (lista de listas).
# Cada ruta es una lista de conexiones que hay entre los nodos. 


