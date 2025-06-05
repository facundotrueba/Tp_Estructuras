import Sistema_de_Transporte
import csv

def leer_csv(nombre_archivo):
    datos=[]
    try:
        with open(nombre_archivo, mode='r') as file:
            lector = csv.reader(file)
            for fila in lector:
                datos.append(fila)
            return datos
    except FileNotFoundError:
        print("Archivo no encontrado")

def cargar_conexiones(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        c = Sistema_de_Transporte.Conexion(i[0], i[1], i[2], i[3], i[4], i[5])

def cargar_solicitudes(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        s = Sistema_de_Transporte.Solicitud_Transporte(i[0], i[1], i[2], i[3])

def cargar_nodos(nombre_archivo):
    datos = leer_csv(nombre_archivo)
    for i in datos:
        n = Sistema_de_Transporte.Nodos(i)



