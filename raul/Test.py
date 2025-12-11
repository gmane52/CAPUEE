#
# streamlit run Test.py
import streamlit as st
import pandas as pd
import requests
import json
from pprint import pprint
import matplotlib.pyplot as plt

st.title('ENCICLOPEDIA POKEMON')
st.write("Bienvenido a la gran enciclopedia Pokémon. Puedes preguntarme todo lo que necesites.")

base_URL = "https://pokeapi.co/api/v2/pokemon/"

pokemon = st.text_input("De qué Pokémon necesitas datos? ").strip().lower()

if pokemon:
    endpoint = base_URL + pokemon

    response = requests.get(endpoint)
    st.write(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        st.error("No encontré ese Pokémon. Verifica el nombre.")
        st.stop()

    data_json = response.json()
    data = response.json()
    sprite_url = data_json['sprites']['front_default']
    st.image(sprite_url, caption=pokemon.capitalize(), use_container_width=False)
tab1, tab2 = st.tabs(["Estadísticas", "Habilidades"])

#
#TAB ESTADÍSTICAS
#
with tab1:
    num_abilities = len(data_json["abilities"])
    st.write(f"{pokemon.capitalize()} tiene {num_abilities} habilidades:")
    abilities = data_json["abilities"]

    # Crear una columna por habilidad
    cols = st.columns(len(abilities))

    for i, hab in enumerate(abilities):
        nombre = hab["ability"]["name"]
        with cols[i]:
            st.metric(f"Habilidad {i + 1}", nombre)
#
#TAB ESTADÍSTICAS
#
with tab2:
        stats = data_json["stats"]
        nombres_stats = ["HP", "Ataque", "Defensa", "Ataque Especial", "Defensa Especial", "Velocidad"]

        cols = st.columns(len(stats))

        for i, stat in enumerate(stats):
            nombre_stat = nombres_stats[i] if i < len(nombres_stats) else f"Stat {i}"
            valor = stat["base_stat"]

            with cols[i]:
                st.metric(nombre_stat, valor)







