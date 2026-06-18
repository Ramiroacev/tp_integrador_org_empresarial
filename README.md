# Trabajo-Practico-Integrador-Organizacion Empresarial
Trabajo Práctico Integrador Final de Organización Empresarial - TUPaD - UTN

## Integrantes
* **Acevedo Ramiro** M26 C1-10
* **Nuñez Dario** M26 C1-26

## Descripción de las tablas
Las tablas se encuentran almacenadas dentro del directorio `/datos` y cuenta con los siguientes archivos:

* **empleados.csv:** Posee los datos de los empleado 20 en este caso.
* **solicitudes_licencias.csv:** Posee los datos de las licencias solicitadas por empleado y su estado.


## Estructura del Proyecto
- `main.py` → archivo principal desde donde se ejecuta el programa
- `principales.py` → posee la logica y funciones primarias del programa
- `auxiliares.py` → posee funciones complementarias del programa

## Instrucciones de Ejecución

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Ramiroacev/tp_integrador_org_empresarial.git
   ```

2. Ingresar a la carpeta del proyecto:

   ```bash
   cd tp_integrador_org_empresarial
   ```

3. Ejecutar el programa:

   ```bash
   python3 main.py
   ```

    El mismo generará un Menú interactivo con maquinas de estado
       -El sistema valida el legajo y muestra las licencias asociadas.
       -El usuario puede gestionar una licencia existente (pendiente, rechazada, reclamada) o iniciar una nueva.
       -Si la licencia está rechazada, se ofrece la opción de reclamar o crear una nueva solicitud.
       -Las fechas se validan para que sean reales (no se aceptan fechas inexistentes).
    
    ```=== [Estado: Inicio] ===
Bienvenido al Bot de Licencias Médicas.
Escriba 'iniciar' para comenzar la solicitud o 'salir': iniciar

=== [Estado: Buscando empleado] ===
Ingrese su número de legajo: 123
Hola Juan, vamos a verificar tus licencias

=== [Estado: Licencias del empleado] ===
Juan, estas son tus licencias:
- Licencia #1 | Estado: Aprobada | Fecha inicio: 20-06-2026 | Motivo: Neumonía
- Licencia #2 | Estado: Rechazada | Fecha inicio: 25-06-2026 | Motivo: Neumococo
Escriba el número de la licencia que quiere gestionar o 'nueva' para iniciar otra: 2

=== [Estado: Rechazada] ===
Lo sentimos Juan, tu solicitud fue rechazada.
Motivo del rechazo: No especificado
Escriba 'reclamar' para pedir reevaluación o 'nueva' para iniciar otra solicitud: reclamar

Tu solicitud fue marcada como 'Reclamada' y enviada nuevamente a RRHH.

=== [Estado: Solicitud en RRHH] ===
RRHH aún no ha revisado su solicitud.
Escriba 'verificar' para reintentar o 'cancelar' para desistir: verificar
    ```

## Requisitos
* ** Python 3

