import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium


# Load the CSV data files
def load_data(path):
    return pd.read_csv(path)


# File paths (Make sure the CSV files are in the same directory as this script)
DATA_PATH_1 = "filtered_data_march_clean.csv"
DATA_PATH_2 = "all_data.csv"

df1 = load_data(DATA_PATH_1)
df2 = load_data(DATA_PATH_2)


# Function to create maps
def create_map(data, icon, color):
    nyc_coordinates = [40.7128, -74.0060]  # Center of New York City
    mapa = folium.Map(location=nyc_coordinates, zoom_start=12, tiles="OpenStreetMap")

    for _, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<b>{row.get('account_name', row.get('name', 'Unknown'))}</b><br>Lat: {row['latitude']}, Lon: {row['longitude']}",
            tooltip=f"{row.get('account_name', row.get('name', 'Unknown'))} ({row['latitude']}, {row['longitude']})",
            icon=folium.Icon(icon=icon, prefix="fa", color=color)
        ).add_to(mapa)

    return mapa


# Streamlit app
st.set_page_config(page_title="NYC Construction Maps", layout="wide")
st.title("Interactive Maps of NYC Construction")

# Sidebar navigation
st.sidebar.title("Navigation")
selected_tab = st.sidebar.radio("Select a category:", ["Construction Companies", "School Projects"])

if selected_tab == "Construction Companies":
    st.subheader("Construction Companies in NYC")
    st_folium(create_map(df1, icon="wrench", color="orange"), width=700, height=500)

elif selected_tab == "School Projects":
    st.subheader("School Construction Projects in NYC")
    st_folium(create_map(df2, icon="graduation-cap", color="blue"), width=700, height=500)