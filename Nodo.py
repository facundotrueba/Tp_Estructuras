import Leer
class Nodo:
    lista_nodos = []
    def __init__(self, nombre):
        self.nombre = nombre
        Nodo.lista_nodos.append(self)
        self.tipos_disponibles = set()#almacena el tipo disponible de nodo
        
    def __str__(self):
        return self.nombre

    @classmethod
    def get_nombre(cls, nombre):
        if not isinstance(nombre, str):
            return None
        nombre = nombre.strip().lower()
        for nodo in cls.lista_nodos:
            if nodo.nombre.strip().lower() == nombre:
                return nodo
        return None
    @staticmethod
    def validar(entrada):
        if not isinstance(entrada, str):
            raise TypeError("El nombre del nodo debe ser un string.")
        nombre = entrada.strip().lower()
        if nombre == "":
            raise ValueError("El nombre del nodo no puede estar vacío.")
        if Nodo.get_nombre(nombre) is not None:
            raise ValueError(f"El nodo '{nombre}' ya fue cargado.")
        return nombre
    @staticmethod
    def cargar(nombre_archivo):
        try:
            datos = Leer.LectorCSV.leer_csv(nombre_archivo)
            Leer.LectorCSV.validar(datos, nombre_archivo)
        except ValueError as e:
            print(e)
            return
        i= 1
        for fila in datos:
            if fila: 
                try:
                    nombre = Nodo.validar(fila[0])
                    Nodo(nombre)
                except (TypeError, ValueError) as e:
                    print(f"Error al cargar nodo '{fila[0].lower()}': {e}")
                    i = 0
        if i:
            print('Nodos cargados exitosamente.')            
                
