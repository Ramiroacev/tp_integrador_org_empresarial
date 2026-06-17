from auxiliares import pedir_entero, buscar_empleado

def solicitar_licencia():
    legajo = pedir_entero()
    empleado = buscar_empleado(legajo)
    if empleado is None:
        print("Legajo inexistente.")
        return


def consultar_estado():
    print("Hola soy la opcion consultar estado")
