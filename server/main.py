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
TEMP_ON = 25
TEMP_OFF = 30
carbonIntensityMAX = 10
CONTROL = "AUTO"
MANUAL_RELE_STATE = False


csv_file = "server/medidas.csv"


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

def ActivarRele(ser):
    try:
        comando = "H\n"
        ser.write(comando.encode()) #Enviar como bytes para comunicaciones serial
    except Exception as e:
        print("#ERROR# no se ha podido escribir en el puerto serial: 'ACTIVATE_RELE'")

def DesactivarRele(ser):
    try:
        comando = "L\n"
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
ser = serial.Serial('COM7', 115200, timeout=1)
time.sleep(2)

## Inicializar valor carbonIntensity
Consulta_api_ElecMap() # Inicializar variable carbonIntensity

## Configuration on ssheduled tasks
schedule.every(15).minutes.do(Consulta_api_ElecMap)
schedule.every(5).seconds.do(log_medida)

## Crear archivo donde guardar las lecturas:
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "TempSensor", "CurrentSensor", "carbonIntensity", "ReleState"])

## Inicializa el rele para saber en que estado esta:
DesactivarRele(ser)
time.sleep(2)
rele = False # False = abierto

## BUCLE
while True:
    try:
        with open("server/config.txt") as f:
            for line in f:
                line = line.strip()
                if line.startswith("TEMP_ON="):
                    TEMP_ON = float(line.split("=", 1)[1])
                elif line.startswith("TEMP_OFF="):
                    TEMP_OFF = float(line.split("=", 1)[1])
                elif line.startswith("CONTROL="):
                    CONTROL = line.split("=",1)[1].strip()
                elif line.startswith("MANUAL_RELE_STATE="):
                    MANUAL_RELE_STATE = line.split("=",1)[1].strip() == "TRUE"
                elif line.startswith("CARBON_INTENSITY_MAX="):
                    carbonIntensityMAX = float(line.split("=", 1)[1])
    except:
        pass

    schedule.run_pending()
    read_serial(ser)

    # manual control
    if CONTROL == "MANUAL":
        if MANUAL_RELE_STATE and not rele:
            ActivarRele(ser)
            rele = True

        elif not MANUAL_RELE_STATE and rele:
            DesactivarRele(ser)
            rele = False

    # auto control
    else:
        if TempSensor is not None and TempSensor < TEMP_ON and not rele:
            ActivarRele(ser)
            rele = True

        elif TempSensor is not None and TempSensor > TEMP_OFF and rele:
            DesactivarRele(ser)
            rele = False

        if carbonIntensity is not None and carbonIntensity < carbonIntensityMAX and rele:
            DesactivarRele(ser)
            rele = False

    time.sleep(1)
