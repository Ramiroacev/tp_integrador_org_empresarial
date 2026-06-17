#funciones complementarias
from pathlib import Path
import csv
# Proyecto portable en Windows y Linux
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de los csv
EMPLEADOS_CSV = BASE_DIR / "datos" / "empleados.csv"
SOLICITUDES_CSV = BASE_DIR / "datos" / "solicitudes_licencias.csv"

def inicializar_archivos():

    if not SOLICITUDES_CSV.exists():

        with open(SOLICITUDES_CSV,"w",newline="",encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["id_solicitud","legajo","fecha_solicitud","fecha_inicio","motivo","certificado","estado"])
            
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

def obtener_licencia(legajo):
    licencias = lectura_csv_solicitudes()
    if licencias:
        for licencia in licencias:
            if licencia['legajo'] == legajo:
                return licencia
        
    return None

def lectura_csv_solicitudes():    #auxiliar de guarda solicitudes
    try:
        with open(SOLICITUDES_CSV, "r", encoding="utf-8") as archivo:
            contenido = list(csv.DictReader(archivo))
            return contenido if contenido else []
    except FileNotFoundError:
        return []

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
    
def pedir_entero(mensaje, minimo=0):
    """Verifica que el número ingresado sea válido y persiste hasta que lo sea"""
    while True:
        try:            #solo es para validar los numero ingresados
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

def cambiar_estado_solicitud(id_solicitud, nuevo_estado):
    filas_actualizadas = []
    encontrado = False

    # 1. Leer el archivo completo y modificar la línea correspondiente
    with open(SOLICITUDES_CSV, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            # Si la fila no está vacía y el ID coincide (convertimos ambos a string por seguridad)
            if fila and str(fila[0]) == str(id_solicitud):
                fila[5] = nuevo_estado  # El índice 5 corresponde a la columna 'estado'
                encontrado = True
            filas_actualizadas.append(fila)

    # 2. Si se encontró y modificó, sobreescribimos el archivo con los nuevos datos
    if encontrado:
        with open(SOLICITUDES_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(filas_actualizadas)
    else:
        print(f"No se encontró la solicitud con ID {id_solicitud}")

    return id_solicitud