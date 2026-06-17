#funciones complementarias
from pathlib import Path
import csv
# Proyecto portable en Windows y Linux
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de los csv
EMPLEADOS_CSV = BASE_DIR / "datos" / "empleados.csv"
SOLICITUDES_CSV = BASE_DIR / "datos" / "solicitudes_licencias.csv"
def lectura_csv_empleados():    
    try:                 #intenta tener acceso al archivo con los datos
        with open(EMPLEADOS_CSV, "r", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo, delimiter=','))   #se utiliza el delimitador ; ya que el csv esta con ese valor
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

def lectura_csv_solicitudes():    #auxiliar de guarda solicitudes
    try:
        with open(SOLICITUDES_CSV, "r", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        return

def obtener_proximo_id():       #para generar un nuevo ID para guardar solicitudes
    solicitudes = lectura_csv_solicitudes()

    if not solicitudes:
        return 1

    return max(int(solicitud["id_solicitud"]) for solicitud in solicitudes) + 1

def guardar_solicitud(legajo,fecha_inicio,motivo,certificado):
    id_solicitud = obtener_proximo_id()
    with open(SOLICITUDES_CSV,"a",newline="",encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([id_solicitud,legajo,fecha_inicio,motivo,certificado,"Pendiente"])
    return id_solicitud
    
def pedir_entero(minimo=0):
    """Verifica que el número ingresado sea válido y persiste hasta que lo sea"""
    while True:
        try:            #solo es para validar los numero ingresados
            numero = int(input().strip())

            if numero < minimo:
                print(f'Error, el valor ingresado debe ser mayor o igual a {minimo}')
                continue

            return numero

        except ValueError:
            print('Error, debe ingresar un número válido')

