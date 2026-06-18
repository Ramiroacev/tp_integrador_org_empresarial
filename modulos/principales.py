from modulos.auxiliares import pedir_entero, buscar_empleado, guardar_solicitud, obtener_licencia, buscar_solicitud, cambiar_estado_solicitud
import random # Lo usamos para simular la respuesta externa de RRHH

def estado_inicio(estado = None):
    if not estado:
        print("\n--- [Estado: Inicio] ---")
        print("Bienvenido al Bot de Licencias Médicas.")

    entrada = input("Escriba 'iniciar' para comenzar la solicitud o 'salir': ").strip().lower()
    
    if entrada == "iniciar":
        return estado_buscando_empleado
    elif entrada == "salir":
        return None
    else:
        print("Opción no válida.")
        return estado_inicio                    # recursividad
    
def estado_buscando_empleado():
    print("\n--- [Estado: Buscando empleado] ---")
    legajo = pedir_entero("\nIngrese su número de legajo: ", 1)

    empleado = buscar_empleado(legajo)

    if empleado:
        print(f"Hola {empleado['nombre']}, vamos a verificar si tenés licencias activas")
        # Para pasar argumentos entre estados sin ejecutar la función aquí, 
        # usamos una función lambda
        return lambda: estado_buscar_licencia(empleado)
    else:
        print("\nEl legajo no coincide con ningún empleado existente")
        return estado_buscando_empleado

def estado_buscar_licencia(empleado):
    print("\n--- [Estado: Buscando licencias] ---")
    licencia = obtener_licencia(empleado['legajo'])

    if licencia:
        print(f"Hemos verificado {empleado['nombre']}, que tenés una licencia activa")
        return lambda: estado_licencia_activa(empleado, licencia)
    else:
        print(f"Bien {empleado['nombre']}, hemos verificado que no tenes licencias activas")
        return lambda: estado_iniciar_solicitud(empleado)
    
def estado_licencia_activa(empleado, licencia):
    print("\n--- [Estado: Licencia activa] ---")
    print(f"{empleado['nombre']}, tu licencia se encuentra en estado {licencia['estado']}")
    return lambda: estado_inicio('pendiente')

def estado_iniciar_solicitud(empleado):
    print("\n--- [Estado: Iniciar solicitud] ---")
    print("Vamos a iniciar una nueva solicitud, por favor ingresa los siguientes datos\n")
    fecha_inicio = input("Ingrese la fecha de inicio de la licencia (dd-mm-aaaa): ").strip()
    motivo = input("Ingrese el motivo de la licencia: ").strip()
    certificado = input("Ingrese el nombre del certificado médico (o Enter para dejar vacío): ").strip()

    if certificado == "":
        print("No se adjuntó certificado médico.")
        print("La solicitud queda a la espera de la carga del certificado.")
        return lambda: estado_esperando_certificado(empleado, fecha_inicio, motivo)

    return lambda: estado_solicitud_iniciada(empleado, fecha_inicio, motivo, certificado)

def estado_solicitud_iniciada(empleado, fecha_inicio, motivo, certificado):
    print("\n--- [Estado: Solicitud Iniciada] ---")
    print("\n=== Resumen de Solicitud ===")
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
    print("\n--- [Estado: Esperando Certificado] ---")
    # El usuario puede decidir cancelar la carga aquí usando el input
    accion = input("Ingrese el nombre del certificado médico (o escriba 'cancelar'): ").strip()

    if accion.lower() == "cancelar":
        print("Solicitud cancelada por el usuario.")
        return estado_inicio

    if accion == "":
        print("Sigue sin adjuntarse el certificado médico.")
        return lambda: estado_esperando_certificado(empleado, fecha_inicio, motivo)
    
    return lambda: estado_solicitud_iniciada(empleado, fecha_inicio, motivo, accion)

def estado_enviado_a_RRHH(id_solicitud):
    print("\n--- [Estado: Solicitud en RRHH (Esperando Evento Externo)] ---")
    solicitud = buscar_solicitud(id_solicitud)

    if solicitud['estado'] == 'Pendiente':
        # SIMULACIÓN DE EVENTO EXTERNO (Aprobación, Rechazo o Sigue Pendiente)
        # En producción, esto consultaría un servicio web o el cambio de estado en el archivo por un admin.
        evento_externo = random.choice(['APROBADA', 'RECHAZADA', 'STILL_PENDING'])
        
        if evento_externo == 'APROBADA':
            cambiar_estado_solicitud(id_solicitud, 'Aprobada')
            return estado_aprobada
        elif evento_externo == 'RECHAZADA':
            cambiar_estado_solicitud(id_solicitud, 'Rechazada')
            return estado_rechazada
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
    print("\n--- [Estado: Aprobada] ---")
    print("¡Bien! Su solicitud ha sido aprobada con éxito por RRHH.")
    return lambda: estado_inicio('aprobada')

def estado_rechazada():
    print("\n--- [Estado: Rechazada] ---")
    print("Lo sentimos, su solicitud ha sido rechazada por RRHH.")
    return lambda: estado_inicio('rechazada')
