import Validaciones
import Planificador
import Itinerario
import Solicitud
import Graficas
import Sistema_de_Transporte
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
            if Solicitud.Solicitud_Transporte.hay_solicitudes():
                try:
                    id, tupla_menor_costo, tupla_menor_tiempo = Planero.procesar_siguiente() 
                    itinerario = elegir_itinerario(id, tupla_menor_costo, tupla_menor_tiempo)
                except TypeError as e:
                    print(e)
                    return
                mostrar_grafs=input("Presione 1 para que se le impriman los graficos:  ")
                if mostrar_grafs=="1": 
                    Graficas.Graficos.graficar_distancia_vs_tiempo(itinerario.vehiculo, itinerario.ruta)
                    Graficas.Graficos.graficar_costo_vs_distancia(itinerario.vehiculo, itinerario.ruta, itinerario.cantidad_vehiculos, itinerario.carga)
                    Graficas.Graficos.graficar_costo_vs_tiempo(itinerario.vehiculo, itinerario.ruta, itinerario.cantidad_vehiculos, itinerario.carga)
            else: 
                 print("No hay solicitudes pendientes.")
        elif opcion == '3':
            print('Programa terminado')
            salir = True
        else:
            print(f'Opcion "{opcion}" inválida. Se espera (1-2-3).')

def elegir_itinerario(id, menor_costo, menor_tiempo):
    print('Elegí la ruta según lo que quieras optimizar \n1. Tiempo\n2. Costo')
    opcion = input('Introduzca la opción elegida (1-2): ').strip()

    if opcion == '1':
        tupla   = menor_tiempo
        kpi_lbl = 'KPI 1'
        print('KPI 1: Minimizar el tiempo total de la entrega')
    elif opcion == '2':
        tupla   = menor_costo
        kpi_lbl = 'KPI 2'
        print('KPI 2: Minimizar el costo total del transporte')
    else:
        print(f'Opción "{opcion}" inválida. Se espera (1-2).')
        return

    mapa_tipos = {
        'automotor':   Sistema_de_Transporte.Automotor,
        'aerea':       Sistema_de_Transporte.Aerea,
        'fluvial':     Sistema_de_Transporte.Fluvial,
        'ferroviaria': Sistema_de_Transporte.Ferroviaria
    }
    tipo_str = tupla[3]                # p.ej. "automotor", "aerea", …
    VehClase = mapa_tipos.get(tipo_str)
    if VehClase is None:
        raise ValueError(f"Tipo de transporte desconocido: {tipo_str}")
    vehiculo = VehClase()              # instancia Automotor(), Aerea(), …

    # Construimos el Itinerario
    itinerario = Itinerario.Itinerario(
        id,
        tupla[2],      # ruta
        tupla[0],      # costo
        tupla[1],      # tiempo
        kpi_lbl,
        vehiculo,      # instancia
        tupla[4],      # cantidad_vehículos
        tupla[5]       # carga
    )
    Itinerario.Itinerario.mostrar_resumen(itinerario)
    return itinerario 
''' 
import Validaciones
import Planificador
import Itinerario
import Solicitud
import Graficas
import Sistema_de_Transporte

class Utilidades_Menu:
    
    @staticmethod
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
                Validaciones.cargar_solicitudes('soliciudes.csv')
            except FileNotFoundError as e:
                print(f'Error al cargar solicitudes: {e}')

    @staticmethod
    def menu_principal():
        salir = False
        while not salir:
            print('-' * 50)
            print('Sistema de transporte - Menú principal')
            Planero=Planificador.Planificador("ADMIN")
            
            print('-' * 50)
            print('1. Cargar nodos, conexiones y solicitudes')
            print('2. Procesar solicitudes')
            print('3. Salir')
            opcion = input("Seleccione una opción (1-3): ").strip() 
            if opcion == '1':
                sistema_cargado = Utilidades_Menu.cargar_sistema()
            elif opcion == '2':
                Utilidades_Menu.procesar_solicitudes()        
            elif opcion == '3':
                print('Programa terminado')
                salir = True
            else:
                print(f'Opcion "{opcion}" inválida. Se espera (1-2-3).')

    @staticmethod
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
                return itinerario
            elif opcion == '2':
                itinerario = Itinerario.Itinerario(id, menor_costo[2], menor_costo[0], menor_costo[1], 'KPI 2', menor_costo[3], menor_costo[4], menor_costo[5])
                print('KPI 2: Minimizar el costo total del transporte')
                Itinerario.Itinerario.mostrar_resumen(itinerario)
                valido = True
                return itinerario
            else:
                print(f'Opción "{opcion}" inválida. Se espera (1-2).')

    @staticmethod
    def procesar_solicitudes():
        hay_solicitudes = True
        while hay_solicitudes:
            id, menor_costo, menor_tiempo = Planificador.Planificador.procesar_siguiente() 
            itinerario = Utilidades_Menu.elegir_itinerario(id, menor_costo, menor_tiempo)
            Utilidades_Menu.ejecutar_graficos(itinerario.vehiculo,itinerario.ruta,itinerario.cantidad_vehiculos)
            
    @staticmethod
    def ejecutar_graficos(vehiculo,ruta,cantidad_vehiculos):
        valido = 0
        while not valido:      
            print(f'Gráficos disponibles para visualizar\n1.Distancia vs Tiempo\n2.Costo VS Distancia\3.Costo VS Tiempo\n4.No quiero visualizar gráficos')
            opcion_graficos = input('Seleccione una opción (1-4): ').strip()
            if opcion_graficos == '1':
                Graficas.Graficos.graficar_distancia_vs_tiempo(vehiculo, ruta)
            elif opcion_graficos == '2':
                Graficas.Graficos.graficar_costo_vs_distancia(vehiculo, ruta, cantidad_vehiculos)
            elif opcion_graficos == '3':
                Graficas.Graficos.graficar_costo_vs_tiempo(vehiculo, ruta, cantidad_vehiculos)
            elif opcion_graficos == '4':
                valido = 1
            else:
                print(f'Opción {opcion_graficos} inválida. Se espera (1-2-3-4)')
 '''
menu_principal()