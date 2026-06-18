from modulos.auxiliares import pedir_entero, buscar_empleado, guardar_solicitud, buscar_solicitud, cambiar_estado_solicitud, lectura_csv_solicitudes
import random
from datetime import datetime

def pedir_fecha(mensaje):
    """Valida que la fecha tenga formato dd-mm-aaaa y sea real"""
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
            return fecha
        except ValueError:
            print("Fecha inválida. Use dd-mm-aaaa (ejemplo: 18-06-2026).")

def estado_inicio(estado=None):
    print("\n=== [Estado: Inicio] ===")
    print("Bienvenido al Bot de Licencias Médicas.")
    entrada = input("Escriba 'iniciar' para comenzar la solicitud o 'salir': ").strip().lower()
    if entrada == "iniciar":
        return estado_buscando_empleado
    elif entrada == "salir":
        return None
    else:
        print("Opción no válida.")
        return estado_inicio

def estado_buscando_empleado():
    print("\n=== [Estado: Buscando empleado] ===")
    legajo = pedir_entero("\nIngrese su número de legajo: ", 1)
    empleado = buscar_empleado(legajo)
    if empleado:
        print(f"Hola {empleado['nombre']}, vamos a verificar tus licencias")
        return lambda: estado_buscar_licencias(empleado)
    else:
        print("\nEl legajo no coincide con ningún empleado existente")
        return estado_buscando_empleado

def estado_buscar_licencias(empleado):
    print("\n=== [Estado: Licencias del empleado] ===")
    licencias = [l for l in lectura_csv_solicitudes() if l['legajo'] == str(empleado['legajo'])]

    if not licencias:
        print(f"{empleado['nombre']}, no tenés licencias registradas.")
        return lambda: estado_iniciar_solicitud(empleado)

    # Mostrar todas las licencias con índice amigable
    for i, l in enumerate(licencias, start=1):
        print(f"- Licencia #{i} | Estado: {l['estado']} | Fecha inicio: {l['fecha_inicio']} | Motivo: {l['motivo']}")

    opcion = input("Escriba el número de la licencia que quiere gestionar o 'nueva' para iniciar otra: ").strip().lower()
    if opcion == "nueva":
        return lambda: estado_iniciar_solicitud(empleado)

    try:
        idx = int(opcion) - 1
        seleccionada = licencias[idx]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return lambda: estado_buscar_licencias(empleado)

    estado = seleccionada['estado'].lower()
    if estado == "pendiente":
        return lambda: estado_licencia_activa(empleado, seleccionada)
    elif estado == "rechazada":
        return lambda: estado_rechazada(empleado, seleccionada)
    elif estado in ["aprobada", "cancelada", "reclamada"]:
        print("Esta licencia está cerrada.")
        opcion = input("¿Desea iniciar una nueva solicitud? (si/no): ").strip().lower()
        if opcion == "si":
            return lambda: estado_iniciar_solicitud(empleado)
        else:
            return estado_inicio

def estado_licencia_activa(empleado, licencia):
    print("\n=== [Estado: Licencia activa] ===")
    print(f"{empleado['nombre']}, tu licencia se encuentra en estado {licencia['estado']}")
    return lambda: estado_inicio('pendiente')

def estado_iniciar_solicitud(empleado):
    print("\n=== [Estado: Iniciar solicitud] ===")
    fecha_inicio = pedir_fecha("Ingrese la fecha de inicio de la licencia (dd-mm-aaaa): ")
    motivo = input("Ingrese el motivo de la licencia: ").strip()
    certificado = input("Ingrese el nombre del certificado médico (o Enter para dejar vacío): ").strip()

    if certificado == "":
        print("No se adjuntó certificado médico.")
        print("La solicitud queda a la espera de la carga del certificado.")
        return lambda: estado_esperando_certificado(empleado, fecha_inicio, motivo)

    return lambda: estado_solicitud_iniciada(empleado, fecha_inicio, motivo, certificado)

def estado_solicitud_iniciada(empleado, fecha_inicio, motivo, certificado):
    print("\n=== [Estado: Solicitud Iniciada] ===")
    print(f"Empleado: {empleado['nombre']} {empleado['apellido']}")
    print(f"Fecha inicio: {fecha_inicio}")
    print(f"Motivo: {motivo}")
    print(f"Certificado: {certificado}")

    id_solicitud = guardar_solicitud(empleado['legajo'], fecha_inicio, motivo, certificado)
    print("\nSolicitud registrada correctamente.")
    print(f"Número de solicitud: {id_solicitud}")
    print("Estado: Pendiente")
    print("Enviando solicitud a RRHH...")
    return lambda: estado_enviado_a_RRHH(id_solicitud)

def estado_esperando_certificado(empleado, fecha_inicio, motivo):
    print("\n=== [Estado: Esperando Certificado] ===")
    accion = input("Ingrese el nombre del certificado médico (o escriba 'cancelar'): ").strip()
    if accion.lower() == "cancelar":
        print("Solicitud cancelada por el usuario.")
        return estado_inicio
    if accion == "":
        print("Sigue sin adjuntarse el certificado médico.")
        return lambda: estado_esperando_certificado(empleado, fecha_inicio, motivo)
    return lambda: estado_solicitud_iniciada(empleado, fecha_inicio, motivo, accion)

def estado_enviado_a_RRHH(id_solicitud):
    print("\n=== [Estado: Solicitud en RRHH] ===")
    solicitud = buscar_solicitud(id_solicitud)

    if solicitud['estado'] in ['Pendiente', 'Reclamada']:
        evento_externo = random.choice(['APROBADA', 'RECHAZADA', 'STILL_PENDING'])
        if evento_externo == 'APROBADA':
            cambiar_estado_solicitud(id_solicitud, 'Aprobada')
            return estado_aprobada
        elif evento_externo == 'RECHAZADA':
            cambiar_estado_solicitud(id_solicitud, 'Rechazada')
            return lambda: estado_rechazada(None, solicitud)
        else:
            print("RRHH aún no ha revisado su solicitud.")
            opcion = input("Escriba 'verificar' para reintentar o 'cancelar' para desistir: ").strip().lower()
            if opcion == 'cancelar':
                cambiar_estado_solicitud(id_solicitud, 'Cancelada')
                print("Solicitud cancelada.")
                return estado_inicio
            return lambda: estado_enviado_a_RRHH(id_solicitud)

    print(f"La licencia ya no está pendiente. Estado actual: {solicitud['estado']}")
    return lambda: estado_inicio('procesada')

def estado_aprobada():
    print("\n=== [Estado: Aprobada] ===")
    print("¡Bien! Su solicitud ha sido aprobada con éxito por RRHH.")
    return lambda: estado_inicio('aprobada')

def estado_rechazada(empleado, licencia):
    print("\n=== [Estado: Rechazada] ===")
    if empleado:
        print(f"Lo sentimos {empleado['nombre']}, tu solicitud fue rechazada.")
    print(f"Motivo del rechazo: {licencia.get('motivo_rechazo','No especificado')}")

    opcion = input("Escriba 'reclamar' para pedir reevaluación o 'nueva' para iniciar otra solicitud: ").strip().lower()
    if opcion == "reclamar":
        if licencia['estado'].lower() == "reclamada":
            print("Esta licencia ya fue reclamada una vez y está cerrada.")
            return estado_inicio
        else:
            cambiar_estado_solicitud(licencia['id_solicitud'], 'Reclamada')
            print("Tu solicitud fue marcada como 'Reclamada' y enviada nuevamente a RRHH.")
            return lambda: estado_enviado_a_RRHH(int(licencia['id_solicitud']))
    elif opcion == "nueva" and empleado:
        return lambda: estado_iniciar_solicitud(empleado)
    else:
        return estado_inicio
