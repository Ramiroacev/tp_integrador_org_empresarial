'''Chat Bot Licencias Medicas Organizacion Empresarial'''

import csv
from auxiliares import pedir_entero, lectura_csv
from principales import solicitar_licencia, consultar_estado

def menu_principal():
    while True:
        try:
            print("\nBienvenido al chat automantico (nombre empresa)...")
            print("¿Qué te trae por acá?\n")
            print("Ingrese la opción seleccionada: ")
            print(f" 1-Solicitar licencia\n 2-Consultar estado\n 3-Salir\n")
            opcion = pedir_entero()

            match opcion:       
                case 1:
                    solicitar_licencia()
                case 2:
                    consultar_estado()
                case 3:
                    print("Saliendo del bot")
                    break
                case _:
                    print('Error, debe ingresar un valor entre 1 y 3\n')
        except ValueError:
            print('Error, debe ingresar un número válido')
            
                
            
            

if __name__ == "__main__":
    menu_principal()
