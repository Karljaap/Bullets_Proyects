import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# Configurar la página
st.set_page_config(page_title="NYC School Projects", layout="wide")

# Función para cargar datos desde un archivo CSV
def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return None

# Rutas de los archivos CSV
DATA_PATH_1 = "filtered_data_march_clean.csv"
DATA_PATH_2 = "all_data.csv"

# Cargar los datos
df1 = load_data(DATA_PATH_1)
df2 = load_data(DATA_PATH_2)

# Función para crear un mapa
def create_map(data):
    if data is None or data.empty:
        return folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    nyc_coordinates = [40.7128, -74.0060]  # Centro de Nueva York
    mapa = folium.Map(location=nyc_coordinates, zoom_start=12, tiles="OpenStreetMap")

    for _, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<b>{row['name']}</b><br>{row['projdesc']}<br>Lat: {row['latitude']}, Lon: {row['longitude']}",
            tooltip=f"{row['name']} ({row['latitude']}, {row['longitude']})",
            icon=folium.Icon(icon="graduation-cap", prefix="fa", color="blue")
        ).add_to(mapa)

    return mapa

# Cambiar tabs por botones de selección
selected_tab = st.radio("Seleccione un conjunto de datos:", ["📊 Filtered Data (March)", "🗺️ All Data"])

# Mostrar contenido según la selección
if selected_tab == "📊 Filtered Data (March)":
    st.subheader("Filtered Data (March) - Description")
    st.write("""
    This dataset provides information about school projects currently under construction in New York City 
    that have been filtered for March. It includes new schools (Capacity) and Capital Improvement Projects (CIP).
    The data is collected and maintained by the School Construction Authority (SCA).
    """)

    st.write("")  

    st.markdown("""
    ### Dictionary Column
    | **Column Name**       | **Description**                                              |
    |----------------------|----------------------------------------------------------|
    | **School Name**           | Name of the school                                      |
    | **BoroughCode**           | Borough code where the school is located              |
    | **Geographical District** | District where the school is located                  |
    | **Project Description**   | Description of the construction work                  |
    | **Construction Award**    | Value of the prime construction contract              |
    | **Project Type**         | Identifies whether the project is **CIP** or **Capacity** |
    """)

    st.write("")  # Espaciado

    st.subheader("Filtered Data (March) - Map")
    st_folium(create_map(df1), width=700, height=500)

elif selected_tab == "🗺️ All Data":
    st.subheader("All Data - Description")
    st.write("""
    This dataset provides information about all school projects currently under construction in New York City.
    It includes new schools (Capacity) and Capital Improvement Projects (CIP). 
    The data is collected and maintained by the School Construction Authority (SCA).
    """)

    st.write("")  # Espaciado

    st.markdown("""
    ### Dictionary Column
    | **Column Name**       | **Description**                                              |
    |----------------------|----------------------------------------------------------|
    | **School Name**           | Name of the school                                      |
    | **BoroughCode**           | Borough code where the school is located              |
    | **Geographical District** | District where the school is located                  |
    | **Project Description**   | Description of the construction work                  |
    | **Construction Award**    | Value of the prime construction contract              |
    | **Project Type**         | Identifies whether the project is **CIP** or **Capacity** |
    """)

    st.write("")  # Espaciado

    st.subheader("All Data - Map")
    st_folium(create_map(df2), width=700, height=500)
