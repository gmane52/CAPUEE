import pandas as pd
import streamlit as st
import datetime as dt
import time

st.markdown(
    "<h2 style='text-align:center;'>Main dashboard</h2>",
    unsafe_allow_html=True
)

## SETUP 
if "show_more_1" not in st.session_state:
    st.session_state.show_more_1 = False

if "show_more_2" not in st.session_state:
    st.session_state.show_more_2 = False

if "show_more_3" not in st.session_state:
    st.session_state.show_more_3 = False

# Nombre dispositivo
device_name = "Mi dispositivo"
try:
    with open("server/config.txt") as f:
        for line in f:
            if line.startswith("DEVICE_NAME"):
                device_name = line.split("=", 1)[1].strip()
except:
    pass

from streamlit_autorefresh import st_autorefresh
# esto esta guai pero genera lag
# st_autorefresh(interval=1000, key="refresh")

# Preparacion dataframe:
@st.cache_data(ttl=5)  # en “tiempo real” pon 1–5s
def load_and_prepare(path: str):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    V = 230.0
    df["dt_s"] = df["timestamp"].diff().dt.total_seconds().clip(lower=0).fillna(0)
    df["power_W"] = V * df["CurrentSensor"]
    df["energy_Wh"] = df["power_W"] * (df["dt_s"] / 3600)

    df["on_dt_s"] = df["dt_s"].where(df["ReleState"], 0)
    df["on_energy_Wh"] = df["energy_Wh"].where(df["ReleState"], 0)
    return df

df = load_and_prepare("medidas_sinteticas_2semanas.csv")

# --- filtrar por hoy y este mes ---
now = pd.Timestamp.now()

df_today = df[df["timestamp"].dt.date == now.date()]
df_month = df[(df["timestamp"].dt.year == now.year) & (df["timestamp"].dt.month == now.month)]

def resumen(d):
    time_on_h = d["on_dt_s"].sum() / 3600
    energy_on_kwh = d["on_energy_Wh"].sum() / 1000
    return time_on_h, energy_on_kwh

time_total_h, energy_total_kwh = resumen(df)
time_today_h, energy_today_kwh = resumen(df_today)
time_month_h, energy_month_kwh = resumen(df_month)

def graficar(datos):
    d = datos.set_index("timestamp")
    d = d.resample("5min").mean(numeric_only=True)

    st.write("Tiempo ON/OFF")
    st.line_chart(d["ReleState"])  # 0/1

    st.write("Power")
    st.line_chart(d["power_W"])

    st.write("carbon Intensity")
    st.line_chart(d["carbonIntensity"])


# ============================================================================
#  Intro dispositivo
# ============================================================================

with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
       st.image(
        "C:/Users/figol/Documents/03. github/CAPUEE/server/testImagen.png",
        width=150
        )
    
    with col2:
        st.text(device_name)


# ============================================================================
# TABS
# ============================================================================
with st.container(border=True):
    st.subheader("Energy Use")
    tab1, tab2, tab3 = st.tabs(["**Today**", "**Last Month**", "**Total**"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric("Time ON ", f"{time_today_h:.2f} h")

        with col2:
            col2.metric("Energy used", f"{energy_today_kwh:.3f} kWh")

        with col3:
            current = df["CurrentSensor"].iloc[-1]
            power = current * 230
            col3.metric("Actual power", f"{power:.0f} W")
    
        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button("show more", use_container_width=True, key="show_more_btn_1"):
                st.session_state.show_more_1 = not st.session_state.show_more_1
        
        if st.session_state.show_more_1:
            with st.container(border=True):
                graficar(df_today)


    with tab2:      
        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric("Time ON ", f"{time_month_h:.2f} h")

        with col2:
            col2.metric("Energy used", f"{energy_month_kwh:.3f} kWh")

        with col3:
            current = df["CurrentSensor"].iloc[-1]
            power = current * 230
            col3.metric("Actual power", f"{power:.0f} W")

        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button("show more", use_container_width=True, key="show_more_btn_2"):
                st.session_state.show_more_2 = not st.session_state.show_more_2
        
        if st.session_state.show_more_2:
            with st.container(border=True):
                graficar(df_month)

    with tab3:
        col1, col2, col3 = st.columns(3)

        with col1:
            col1.metric("Time ON", f"{time_total_h:.2f} h")

        with col2:
            col2.metric("Energy used", f"{energy_total_kwh:.3f} kWh")

        with col3:
            current = df["CurrentSensor"].iloc[-1]
            power = current * 230
            col3.metric("Actual power", f"{power:.0f} W")

    
        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button("show more", use_container_width=True, key="show_more_btn_3"):
                st.session_state.show_more_1 = not st.session_state.show_more_1
        
        if st.session_state.show_more_1:
            with st.container(border=True):
                graficar(df)


# ============================================================================
# Actions
# ============================================================================
# init
# ============================================================================
# Actions
# ============================================================================

with st.container(border=True):
    st.subheader("Actions")
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("⚡ Activate / Deactivate", expanded=False):
                         
            if st.button("Activate", use_container_width=True):
                st.success("Botón pulsado")
            
            if st.button("Desactivate", use_container_width=True):
                st.success("Botón pulsado")

    with col2:
        with st.expander("⚙️ Settings", expanded=False):

            device_name = st.text_input("Device Name", placeholder="Example: TV room device")
            temp_on = st.number_input("Temp ON", value=25.0, step=0.5)
            temp_off = st.number_input("Temp OFF", value=30.0, step=0.5)
            carbon_intensity_max = st.number_input("Carbon intensity max", value=10.0, step=0.5)

            if st.button("Apply settings", use_container_width=True):
                with open("server/config.txt", "w") as f:
                    f.write(f"DEVICE_NAME={device_name}\n")
                    f.write(f"TEMP_ON={temp_on}\n")
                    f.write(f"TEMP_OFF={temp_off}\n")
                    f.write(f"CARBON_INTENSITY_MAX={carbon_intensity_max}\n")
                st.success("Settings applied")

            if st.button("‼️ Erase dataset ‼️", use_container_width=True):
                st.success("Done!")

# ============================================================================
# Settings
# ============================================================================




        
