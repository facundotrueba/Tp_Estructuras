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
        descripcion_tramos = " → ".join(str(conex) for conex in self.ruta)
        horas = int(self.tiempo)
        minutos = int((self.tiempo - horas) * 60)
        print(f"Itinerario: {descripcion_tramos}\n Cantidad de conexiones: {len(self.ruta)}\n Tiempo total: {horas} h {minutos} m \n Costo total: ${self.costo}\n KPI optimizado: {self.optimizacion}")  # si tenés ese atributo

    
    