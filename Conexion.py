import Nodo
import Leer
#DICCIONARIO: CLAVE 1 TIPO, CLAVE 2 NODO, CLAVE 3 DESTINO, lista (dist, restriccion, valor_restriccion)
class Conexion: 
    conexiones_por_tipo = {} #clave=tipo, valor=set de conexiones del tipo
    tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
    restricciones_validas = {"velocidad_max", "peso_max", "tipo", "prob_mal_tiempo"}

    def __init__(self, origen, destino, tipo, distancia, restriccion, valor_restriccion,riesgo):   ###

        if tipo not in Conexion.tipos:
            raise TypeError("El tipo de conexión es incorrecto.")
        self.origen = origen
        self.destino = destino
        self.tipo = tipo.strip().lower()
        self.distancia = float(distancia)
        self.riesgo = riesgo              ###
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
            
    @classmethod
    def get_conexion(cls, origen, destino, tipo, distancia, restriccion=None, valor_restriccion=None, riesgo=0):
        tipo = tipo.strip().lower()
        if tipo not in cls.conexiones_por_tipo:
            return None

        for conexion in cls.conexiones_por_tipo[tipo]:
            if (
                conexion.origen == origen and
                conexion.destino == destino and
                conexion.tipo == tipo and
                conexion.distancia == float(distancia) and
                conexion.restriccion == (restriccion.strip().lower() if restriccion else None) and
                conexion.valor_restriccion == (float(valor_restriccion) if valor_restriccion is not None else None) and
                conexion.riesgo == float(riesgo)
            ):
                return conexion
        return None 
    def __str__(self):
        return f"De {self.origen} a {self.destino}. Tipo: {self.tipo}"

    def __eq__(self, other):
        return (
            self.origen == other.origen and
            self.destino == other.destino and
            self.tipo == other.tipo and
            self.distancia == other.distancia and
            self.restriccion == other.restriccion and
            self.valor_restriccion == other.valor_restriccion and
            self.riesgo == other.riesgo
        )
        

    def __hash__(self): #Resolver! Puede que tengamos que cambiar la estructura
        return hash((self.origen, self.destino, self.tipo, self.distancia, self.restriccion, self.valor_restriccion, self.riesgo))

    @staticmethod
    def validar(lista):
        tipos = ("fluvial", "aerea", "automotor", "ferroviaria")
        for i in range(len(lista)):
            if isinstance(lista[i], str):
                lista[i] = lista[i].strip().lower()
        if len(lista) != 7:                                    ###esperando lo que diga lucas
            raise TypeError('Cantidad de atributos insuficientes para instanciar una conexión')
        lista[4] = None if lista[4] == '' else lista[4]
        lista[5] = None if lista[5] == '' else lista[5]
        if Nodo.Nodo.get_nombre(lista[0]) is None:  
            raise ValueError(f'Nodo "{lista[0]}" inexistente')
        if Nodo.Nodo.get_nombre(lista[0]) == Nodo.Nodo.get_nombre(lista[1]):
            raise ValueError(f'El origen de una conexión no puede ser igual a su destino')
        if Nodo.Nodo.get_nombre(lista[1]) is None:  
            raise ValueError(f'Nodo "{lista[1]}" inexistente')
        if lista[2] not in tipos:
            raise ValueError(f'El tipo ingresado "{lista[2]}" es invalido')
       
        if not isinstance(lista[3], (int, float, str)):
            raise TypeError(f'Tipo de dato incorrecto para el atributo Distancia')
        
        else:
            try:
                lista[3] = float(lista[3])
            except ValueError:
                raise ValueError('El valor de la distancia debe ser un número válido')
            
            if lista[3] <= 0:
                raise ValueError(f'La distancia no puede ser negativa o 0')
        if (lista[4] == None and lista[5]) or (lista[5] == None and lista[4]):
            raise ValueError(f'Error en la restricción y el valor de la misma')
        if not (lista[4] == None and lista[5] == None):
            if lista[2] == 'fluvial':
                if not (lista[4] == 'tipo'):
                    raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte fluvial')
                else:
                    if not isinstance(lista[5],str):
                        raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')
                    elif not (lista[5] == 'fluvial' or lista[5] == 'maritimo'):
                        raise ValueError(f'El valor de la restricción {lista[5]} es inválido para la restricción')
            if lista[2] == 'aerea':
                if not (lista[4] == 'prob_mal_tiempo'):
                    raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte aéreo')
                else:
                    if not isinstance(lista[5], (int, float, str)):
                        raise TypeError(f'Tipo de dato incorrecto para el valor de la restricción')                
                    else:
                        try:
                            lista[5] = float(lista[5])
                        except ValueError:
                            raise ValueError('El valor de la restricción debe ser un número válido')
                        if not (1 > lista[5] > 0):
                            raise ValueError(f'El valor de la restricción es inválido')
            if lista[2] == 'ferroviaria':
                if not (lista[4] == 'velocidad_max'):
                    raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte ferroviario')
                else:
                    if not isinstance(lista[5], (int, str, float)):
                        raise ValueError(f'El valor de la restricción es inválido')    
                    else:
                        try:
                            lista[5] = float(lista[5])
                        except ValueError:
                            raise ValueError('El valor de la restricción debe ser un número válido')
                        if not (lista[5] > 0):
                            raise ValueError(f'El valor de la restricción es inválido')
            if lista[2] == 'automotor':
                if not (lista[4] == 'peso_max'):
                    raise ValueError(f'La restricción "{lista[4]}" es invalida para el transporte automotor')
                else:
                    if not isinstance(lista[5], (str, int, float)):
                        raise ValueError(f'El valor de la restricción es inválido')    
                    else: 
                        try:
                            lista[5] = float(lista[5])
                        except ValueError:
                            raise ValueError('El valor de la restricción debe ser un número válido')
                        if not (lista[5] > 0):
                            raise ValueError(f'El valor de la restricción es inválido')
        if not isinstance(lista[6], (int, float, str)):
            raise TypeError(f'Tipo de dato incorrecto para el atributo Riesgo')
        else: 
            try:
                lista[6] = float(lista[6])
            except ValueError:
                raise ValueError('El valor del riesgo debe ser un número válido')
        if not isinstance(lista[6],float) and not (0<lista[6]<1):   ###
            raise ValueError('El riesgo debe ser un número postivo mayor a 0 y menor a 1') ###
        if Conexion.get_conexion(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5], lista[6]) is not None: ###
            raise ValueError(f"La conexion '{lista[0]} a {lista[1]} de tipo: {lista[2]}' ya fue cargado.")
        return lista
    @staticmethod                                    
    def cargar(nombre_archivo):
        try:
            datos = Leer.LectorCSV.leer_csv(nombre_archivo)
            Leer.LectorCSV.validar(datos, nombre_archivo)
        except ValueError as e:
            print(e)
            return
        i =1
        for fila in datos:
            if fila:
                try:
                    conexion = Conexion.validar(fila)
                    Conexion(conexion[0],conexion[1],conexion[2],conexion[3],conexion[4],conexion[5],conexion[6])
                    Conexion(conexion[1],conexion[0],conexion[2],conexion[3],conexion[4],conexion[5],conexion[6])
                except (TypeError, ValueError) as e:
                    print(f"Error al cargar conexiones '{fila[0]}': {e}")
                    i = 0
        if i:
            print('Conexiones cargadas exitosamente.')
