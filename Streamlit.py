import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# Función para cargar datos desde un archivo CSV
def load_data(path):
    return pd.read_csv(path)

# Rutas de los archivos CSV
DATA_PATH_1 = "filtered_data_march_clean.csv"
DATA_PATH_2 = "all_data.csv"

# Cargar los datos
df1 = load_data(DATA_PATH_1)
df2 = load_data(DATA_PATH_2)

# Función para crear un mapa
def create_map(data):
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

# Crear pestañas
tab1, tab2 = st.tabs(["📊 Filtered Data (March)", "🗺️ All Data"])

# Contenido de la pestaña 1
with tab1:
    st.header("Filtered Data (March) - Description")
    st.write("""
    This dataset provides information about school projects currently under construction in New York City 
    that have been filtered for March. It includes new schools (Capacity) and Capital Improvement Projects (CIP).
    The data is collected and maintained by the School Construction Authority (SCA).
    """)

    st.markdown("""
    ### Dictionary Column
    | **Column Name**       | **Description**                                              | **API Field Name**      | **Data Type**      |
    |----------------------|----------------------------------------------------------|----------------------|-------------------|
    | **School Name**           | Name of the school                                      | `name`                 | Text             |
    | **BoroughCode**           | Borough code where the school is located              | `boro`                 | Text             |
    | **Geographical District** | District where the school is located                  | `geo_dist`             | Number           |
    | **Project Description**   | Description of the construction work                  | `projdesc`             | Text             |
    | **Construction Award**    | Value of the prime construction contract              | `award`                | Number           |
    | **Project Type**         | Identifies whether the project is **CIP** or **Capacity** | `constype`             | Text             |
    | **Building ID**           | Unique identifier of the building                     | `buildingid`           | Text             |
    | **Building Address**      | Address of the building under construction            | `building_address`     | Text             |
    | **City**                 | City where the project is located                      | `city`                 | Text             |
    | **Borough**              | Name of the borough where the school is located       | `borough`              | Text             |
    | **Latitude**             | Latitude of the site location                         | `latitude`             | Number           |
    | **Longitude**            | Longitude of the site location                        | `longitude`            | Number           |
    """)

    st.header("Filtered Data (March) - Map")
    st_folium(create_map(df1), width=700, height=500)

# Contenido de la pestaña 2
with tab2:
    st.header("All Data - Description")
    st.write("""
    This dataset provides information about all school projects currently under construction in New York City.
    It includes new schools (Capacity) and Capital Improvement Projects (CIP). 
    The data is collected and maintained by the School Construction Authority (SCA).
    """)

    st.markdown("""
    ### Dictionary Column
    | **Column Name**       | **Description**                                              | **API Field Name**      | **Data Type**      |
    |----------------------|----------------------------------------------------------|----------------------|-------------------|
    | **School Name**           | Name of the school                                      | `name`                 | Text             |
    | **BoroughCode**           | Borough code where the school is located              | `boro`                 | Text             |
    | **Geographical District** | District where the school is located                  | `geo_dist`             | Number           |
    | **Project Description**   | Description of the construction work                  | `projdesc`             | Text             |
    | **Construction Award**    | Value of the prime construction contract              | `award`                | Number           |
    | **Project Type**         | Identifies whether the project is **CIP** or **Capacity** | `constype`             | Text             |
    | **Building ID**           | Unique identifier of the building                     | `buildingid`           | Text             |
    | **Building Address**      | Address of the building under construction            | `building_address`     | Text             |
    | **City**                 | City where the project is located                      | `city`                 | Text             |
    | **Borough**              | Name of the borough where the school is located       | `borough`              | Text             |
    | **Latitude**             | Latitude of the site location                         | `latitude`             | Number           |
    | **Longitude**            | Longitude of the site location                        | `longitude`            | Number           |
    """)

    st.header("All Data - Map")
    st_folium(create_map(df2), width=700, height=500)
