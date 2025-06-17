import Validaciones
import Sistema_de_Transporte
import Planificador
import Itinerario
def cargar_sistema(archivo_nodos, archivo_conexiones, archivo_solicitudes):
    Validaciones.cargar_nodos(archivo_nodos)
    Validaciones.cargar_conexiones(archivo_conexiones)
    Validaciones.cargar_solicitudes(archivo_solicitudes)
def menu_principal():
    salir = False
    while not salir:
        print('-' * 50)
        print('Sistema de transporte - Menú principal')
        print('-' * 50)
        print('1. Cargar nodos y conexiones')
        print('2. Cargar solicitudes')
        print('3. Procesar solicitudes')
        print('4. Salir')
        opcion = input("Seleccione una opción (1-4): ").strip() 
        if opcion == '1':
            ruta_archivo_nodos = input('Ingrese la ubicación del archivo de nodos: ').strip()
            try:
                Validaciones.cargar_nodos(ruta_archivo_nodos)
                print('Nodos cargados exitosamente.')
            except FileNotFoundError as e:
                print('Error al cargar nodos: {e}')
            ruta_archivo_conexiones = input('Ingrese la ubicación del archivo de conexiones: ').strip()
            try:
                Validaciones.cargar_conexiones(ruta_archivo_conexiones)
                print('Conexiones cargadas exitosamente.')
            except FileNotFoundError as e:
                print('Error al cargar conexiones: {e}')
        elif opcion == '2':
            ruta_archivo_solicitudes = input('Ingrese la ubicación del archivo de solicitudes: ').strip()
            try:
                Validaciones.cargar_nodos(ruta_archivo_solicitudes)
                print('Solicitudes cargadas exitosamente.')
            except FileNotFoundError as e:
                print('Error al cargar solicitudes: {e}')
        elif opcion == '3':
            hay_solicitudes = True
            while hay_solicitudes:
                id, menor_costo, menor_tiempo = Planificador.Planificador.procesar_siguiente() #Revisar funcion, no se si necesita que este el self
                elegir_itinerario(id, menor_costo, menor_tiempo)
                #Yo agregaria aca el tema de los graficos
        elif opcion == '4':
            print('Programa terminado')
            salir = True
        else:
            print(f'Opcion "{opcion}" inválida. Se espera (1-2-3-4).')

def elegir_itinerario(id, menor_costo, menor_tiempo):
    valido = False
    while not valido:
        print(f'Elegí la ruta segun lo que quieras optimizar \n1. Tiempo\n2. Costo')
        opcion = input('Introduzca la opción elegida (1-2): ').strip()
        if opcion == '1':
            itinerario = Itinerario.Itinerario(id, menor_tiempo[2], menor_tiempo[0], menor_tiempo[1], 'KPI 1', menor_tiempo[3], menor_tiempo[4], menor_tiempo[5])
            print('KPI 1: Minimizar el tiempo total de la entrega')
            Itinerario.Itinerario.mostrar_resumen(itinerario) #Quedaria ver si hay que almacenar los itinerarios en algun lado
            valido = True
        elif opcion == '2':
            itinerario = Itinerario.Itinerario(id, menor_costo[2], menor_costo[0], menor_costo[1], 'KPI 2', menor_costo[3], menor_costo[4], menor_costo[5])
            print('KPI 2: Minimizar el costo total del transporte')
            Itinerario.Itinerario.mostrar_resumen(itinerario)
            valido = True
        else:
            print(f'Opción "{opcion}" inválida. Se espera (1-2).')