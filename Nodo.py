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