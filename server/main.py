# ----- IMPORTS ----- # 
import serial
import time
import re
import requests
import schedule
import csv
from datetime import datetime
import os


# ----- INIT ----- #
carbonIntensity = None 
CurrentSensor = None
TempSensor = None
rele = False # False = abierto

csv_file = "medidas.csv"


# ----- FUNCIONES ----- # 
def Consulta_api_ElecMap():
    global carbonIntensity 

    response = requests.get(
        "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=ES&temporalGranularity=5_minutes&emissionFactorType=direct",
        headers={
            "auth-token": f"ANLye3RJmgaNP2Hx8lsf" #TOKEN GUILLEM HARDCODED
        }
    )

    if response.status_code != 200:
        raise Exception("Error en la API:", response.text)
    
    data = response.json()
    carbonIntensity = data["carbonIntensity"]


def read_serial(ser):
    global CurrentSensor, TempSensor

    # Leer todas las líneas que haya en el buffer
    while ser.in_waiting > 0: # Comprovar que hay datos en bufer COM
        line = ser.readline().decode(errors='ignore').strip() #Lee todas las lineas, elimina espacios y convierte a texto
        if not line:
            continue

        # "CurrentSensor:123"
        if line.startswith("CurrentSensor:"):
            value_str = line.split(":", 1)[1]
            try:
                CurrentSensor = float(value_str)
                print(f"  -> CurrentSensor = {CurrentSensor}")
            except ValueError:
                print("  [ERROR] No pude convertir CurrentSensor a float.")

        # "TempSensor:123"
        if line.startswith("TempSensor:"):
            value_str = line.split(":", 1)[1]
            try:
                TempSensor = float(value_str)
                print(f"  -> TempSensor = {TempSensor}")
            except ValueError:
                print("  [ERROR] No pude convertir TempSensor a float.")

def ActivarRele():
    try:
        comando = "ACTIVATE_RELE\n"
        ser.write(comando.encode()) #Enviar como bytes para comunicaciones serial
    except Exception as e:
        print("#ERROR# no se ha podido escribir en el puerto serial: 'ACTIVATE_RELE'")

def DesactivarRele():
    try:
        comando = "DESACTIVATE_RELE\n"
        ser.write(comando.encode()) #Enviar como bytes para comunicaciones serial
    except Exception as e:
        print("#ERROR# no se ha podido escribir en el puerto serial: 'DESACTIVATE_RELE'")

def log_medida():
    global TempSensor, CurrentSensor, carbonIntensity, rele

    if TempSensor is None and CurrentSensor is None: # Porsi
        return

    timestamp = datetime.now().isoformat(timespec="seconds")

    with open(csv_file, "a", newline="") as f: # append
        writer = csv.writer(f)
        writer.writerow([timestamp, TempSensor, CurrentSensor, carbonIntensity, rele])


# ----- MAIN ----- #
## Abrir puerto serial y esperar un poco
ser = serial.Serial('COM11', 9600, timeout=1)
time.sleep(2)

## Inicializar valor carbonIntensity
Consulta_api_ElecMap() # Inicializar variable carbonIntensity

## Configuration on ssheduled tasks
schedule.every(15).minutes.do(Consulta_api_ElecMap)
schedule.every(5).minutes.do(log_medida)

## Crear archivo donde guardar las lecturas:
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "TempSensor", "CurrentSensor", "carbonIntensity", "ReleState"])

## Inicializa el rele para saber en que estado esta:
DesactivarRele()
rele = False # False = abierto

## BUCLE
while True:
    schedule.run_pending()
    
    read_serial(ser)
    if TempSensor is not None and TempSensor < 25:
        ActivarRele()
        rele = True

    if TempSensor is not None and TempSensor > 30:
        DesactivarRele()
        rele = False

    time.sleep(1) 

# Conectate a la API y actualiza el valor de la variable Tco2 (cada 15 minutos)(función que devactualiza directamente la variable global) -> OKKK

# Leer los valores Serial (una función que devuelve los valores de Current y Temp.)
# Logica de activación / desactivación del relé