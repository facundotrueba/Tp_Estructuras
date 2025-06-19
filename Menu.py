import Validaciones
import Planificador
import Itinerario
import Solicitud
def cargar_sistema():
            try:
                Validaciones.cargar_nodos('nodos.csv')
            except FileNotFoundError as e:
                print(f'Error al cargar nodos: "{e}"')
            try:
                Validaciones.cargar_conexiones('conexiones.csv')
            except FileNotFoundError as e:
                print(f'Error al cargar conexiones: "{e}"')
        
            try:
                Validaciones.cargar_solicitudes('solicitudes.csv')
            except FileNotFoundError as e:
                print(f'Error al cargar solicitudes: {e}')

    
def menu_principal():
    salir = False
    Planero=Planificador.Planificador("ADMIN")
    while not salir:
        print('-' * 50)
        print('Sistema de transporte - Menú principal')
        print('-' * 50)
        print('1. Cargar nodos, conexiones y solicitudes')
        print('2. Procesar solicitud')
        print('3. Salir')
        opcion = input("Seleccione una opción (1-3): ").strip() 
        if opcion == '1':
            cargar_sistema()
        elif opcion == '2':
            hay_solicitudes = True
            if Solicitud.Solicitud_Transporte.hay_solicitudes():
                id, tupla_menor_costo, tupla_menor_tiempo = Planero.procesar_siguiente() 
                itinerario = elegir_itinerario(id, tupla_menor_costo, tupla_menor_tiempo)
                #graficar_distancia_vs_tiempo(self, itinerario.vehiculo, itinerario.ruta)
                # graficar_costo_vs_distancia(self, vehiculo, ruta, cantidad_vehiculos, carga)
                # graficar_costo_vs_tiempo(self, vehiculo, ruta, cantidad_vehiculos, carga)
                #Yo agregaria aca el tema de los graficos
            else: 
                 print("No hay solicitudes pendientes.")
        elif opcion == '3':
            print('Programa terminado')
            salir = True
        else:#aca deberia tirar un raiserror
            print(f'Opcion "{opcion}" inválida. Se espera (1-2-3).')

def elegir_itinerario(id, menor_costo, menor_tiempo):
    ''' valido = False
    if not Solicitud.Solicitud_Transporte.hay_solicitudes():
            print("No hay solicitudes pendientes.")
            return ''' 
    print(f'Elegí la ruta segun lo que quieras optimizar \n1. Tiempo\n2. Costo')
    opcion = input('Introduzca la opción elegida (1-2): ').strip()
    if opcion == '1':
        itinerario = Itinerario.Itinerario(id, menor_tiempo[2], menor_tiempo[0], menor_tiempo[1], 'KPI 1', menor_tiempo[3], menor_tiempo[4], menor_tiempo[5])
        print('KPI 1: Minimizar el tiempo total de la entrega')
        Itinerario.Itinerario.mostrar_resumen(itinerario) #Quedaria ver si hay que almacenar los itinerarios en algun lado
        
    elif opcion == '2':
        itinerario = Itinerario.Itinerario(id, menor_costo[2], menor_costo[0], menor_costo[1], 'KPI 2', menor_costo[3], menor_costo[4], menor_costo[5])
        print('KPI 2: Minimizar el costo total del transporte')
        Itinerario.Itinerario.mostrar_resumen(itinerario)
    else:
        #Aca se deberia lanzar un error no?
        print(f'Opción "{opcion}" inválida. Se espera (1-2).')


menu_principal()