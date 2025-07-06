import math

import random
class Tipo_transporte:
    def __init__(self, velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg):
        if velocidad_nominal <= 0:
            raise ValueError("La velocidad no puede ser negativa")
        if capacidad_carga <= 0:
            raise ValueError("La capacidad de carga no puede ser negativa")
        self.velocidad_nominal=velocidad_nominal
        self.capacidad_carga=capacidad_carga
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg
    
    
    @staticmethod
    def obtener_tipo_vehiculo(vehiculo):
        if isinstance(vehiculo,Automotor):
            return "automotor"
        elif isinstance(vehiculo,Aerea):
            return "aerea"
        elif isinstance(vehiculo,Fluvial):
            return "fluvial"
        elif isinstance(vehiculo,Ferroviaria):
            return "ferroviaria"
        else:
            raise ValueError("Tipo de transporte no reconocido")
    
    @staticmethod
    def crear_vehiculo_base(tipo_transporte):
        tipo = tipo_transporte.lower()
        if tipo == "automotor":
            return Automotor()
        elif tipo == "aerea":
            return Aerea()
        elif tipo == "fluvial":
            return Fluvial()
        elif tipo == "ferroviaria":
            return Ferroviaria()
        else:
            raise ValueError("Tipo de transporte no reconocido.")
    
    
    def calcular_costo_variable(self, carga, ruta):
        costo_variable_total = self.costo_kg * carga
        return costo_variable_total



    @staticmethod
    def ajustar_vehiculo_por_conexion(conexion, tipo_transporte):
        tipo = tipo_transporte.lower()
        if tipo == "aerea":
            if getattr(conexion, 'restriccion', None) == 'prob_mal_tiempo':
                prob = float(getattr(conexion, 'valor_restriccion', 0))
                velocidad = Aerea.determinar_vel(prob)
                return Aerea(velocidad)
            else:
                return Aerea()
        elif tipo == "fluvial":
            valor_restriccion = getattr(conexion, 'valor_restriccion', '').lower()
            if valor_restriccion == "fluvial":
                return Fluvial(costo_fijo=500)
            elif valor_restriccion == "maritima":
                return Fluvial(costo_fijo=1500)
            else:
                return Fluvial()
        elif tipo == "ferroviaria":
            if getattr(conexion, 'restriccion', None) == 'velocidad_max':
                velocidad = min(100, float(getattr(conexion, 'valor_restriccion', 100)))
            else:
                velocidad = 100
            if conexion.distancia < 200:
                return Ferroviaria(velocidad, costo_km=20)
            else:
                return Ferroviaria(velocidad, costo_km=15)
        else:
            return None

        
    
    def cantidad_vehiculos(self, carga, ruta): 
        return math.ceil(carga / self.capacidad_carga)
            
    
    def calcular_costo(self,conexion, cantidad_vehiculos): 
        costo_km = self.costo_km
        costo_fijo = self.costo_fijo
        costo_total = (cantidad_vehiculos * (costo_fijo + costo_km * conexion.distancia)) 
        return costo_total
    
    
    def calcular_tiempo(self,conexion):
        distancia = conexion.distancia
        velocidad = self.velocidad_nominal
        return (distancia / velocidad)

    
    
    @staticmethod
    def calcular_costo_tiempo_riesgo(ruta,carga,tipo_transporte): #ruta es lista de conexiones. #ruta= [zarate->bsas, bsas->mdp] cada uno es un objeto conexion
        costo_total = 0
        tiempo_total = 0
        vehiculo = Tipo_transporte.crear_vehiculo_base(tipo_transporte)
        cantidad_vehiculos = vehiculo.cantidad_vehiculos(carga,ruta)
        costo_variable_total = vehiculo.calcular_costo_variable(carga,ruta)
        riesgo_ruta = 1
        for conexion in ruta:
            vehiculo_ajustado = Tipo_transporte.ajustar_vehiculo_por_conexion(conexion, tipo_transporte)
            if vehiculo_ajustado is not None:
                vehiculo = vehiculo_ajustado
            riesgo_ruta = riesgo_ruta * (1-conexion.riesgo)
            costo_total += vehiculo.calcular_costo(conexion,cantidad_vehiculos)
            tiempo_total += vehiculo.calcular_tiempo(conexion)
        
        riesgo_total = 1-((riesgo_ruta)**cantidad_vehiculos)
        
        costo_total += costo_variable_total
        return costo_total, tiempo_total, tipo_transporte, cantidad_vehiculos, riesgo_total



class Automotor(Tipo_transporte):
    def __init__(self,  velocidad_nominal=80, capacidad_carga= 30000, costo_fijo=30, costo_km= 5, costo_kg= 1):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

    
    def calcular_costo_variable(self, carga, ruta):
            costo_variable_total = 0
            capacidad_efectiva = self.capacidad_carga
            for conexion in ruta:
                if getattr(conexion, 'restriccion', None) == "peso_max":
                    valor = getattr(conexion, 'valor_restriccion', None)
                    if valor:
                        capacidad_efectiva = min(capacidad_efectiva, float(valor))
            carga_restante = carga
            while carga_restante > 0:
                carga_vehiculo = min(capacidad_efectiva, carga_restante)
                costo_kg = 2 if carga_vehiculo >= 15000 else 1
                costo_variable_total += carga_vehiculo * costo_kg
                carga_restante -= carga_vehiculo
            
            return costo_variable_total
    
    def cantidad_vehiculos(self, carga, ruta): #ruta es una lista de conexiones
            #carga es la carga que se quiere transportar, capacidad es el peso maximo del vehiculo
            cantidades_posibles=[]
            for conexion in ruta:
                restriccion = getattr(conexion, 'restriccion', None)
                valor_restriccion = getattr(conexion, 'valor_restriccion', None)
                if restriccion == "peso_max" and valor_restriccion is not None: #Si tiene la restriccion de peso maximo, entonces cada camion debe tener la minima entre el "peso maximo" y la capacidad del camion
                     max_peso=min(float(valor_restriccion),self.capacidad_carga)
                     cantidad = math.ceil(carga /max_peso)
                     cantidades_posibles.append(cantidad)
            if cantidades_posibles:
                return max(cantidades_posibles)
            return math.ceil(carga / self.capacidad_carga)
        
class Aerea(Tipo_transporte):
    def __init__(self, velocidad_nominal = 600, capacidad_carga = 5000, costo_fijo = 750, costo_km = 40, costo_kg = 10, velocidad_mal_tiempo = 400):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        self.velocidad_mal_tiempo = velocidad_mal_tiempo

    @staticmethod
    def determinar_vel(prob_mal_tiempo, velocidad_buen_tiempo = 600, velocidad_mal_tiempo = 400):
        if not 0 <= prob_mal_tiempo <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        if random.random() <= prob_mal_tiempo:
            return velocidad_mal_tiempo
        else:
            return velocidad_buen_tiempo


class Fluvial(Tipo_transporte):
    def __init__(self, velocidad_nominal = 40, capacidad_carga = 100000, costo_fijo = 500, costo_km = 15, costo_kg = 2):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)

class Ferroviaria(Tipo_transporte):
    def __init__(self, velocidad_nominal = 100, capacidad_carga = 150000, costo_fijo = 100, costo_km = 20, costo_kg = 3):
        super().__init__(velocidad_nominal, capacidad_carga, costo_fijo, costo_km, costo_kg)
        



