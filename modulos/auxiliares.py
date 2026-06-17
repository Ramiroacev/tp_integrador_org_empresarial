#funciones complementarias
from pathlib import Path

# Proyecto portable en Windows y Linux
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas
ARCHIVO_CSV = BASE_DIR / "datos" / "listado_empleado.csv"

def lectura_csv():    
    try:                 #intenta tener acceso al archivo con los datos
        with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo, delimiter=';'))   #se utiliza el delimitador ; ya que el csv esta con ese valor
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ARCHIVO_CSV}' en el directorio actual.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return []

    
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

