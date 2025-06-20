from collections import deque
class Solicitud_Transporte:
    cola_solicitudes = deque() 
    def __init__(self, id_carga, peso_kg, origen, destino):
        if peso_kg <= 0: #Validaciones
            raise ValueError("El peso debe ser mayor a cero.")
        if origen == destino:
            raise ValueError("El destino debe ser distinto del origen.")
        self.id_carga=id_carga
        self.peso_kg=peso_kg
        self.origen=origen
        self.destino=destino
        Solicitud_Transporte.cola_solicitudes.append(self)
    @classmethod
    def hay_solicitudes(cls):
        return len(cls.cola_solicitudes) > 0
