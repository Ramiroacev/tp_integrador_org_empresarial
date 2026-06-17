from modulos.auxiliares import pedir_entero, buscar_empleado, guardar_solicitud

def solicitar_licencia():   #opcion 1
    print("\n=== Solicitud de Licencia Médica ===")

    print("Ingrese su número de legajo:")
    legajo = pedir_entero()

    empleado = buscar_empleado(legajo)

    if empleado is None:
        print("Legajo inexistente.")
        return

    print(f"\nBienvenido {empleado['nombre']} {empleado['apellido']}")

    fecha_inicio = input(
        "Ingrese la fecha de inicio de la licencia (dd-mm-aaaa): "
    ).strip()

    motivo = input(
        "Ingrese el motivo de la licencia: "
    ).strip()

    certificado = input(
        "Ingrese el nombre del certificado médico: "
    ).strip()

    if certificado == "":
        print("No se adjuntó certificado médico.")
        print("La solicitud no puede enviarse a RRHH.")
        return

    print("\n=== Resumen de Solicitud ===")
    print(f"Empleado: {empleado['nombre']} {empleado['apellido']}")
    print(f"Fecha inicio: {fecha_inicio}")
    print(f"Motivo: {motivo}")
    print(f"Certificado: {certificado}")
    id_solicitud = guardar_solicitud(legajo,fecha_inicio,motivo,certificado)
    print("\nSolicitud registrada correctamente.")
    print(f"Número de solicitud: {id_solicitud}")
    print("Estado: Pendiente")
    print("Enviando solicitud a RRHH...")
#---------------------------------------------------------------------------
def consultar_estado():
    print("Hola soy la opcion consultar estado")
