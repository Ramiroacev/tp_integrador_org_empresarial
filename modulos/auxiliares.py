#funciones complementarias
from pathlib import Path
import csv
# Proyecto portable en Windows y Linux
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas
EMPLEADOS_CSV = BASE_DIR / "datos" / "empleados.csv"

def lectura_csv_empleados():    
    try:                 #intenta tener acceso al archivo con los datos
        with open(EMPLEADOS_CSV, "r", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo, delimiter=';'))   #se utiliza el delimitador ; ya que el csv esta con ese valor
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

