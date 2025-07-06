import Planificador
import Itinerario
import Solicitud
import Graficas
import Sistema_de_Transporte
import Conexion
import Nodo


class Utilidades_Menu:
    @staticmethod
    def cargar_sistema():
        try:
            Nodo.Nodo.cargar('nodos.csv')
        except FileNotFoundError as e:
            print(f'Error al cargar nodos: "{e}"')
        try:
            Conexion.Conexion.cargar('conexiones.csv')
        except FileNotFoundError as e:
            print(f'Error al cargar conexiones: "{e}"')
        try:
            Solicitud.Solicitud_Transporte.cargar('solicitudes.csv')
        except FileNotFoundError as e:
            print(f'Error al cargar solicitudes: {e}')

    @staticmethod
    def menu_principal():
        salir = False
        Planero = Planificador.Planificador('ADMIN')
        hay_solicitudes_procesadas = False
        
        while not salir:
            print('-' * 50)
            print('Sistema de transporte - Menú principal')
            print('-' * 50)
            print('1. Cargar nodos, conexiones y solicitudes')
            print('2. Procesar solicitudes')
            print("3. Ver solicitudes procesadas")
            print('4. Ver tramos más transitados')
            print('5. Salir')
            opcion = input("Seleccione una opción (1-5): ").strip()
            if opcion == '1':
                Utilidades_Menu.cargar_sistema()
            elif opcion == '2':
                if Solicitud.Solicitud_Transporte.hay_solicitudes():
                    try:
                        id, tupla_menor_costo, tupla_menor_tiempo, tupla_menor_riesgo = Planero.procesar_siguiente() 
                        itinerario = Utilidades_Menu.elegir_itinerario(id, tupla_menor_costo, tupla_menor_tiempo, tupla_menor_riesgo, Planero.historial_solicitudes_procesadas)
                        hay_solicitudes_procesadas = True
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
                            Graficas.Graficos.graficar_riesgo_total(dic_rutas, carga)#probar

                        except Exception as e:
                            print(f"Error al graficar rutas múltiples: {e}")
                else: 
                    print("No hay solicitudes pendientes.")       
            elif opcion == '3':
                Utilidades_Menu.historial_itinerarios(Planero.historial_solicitudes_procesadas)
            elif opcion == '4':
                if hay_solicitudes_procesadas:
                    Graficas.Graficos.plot_conexiones_mas_usadas(Planero.historial_solicitudes_procesadas)
                else:
                    print('No hay solicitudes procesadas')
            elif opcion == '5':
                print('Programa terminado')
                salir = True
            else:
                print(f'Opcion "{opcion}" inválida. Se espera (1-2-3-4-5).')

    @staticmethod
    def elegir_itinerario(id, menor_costo, menor_tiempo, menor_riesgo,historial_solicitudes_procesadas):
        print('Elegí el metodo de optimización \n1. Tiempo\n2. Costo\n3. Riesgo')
        opcion = input('Introduzca la opción elegida (1-3): ').strip()

        if opcion == '1':
            tupla   = menor_tiempo
            kpi_lbl = 'KPI 1'
            print('KPI 1: Minimizar el tiempo total de la entrega')
        elif opcion == '2':
            tupla   = menor_costo
            kpi_lbl = 'KPI 2'
            print('KPI 2: Minimizar el costo total del transporte')
        elif opcion == '3':
            tupla   = menor_riesgo
            kpi_lbl = 'KPI 3'
            print('KPI 3: Minimizar el riesgo total del transporte')
        else:
            print(f'Opción "{opcion}" inválida. Se espera (1-3).')
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
            tupla[6],   
            tupla[5]   
        )
        Itinerario.Itinerario.mostrar_resumen(itinerario)
        historial_solicitudes_procesadas.agregar(itinerario)
        
        return itinerario
    
    @staticmethod
    def historial_itinerarios(historial):
        id_solicitud = input('Ingrese el ID de la solicitud procesada que quiere ver: ')
        actual = historial.cabeza
        solicitud_procesada =False
        while actual:
            if id_solicitud==actual.itinerario.id_solicitud:
                print(f'ID: {id_solicitud}')
                print(f'{actual.itinerario}')
            
                solicitud_procesada = True          
            actual = actual.siguiente
        if not solicitud_procesada:
            print('La solicitud ingresada no fue procesada')
            
        
        

Utilidades_Menu.menu_principal()
