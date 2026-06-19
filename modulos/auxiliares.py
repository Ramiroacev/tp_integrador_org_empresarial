# funciones complementarias
from pathlib import Path
import csv
from datetime import datetime   # <-- agregado para fecha_solicitud

# Proyecto portable en Windows y Linux
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de los csv
EMPLEADOS_CSV = BASE_DIR / "datos" / "empleados.csv"
SOLICITUDES_CSV = BASE_DIR / "datos" / "solicitudes_licencias.csv"

def inicializar_archivos():    # ocurre primero
    if not SOLICITUDES_CSV.exists():
        with open(SOLICITUDES_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["id_solicitud","legajo","fecha_solicitud","fecha_inicio","motivo","certificado","estado"])

def lectura_csv_empleados():    
    try:
        with open(EMPLEADOS_CSV, "r", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo, delimiter=','))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{EMPLEADOS_CSV}' en el directorio actual.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return []

def buscar_empleado(legajo):
    empleados = lectura_csv_empleados()
    for empleado in empleados:
        if int(empleado["legajo"]) == legajo:
            return empleado
    return None

def obtener_licencia(legajo):
    licencias = lectura_csv_solicitudes()
    if licencias:
        for licencia in licencias:
            if licencia['legajo'] == legajo:
                return licencia
    return None

def lectura_csv_solicitudes():
    try:
        with open(SOLICITUDES_CSV, "r", encoding="utf-8") as archivo:
            contenido = list(csv.DictReader(archivo))
            return contenido if contenido else []
    except FileNotFoundError:
        return []

def escribir_csv_solicitudes(solicitudes):
    """Sobrescribe el archivo solicitudes_licencias.csv con la lista actualizada"""
    campos = ["id_solicitud", "legajo", "fecha_solicitud", "fecha_inicio", "motivo", "certificado", "estado"]
    with open(SOLICITUDES_CSV, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for s in solicitudes:
            writer.writerow(s)

def obtener_proximo_id():
    solicitudes = lectura_csv_solicitudes()
    if not solicitudes:
        return 1
    return max(int(solicitud["id_solicitud"]) for solicitud in solicitudes) + 1

def guardar_solicitud(legajo, fecha_inicio, motivo, certificado):
    id_solicitud = obtener_proximo_id()
    fecha_solicitud = datetime.now().strftime("%d-%m-%Y")
    with open(SOLICITUDES_CSV, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([id_solicitud, legajo, fecha_solicitud, fecha_inicio, motivo, certificado, "Pendiente"])
    return id_solicitud

def pedir_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje).strip())
            if numero < minimo:
                print(f'Error, el valor ingresado debe ser mayor o igual a {minimo}')
                continue
            return numero
        except ValueError:
            print('Error, debe ingresar un número válido')

def buscar_solicitud(id_solicitud):
    solicitudes = lectura_csv_solicitudes()
    for solicitud in solicitudes:
        if int(solicitud['id_solicitud']) == id_solicitud:
            return solicitud
    return None

def cambiar_estado_solicitud(id_solicitud, nuevo_estado, certificado=None):
    """Actualiza el estado (y opcionalmente el certificado) de una solicitud en el CSV"""
    solicitudes = lectura_csv_solicitudes()
    for s in solicitudes:
        if s['id_solicitud'] == str(id_solicitud):
            s['estado'] = nuevo_estado
            if certificado is not None:
                s['certificado'] = certificado
    escribir_csv_solicitudes(solicitudes)

def pedir_fecha(mensaje):
    """Valida que la fecha tenga formato dd-mm-aaaa y sea real"""
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
            return fecha
        except ValueError:
            print("Fecha inválida. Use dd-mm-aaaa (ejemplo: 18-06-2026).")
