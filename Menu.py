'''
import Validaciones
import Planificador
import Itinerario
import Solicitud
import Graficas
import Sistema_de_Transporte
import Conexion
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
                        try:
                            ruta = itinerario.ruta
                            carga = itinerario.carga
                            grafo = Planificador.Planificador.construir_grafo(Conexion.Conexion.conexiones_por_tipo)
                            dic_rutas = Planificador.Planificador.encontrar_todas_rutas(
                                grafo, ruta[0].origen, ruta[-1].destino
                            )
                            Graficas.Graficos.graficar_distancia_vs_tiempo_todas_rutas(dic_rutas)
                            Graficas.Graficos.graficar_costo_vs_distancia_todas_rutas(dic_rutas, carga)
                            Graficas.Graficos.graficar_costo_vs_tiempo_todas_rutas(dic_rutas, carga)

                        except Exception as e:
                            print(f"Error al graficar rutas múltiples: {e}")
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
import Conexion

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
            Validaciones.cargar_solicitudes('solicitudes.csv')
        except FileNotFoundError as e:
            print(f'Error al cargar solicitudes: {e}')

    @staticmethod
    def menu_principal():
        salir = False
        Planero = Planificador.Planificador('ADMIN')
        while not salir:
            print('-' * 50)
            print('Sistema de transporte - Menú principal')
            print('-' * 50)
            print('1. Cargar nodos, conexiones y solicitudes')
            print('2. Procesar solicitudes')
            print('3. Salir')
            opcion = input("Seleccione una opción (1-3): ").strip() 
            if opcion == '1':
                Utilidades_Menu.cargar_sistema()
            elif opcion == '2':
                if Solicitud.Solicitud_Transporte.hay_solicitudes():
                    try:
                        id, tupla_menor_costo, tupla_menor_tiempo = Planero.procesar_siguiente() 
                        itinerario = Utilidades_Menu.elegir_itinerario(id, tupla_menor_costo, tupla_menor_tiempo)
                    except TypeError as e:
                        print(e)
                        return
                    mostrar_grafs=input("Presione 1 para que se le impriman los graficos:  ")
                    if mostrar_grafs=="1": 
                        try:
                            ruta = itinerario.ruta
                            carga = itinerario.carga
                            grafo = Planificador.Planificador.construir_grafo(Conexion.Conexion.conexiones_por_tipo)
                            dic_rutas = Planificador.Planificador.encontrar_todas_rutas(
                                grafo, ruta[0].origen, ruta[-1].destino
                            )
                            Graficas.Graficos.graficar_distancia_vs_tiempo_todas_rutas(dic_rutas)
                            Graficas.Graficos.graficar_costo_vs_distancia_todas_rutas(dic_rutas, carga)
                            Graficas.Graficos.graficar_costo_vs_tiempo_todas_rutas(dic_rutas, carga)

                        except Exception as e:
                            print(f"Error al graficar rutas múltiples: {e}")
                else: 
                    print("No hay solicitudes pendientes.")       
            elif opcion == '3':
                print('Programa terminado')
                salir = True
            else:
                print(f'Opcion "{opcion}" inválida. Se espera (1-2-3).')

    @staticmethod
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
        tipo_str = tupla[3] 
        VehClase = mapa_tipos.get(tipo_str)
        if VehClase is None:
            raise ValueError(f"Tipo de transporte desconocido: {tipo_str}")
        vehiculo = VehClase()             

        itinerario = Itinerario.Itinerario(
            id,
            tupla[2],
            tupla[0],
            tupla[1],      
            kpi_lbl,
            vehiculo,      
            tupla[4],      
            tupla[5]      
        )
        Itinerario.Itinerario.mostrar_resumen(itinerario)
        return itinerario


Utilidades_Menu.menu_principal()
