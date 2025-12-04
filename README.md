# Academic Context

This project was developed within the framework of the Control and Automation for the Efficient Use of Energy (CAPUEE) course, coursed at the Universitat Politècnica de Catalunya (UPC) as part of the Master’s Degree in electric power systems and drives. The course focuses on the design, analysis, and implementation of automation systems aimed at improving energy efficiency.

Throughout the course, we acquired skills in rapid prototyping, data communication, visualization and API integration, and the development of innovative solutions that combine hardware and software to optimize energy use.

# Project Overview
## 1. Description
This project optimizes the energy use of a resistive heating system based on room temperature and the CO₂ emissions of the electrical grid.  
The system measures:
- Room temperature
- Electrical consumption
- Daily CO₂ emission levels (via HTTP request)

Heating is enabled only when necessary and when grid emissions are low enough to justify it.

## 2. Hardware Architecture
Main components:
- **ESP32**: Central controller. Reads sensors, makes decisions, and retrieves CO₂ data over Wi-Fi.
- **Hall-effect current sensor**: Measures load current via ESP32 ADC.
- **Temperature sensor**: Provides ambient temperature for comparison with heating thresholds.
- **Power relay**: Switches heater on/off based on control logic.
- **Power supply & protections**: 5 V isolated supply, fuse on phase line, proper physical isolation and enclosure.

## 3. Software Architecture
Two main tasks:
- **Control task** (continuous): Reads temperature and current, controls relay.
- **CO₂ acquisition task** (periodic): Performs HTTP requests and updates a shared CO₂ variable.

### Relay Logic
- Turn **ON** heater if `T < Tmin`.
- Turn **ON** heater if `Tmin ≤ T < Ttarget` **and** CO₂ emissions are below limit.
- Turn **OFF** heater if `T ≥ Ttarget`.

### Optional Features (time-dependent)
- Remote control and notifications via Telegram.
- Weekly usage report (energy, emissions, switching cycles) stored in non-volatile memory.

## 4. Implementation
- **Firmware language:** C++, python
- **Framework:** Arduino on ESP32


# IMPLEMENTATION 
## ESP32
- En un loop leer valor de corriente y escribirlo en serial como "CurrentSensor:XXX" (RL)
- En un loop leer valor de temperatura y escribirlo en serial como "TempSensor:XXX" (RL)

- En un loop buscara todo el rato "ACTIVATE_RELE" o "DESACTIVATE_RELE", y en cada caso activara o desactivara. (MS)

- (OPCIONAL) Enviar a TELEGRAM cambios de estado del rele, estilo: "Relé activado" o "Relé desactivado". (RL y MS)
- (OPCIONAL) Recibir de TELEGRAM comandos para cambiar el estado del relé. -> Se tiene que imprimir alguna cosa para que python lo sepa. (RL y MS)
- (OPCIONAL) Desde TELEGRAM enviar peticiones de lectura de temperatura y corriente (RL y MS)


## SERVER
- Leer en serial los valores de "CurrentSensor:XXX" y "TempSensor:XXX" (GM)
- Acceder a la API de ESIOS y actualizar una variable el valor de Tco2 generados por las tecnologias generadoras en ese momento. (MS)
- Existe una logica de activación y desactivacion de relés: (MS)
    - (OPCIONAL) Se desactiva durante X tiempo (1minuto) la logica si se activa/desactiva el relé por TELEGRAM.
    - Enviar por serie "ACTIVATE_RELE" o "DESACTIVATE_RELE" en base a esta logica

- Dashboards para activar/desactivar, observar historicos, etc.... (GM)
