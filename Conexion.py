import Nodo
#DICCIONARIO: CLAVE 1 TIPO, CLAVE 2 NODO, CLAVE 3 DESTINO, lista (dist, restriccion, valor_restriccion)
class Conexion: 
    conexiones_por_tipo = {} #clave=tipo, valor=set de conexiones del tipo
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max", "tipo", "prob_mal_tiempo"}

    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion):

        if tipo not in Conexion.tipos:
            raise TypeError("El tipo de conexión es incorrecto.")
        self.origen = origen
        self.destino = destino
        self.tipo = tipo.strip().lower()
        self.distancia = float(distancia)
        if restriccion:
            restriccion = restriccion.strip().lower()
            if restriccion not in Conexion.restricciones_validas:
                raise ValueError(f"Restricción no válida: {restriccion}")
            self.restriccion = restriccion
            self.valor_restriccion = valor_restriccion
        else:
            self.restriccion = None
            self.valor_restriccion = None

        Nodo.Nodo.get_nombre(self.origen).tipos_disponibles.add(self.tipo)#agrega los tipos al nodo
        Nodo.Nodo.get_nombre(self.destino).tipos_disponibles.add(self.tipo)

        if self.tipo not in Conexion.conexiones_por_tipo:
            Conexion.conexiones_por_tipo[self.tipo] = {self}
        else:
            Conexion.conexiones_por_tipo[self.tipo].add(self)
            
    def __str__(self):
        return f"De {self.origen} a {self.destino}. Tipo: {self.tipo}"

    def __eq__(self, other):
        return (
            self.origen == other.origen and
            self.destino == other.destino and
            self.tipo == other.tipo and
            self.distancia == other.distancia and
            self.restriccion == other.restriccion and
            self.valor_restriccion == other.valor_restriccion
        )
        

    def __hash__(self): #Resolver! Puede que tengamos que cambiar la estructura
        return hash((self.origen, self.destino, self.tipo, self.distancia, self.restriccion, self.valor_restriccion))
