import pandas as pd
import streamlit as st

df = pd.read_csv("curva_carga_sintetica_1dia_5min.csv")


# Line chart - best for trends over time
st.line_chart(df.set_index('timestamp')['TempSensor'])

# Bar chart - best for comparisons
st.bar_chart(df.set_index('timestamp')['CurrentSensor'])

# Area chart - best for cumulative/magnitude
st.area_chart(df.set_index('timestamp')[['CurrentSensor', 'TempSensor']])
