import csv

class LectorCSV:
    @staticmethod
    def leer_csv(nombre_archivo):
        datos = []
        try:
            with open(nombre_archivo, mode="r",encoding="utf-8") as file:
                lector = csv.reader(file)
                i=0
                for fila in lector:
                    if i == 0:
                        i = 1
                    else:
                        datos.append(fila)
                return datos
        except FileNotFoundError:
            print("Archivo no encontrado")
            return []
    @staticmethod    
    def validar(datos, nombre_archivo):
        if not datos:
            raise ValueError(f"Archivo '{nombre_archivo}' vacío o no válido.")
        return True
    
