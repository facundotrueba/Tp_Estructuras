import Sistema_de_Transporte 
import auxiliar, Planificador

#import todo

def main(planificador):
    menu_valido=0
    while menu_valido != "E":
            if menu_valido==0:
                menu_valido= validar_menu() #esto es del cuatri PASADO, fijarse para que se uso y repetir
                
            if menu_valido=='A':
                    ##TODO LO DE CENTRAL##
                    self.submenus.submenu_central()
                    menu_valido=0
                                        
            if menu_valido=='B':
                    ##TODO LO DE PHONE##
                    self.submenus.usar_cel()
                    menu_valido=0
                    pass
                    
            if menu_valido=='C':
                    ##TODO LO DE ANALISIS DE DATOS##
                    self.submenus.submenu_analisis()
                    menu_valido=0
                    
            if menu_valido == "D":
                    self.submenus.submenu_tablet()
                    menu_valido=0

            if menu_valido=='E':
                    print("Gracias por usar el programa")
                    exit()
    planificador.procesar_siguiente
