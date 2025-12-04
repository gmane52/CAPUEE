import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

import serial
import time
import re

# Archvio con funciones:

def Consulta_api_esios(API_KEY=None):
    # Abrir archivo con el token para no hardcodearlo
    ruta = r"C:\Users\figol\Documents\03. github\Personal\03. DevOps\TOKEN_ESIOS.txt"
    with open (ruta,"r",encoding="utf-8") as f:
        API_KEY = f.read()

    # ENDPOINTS
    API_BASE = "https://api.esios.ree.es"

    # Headers
    HEADERS = {
        "Accept": "application/json; application/vnd.esios-api-v1+json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        }
    
    ahora = datetime.now(timezone.utc)
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)

    ayer = ahora - timedelta(days=1)
    inicio_ayer = ayer.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_ayer = ayer.replace(hour=23, minute=59, second=59, microsecond=0)
    
    params = {
    "start_date": inicio_ayer.isoformat(timespec="seconds"),
    "end_date": fin_ayer.isoformat(timespec="seconds"),
    "time_trunc": "hour",
    "geo_ids[]": 1,    # 1 = sistema peninsular
    }
    
    url = f"{API_BASE}/indicators/{10355}"
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()

    valores = r.json()["indicator"]["values"]

    if not valores:
        print("No hay datos disponibles para hoy todavía.")
        return

    ultimo = valores[-1]

    print("Última hora publicada:")
    print("Datetime:", ultimo["datetime"])
    print("CO₂:", ultimo["value"], ultimo.get("value_units", ""))

    return ultimo

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

