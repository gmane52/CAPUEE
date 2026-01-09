import pandas as pd
import streamlit as st

st.markdown(
    "<h2 style='text-align:center;'>Main dashboard</h2>",
    unsafe_allow_html=True
)

if "show_more_1" not in st.session_state:
    st.session_state.show_more_1 = False

if "show_more_2" not in st.session_state:
    st.session_state.show_more_2 = False

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
        st.text("Nombre dispositivo")


# ============================================================================
# TABS
# ============================================================================
with st.container(border=True):
    st.subheader("Energy Use")
    tab1, tab2 = st.tabs(["**Today**", "**Last Month**"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric("Time on", "17.65 h")

        with col2:
            col2.metric("Energy used", "123 kWh")

        with col3:
            col3.metric("Actual power", "230 kW")
    
        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button("show more", use_container_width=True, key="show_more_btn_1"):
                st.session_state.show_more_1 = not st.session_state.show_more_1
        
        if st.session_state.show_more_1:
            with st.container(border=True):
                st.subheader("Caja")
                st.write("Contenido dentro del recuadro")

                df = pd.read_csv("curva_carga_sintetica_1dia_5min.csv")

                st.line_chart(df.set_index('timestamp')['TempSensor'])
                st.bar_chart(df.set_index('timestamp')['CurrentSensor'])
                st.area_chart(df.set_index('timestamp')[['CurrentSensor', 'TempSensor']])

    with tab2:      
        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric("Time on", "277.65 h")

        with col2:
            col2.metric("Energy used", "1223 kWh")

        with col3:
            col3.metric("Actual power", "230 kW")

        left, center, right = st.columns([1, 2, 1])
        with center:
            if st.button("show more", use_container_width=True, key="show_more_btn_2"):
                st.session_state.show_more_2 = not st.session_state.show_more_2
        
        if st.session_state.show_more_2:
            with st.container(border=True):
                st.subheader("Caja")
                st.write("Contenido dentro del recuadro")

                df = pd.read_csv("curva_carga_sintetica_1dia_5min.csv")

                st.line_chart(df.set_index('timestamp')['TempSensor'])
                st.bar_chart(df.set_index('timestamp')['CurrentSensor'])
                st.area_chart(df.set_index('timestamp')[['CurrentSensor', 'TempSensor']])


# ============================================================================
# Actions
# ============================================================================
with st.container(border=True):
    st.subheader("Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚡Activate/Desactivate", use_container_width=True):
            st.success("Botón pulsado")

    with col2:
        if st.button("🗓️ Timer", use_container_width=True):
            st.success("Botón pulsado")

    with col3:
        if st.button("⚙️ Settings", use_container_width=True):
            st.success("Botón pulsado") 
