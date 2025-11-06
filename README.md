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
- **Firmware language:** C++
- **Framework:** Arduino on ESP32
- **Version control:** GitHub with main directories `documentation/` and `code/`, branch coordination to avoid merge conflicts.
