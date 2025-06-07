import Sistema_de_Transporte
import csv

def leer_csv(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, mode="r") as file:
            lector = csv.reader(file)
            next(lector) 
            for fila in lector:
                datos.append(fila)
        return datos
    except FileNotFoundError:
        print("Archivo no encontrado")

def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        if i and i[0].strip():
            Sistema_de_Transporte.Nodo(i[0].strip())
def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        restriccion = i[4] if len(i) > 4 and i[4] else None
        valor_restriccion = i[5] if len(i) > 5 and i[5] else None

        origen = Sistema_de_Transporte.Nodo.get_nombre(i[0])
        destino = Sistema_de_Transporte.Nodo.get_nombre(i[1])

        tipo = i[2].strip().lower() if len(i) > 2 else None

        if tipo not in Sistema_de_Transporte.Conexion.tipos:
            print(f"Tipo desconocido: '{tipo}'")

        ida = Sistema_de_Transporte.Conexion(origen, destino, tipo, i[3], restriccion, valor_restriccion)
        vuelta = Sistema_de_Transporte.Conexion(destino, origen, tipo, i[3], restriccion, valor_restriccion)

def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        s = Sistema_de_Transporte.Solicitud_Transporte(i[0], i[1], i[2], i[3])


def inicializar_sistema(nodos_path, conexiones_path):
    cargar_nodos(nodos_path)
    cargar_conexiones(conexiones_path)
    grafo = Sistema_de_Transporte.construir_grafo(Sistema_de_Transporte.Conexion.conexiones_por_tipo)
    return grafo

