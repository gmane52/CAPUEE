
sequenceDiagram
    autonumber

    participant Dashboard
    participant BotTelegram
    participant ESP32
    participant Algorithm

flowchart TD

    %% ===== ESP32 =====
    B["ESP32 Script start"]
    C["Measure and calculation
    Temperature and Current"]
    F["Serial
    Read / Write"]
    G["Configuration file
    Read / Write"]
    D{Action required?}
    E["Relay
    Activation / Deactivation"]

    %% ===== Flow =====
    B --> C
    C --> F
    F --> G
    G --> D
    D -->|No| B
    D -->|Yes| E
    E --> B

flowchart TD

    %% ===== Python Nodes =====
    A["Python Script starts"]
    B["Read configuration file"]
    C["Update Carbon Intensity
    via REST API"]
    D{Evaluate
    Temperature & Dashboard}
    E["Relay
    Activation / Deactivation"]
    F["Other actions"]

    %% ===== Flow =====
    A --> B
    B --> C
    C --> D
    D -->|Temp or Carbon Intensity trigger| E
    D -->|No| B
    E --> F



```mermaid
flowchart LR
%%{init: {'theme':'default'}}%%
    %% ================= ESP32 FLOW =================
    subgraph ESP32["ESP32 Flow"]
        ESP_B["ESP32 Script start"]
        ESP_C["Measure and calculation<br/>Temperature and Current"]
        ESP_F["Serial
        Read / Write"]
        ESP_G["Configuration file 
        Read / Write"]
        ESP_D{Action required?}
        ESP_E["Relay
        Activation / Deactivation"]

        ESP_B --> ESP_C
        ESP_C --> ESP_F
        ESP_F --> ESP_G
        ESP_G --> ESP_D
        ESP_D -->|No| ESP_B
        ESP_D -->|Yes| ESP_E
        ESP_E --> ESP_B
    end

    %% ================= PYTHON FLOW =================
    subgraph PY["Python Flow"]
        PY_A["Python Script starts"]
        PY_B["Read configuration file"]
        PY_C["Update Carbon Intensity 
        via REST API"]
        PY_D{Evaluate
        Temperature / Dashboard /
        Carbon intensity}
        PY_E["Relay 
        Activation / Deactivation"]

        PY_A --> PY_B
        PY_B --> PY_C
        PY_C --> PY_D
        PY_D -->|Temp or Carbon Intensity 
        trigger| PY_E
        PY_D -->|No| PY_B
        PY_E --> PY_A
    end




