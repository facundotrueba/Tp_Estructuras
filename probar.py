def encontrar_todas_las_rutas(grafo, nodo_inicio, nodo_fin, camino_actual=None): #PORQUE SE HACE ESTO DE CAMINOACTUAL=NONE, NO ES MAS FACIL SOLO CREAR UNA LISTA VACIA EN LA PROXIMA LINEA
    if camino_actual is None:
        camino_actual = []

    camino_actual = camino_actual + [nodo_inicio]

    if nodo_inicio == nodo_fin:
        return [camino_actual]

    rutas = []
    for vecino in grafo.get(nodo_inicio,[]):
        if vecino not in camino_actual:
            nuevas_rutas = encontrar_todas_las_rutas(grafo, vecino, nodo_fin, camino_actual)
            rutas.extend(nuevas_rutas)
    return rutas


class Ciudad:
    pass

Buenos_Aires = Ciudad()
Azul = Ciudad()
Mar_del_Plata = Ciudad()
Zarate = Ciudad()
Junin = Ciudad()

grafo = {
    Buenos_Aires: [Azul, Junin, Mar_del_Plata,Zarate],
    Azul: [Mar_del_Plata, Junin, Buenos_Aires],
    Junin: [Azul,Buenos_Aires, Zarate],
    Zarate:[Buenos_Aires,Junin],
    Mar_del_Plata:[Buenos_Aires, Azul]
}
grafo2 = {
    "Buenos Aires": ["Azul", "Junin", "Mar del Plata","Zarate"],
    "Azul": ["Mardel Plata", "Junin", "Buenos Aires"],
    "Junin": ["Azul","Buenos Aires", "Zarate"],
    "Zarate":["Buenos Aires","Junin"],
    "Mar del Plata":["Buenos Aires", "Azul"]
}

rutas = encontrar_todas_las_rutas(grafo, Buenos_Aires, Mar_del_Plata)
for r in rutas:
    print(r)  

''' def construir_grafo():
    grafo = {}
    for conexiones in Conexion.conexiones_por_tipo.values():
        for conexion in conexiones:
            if conexion.origen not in grafo:
                grafo[conexion.origen] = []
            grafo[conexion.origen].append(conexion)
    return grafo
 ''' #nose que tan bien este eso


def encontrar_rutas(grafo, nodo_inicio, nodo_fin):
       #falta la func que pasa de el diccionario de conexion cada grafo
       rutas=[] 
       
       conexiones_recorridas=[]
       if not ciudades_recorridas:
            conexiones_posibles = grafo.get(nodo_inicio, [])
       else: 
           ultimo_nodo = conexiones_recorridas[-1].destino
           if ultimo_nodo == nodo_fin:
            return [camino_actual]
       conexiones_posibles = grafo.get(ultimo_nodo, [])     


    
    
    
    
    