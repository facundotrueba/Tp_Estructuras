from collections import deque
import Nodo
import Leer
class Solicitud_Transporte:
    cola_solicitudes = deque() #Esto es una cola
    
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

    @staticmethod            
    def validar(fila):
        if len(fila) != 4:
            raise ValueError("La solicitud debe tener exactamente 4 campos: id_carga, peso_kg, origen, destino")

        id_carga, peso, origen, destino = [x.strip() for x in fila]

        # Validar ID duplicado en cola
        for solicitud in Solicitud_Transporte.cola_solicitudes:
            if solicitud.id_carga == id_carga:
                raise ValueError(f"Ya existe una solicitud con ID '{id_carga}'")

        # Validar peso
        peso = float(peso)
        if peso <= 0:
            raise ValueError("El peso debe ser un número positivo")   

        origen_nodo = Nodo.Nodo.get_nombre(origen)
        destino_nodo = Nodo.Nodo.get_nombre(destino)

        if origen_nodo is None:
            raise ValueError(f"El nodo de origen '{origen}' no existe.")
        if destino_nodo is None:
            raise ValueError(f"El nodo de destino '{destino}' no existe.")
        if origen_nodo == destino_nodo:
            raise ValueError("El nodo de origen y destino no pueden ser el mismo.")

        return id_carga, peso, origen_nodo, destino_nodo

    @staticmethod
    def cargar(nombre_archivo):
        try:
            datos = Leer.LectorCSV.leer_csv(nombre_archivo)
            Leer.LectorCSV.validar(datos, nombre_archivo)
        except ValueError as e:
            print(e)
            return
        i=1
        for fila in datos:
            if fila:
                try:
                    id_carga, peso, origen, destino = Solicitud_Transporte.validar(fila)
                    Solicitud_Transporte(id_carga, peso, origen, destino)
                except (ValueError, TypeError) as e:
                    print(f"Error al cargar solicitud: {e}")
                    i=0
        if i:
            print('Solicitudes cargadas exitosamente.')
    
    
            
            