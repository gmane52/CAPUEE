# IMPORTS: 
import serial
import time
import re

import requests

import schedule


# FUNCIONES: 
def Consulta_api_ElecMap():

    response = requests.get(
        "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=ES&temporalGranularity=5_minutes&emissionFactorType=direct",
        headers={
            "auth-token": f"ANLye3RJmgaNP2Hx8lsf"
        }
    )

    if response.status_code != 200:
        raise Exception("Error en la API:", response.text)
    
    data = response.json()
    global carbonIntensity 
    carbonIntensity = data["carbonIntensity"]

def read_serial():
    # Set up the serial port
    ser = serial.Serial('COM3', 9600, timeout=100)
    time.sleep(2)   # Wait for Arduino to initialize

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode(errors='ignore').strip()   # Read a line and decode

                # Use regex to find all numbers in the received line
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", line)

                # Print the extracted sensor values
                print(f"Extracted values: {numbers}")

    except KeyboardInterrupt:
        print("Program terminated by user.")
        ser.close()


# INIT:
carbonIntensity = None # Esto será una variable global
Consulta_api_ElecMap() # Inicializar variable carbonIntensity



# Configuration on ssheduled tasks
schedule.every(15).minutes.do(Consulta_api_ElecMap)

while True:
    schedule.run_pending()

    time.sleep(1)

    # Conectate a la API y actualiza el valor de la variable Tco2 (cada 15 minutos)(función que devactualiza directamente la variable global) -> OKKK

    # Leer los valores Serial (una función que devuelve los valores de Current y Temp.)
    # Logica de activación / desactivación del relé