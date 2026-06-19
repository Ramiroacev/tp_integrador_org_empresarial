from modulos.auxiliares import inicializar_archivos
from modulos import principales

  

if __name__ == "__main__":
    inicializar_archivos()
    
    # Comenzamos con la función de inicio
    estado_actual = principales.estado_inicio
    
    # El bucle ejecuta la función actual, recibe la SIGUIENTE función, y repite
    # hasta que alguna función devuelva 'None' (como al escribir 'salir')
    while estado_actual is not None:
        estado_actual = estado_actual()