class Itinerario:
    def __init__(self, id_solicitud, ruta, costo, tiempo, optimizacion, vehiculo, cantidad_vehiculos, carga):
        self.id_solicitud =id_solicitud
        self.ruta=ruta
        self.costo=costo
        self.tiempo=tiempo
        self.optimizacion= optimizacion
        self.vehiculo = vehiculo
        self.cantidad_vehiculos=cantidad_vehiculos
        self.carga=carga
    
        
    def mostrar_resumen(self):
        return f"Itinerario: {self.ruta} | cantidad de conexion: {len(self.ruta)} | Tiempo: {self.tiempo} min | Costo: ${self.costo}"

    