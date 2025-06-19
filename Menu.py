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
            hay_solicitudes = True
            if Solicitud.Solicitud_Transporte.hay_solicitudes():
                id, tupla_menor_costo, tupla_menor_tiempo = Planero.procesar_siguiente() 
                itinerario = elegir_itinerario(id, tupla_menor_costo, tupla_menor_tiempo)
                Graficas.Graficos().graficar_distancia_vs_tiempo(itinerario.vehiculo, itinerario.ruta)
                Graficas.Graficos().graficar_costo_vs_distancia(itinerario.vehiculo, itinerario.ruta, itinerario.cantidad_vehiculos)
                Graficas.Graficos().graficar_costo_vs_tiempo(itinerario.vehiculo, itinerario.ruta, itinerario.cantidad_vehiculos)
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

    # ——— AÑADIDO: mapear el string al objeto de transporte ———
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

    # ——— Construyo el Itinerario con la instancia, no con el string ———
    itinerario = Itinerario.Itinerario(
        id,
        tupla[2],      # ruta
        tupla[0],      # costo
        tupla[1],      # tiempo
        kpi_lbl,
        vehiculo,      # ← acá va la instancia
        tupla[4],      # cantidad_vehículos
        tupla[5]       # carga
    )
    Itinerario.Itinerario.mostrar_resumen(itinerario)
    return itinerario


menu_principal()