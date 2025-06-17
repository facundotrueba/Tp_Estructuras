from collections import deque
import Planificador
class Solicitud_Transporte:
    cola_solicitudes = deque() #colacha ()
    def __init__(self, id_carga, peso_kg, origen, destino):
        if peso_kg <= 0: #Validaciones
            raise ValueError("El peso debe ser mayor a cero.")
        if origen == destino:
            raise ValueError("El destino debe ser distinto del origen.")
        self.id_carga=id_carga
        self.peso_kg=peso_kg
        self.origen=origen
        self.destino=destino
        Planificador.cola_solicitudes.append(self)