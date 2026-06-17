'''Chat Bot Licencias Medicas Organizacion Empresarial'''
#prueba

from modulos.auxiliares import pedir_entero
from modulos.principales import solicitar_licencia, consultar_estado

def menu_principal():
    while True:
        print("\n=== BOT RRHH ===")
        print("Bienvenido al sistema de licencias médicas")
        print("\nSeleccione una opción:")
        print("1 - Solicitar licencia")
        print("2 - Consultar estado")
        print("3 - Salir")

        opcion = pedir_entero()

        match opcion:
            case 1:
                solicitar_licencia()

            case 2:
                consultar_estado()

            case 3:
                print("Gracias por utilizar el sistema.")
                break

            case _:
                print("Error, debe ingresar una opción entre 1 y 3.")
            

if __name__ == "__main__":
    menu_principal()
