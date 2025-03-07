import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

"""
# Data Description
This dataset contains information about companies registered by the Business Integrity Commission (BIC) to collect and dispose of waste materials resulting exclusively from demolition, construction, alterations, or excavations in New York City.
Each record represents an entity approved to operate under the classification of Class 2 C&D Registrants. The information is updated daily and has been publicly available since April 4, 2017.

# Dictionary Column
| **Column Name**      | **Description**                                          | **API Field Name**    | **Data Type**        |
|----------------------|----------------------------------------------------------|----------------------|----------------------|
| **CREATED**          | Timestamp of when data is processed for OpenData         | `created`            | Floating Timestamp  |
| **BIC NUMBER**       | Unique BIC file number assigned to the entity            | `bic_number`         | Text                |
| **ACCOUNT NAME**     | Name of the entity                                       | `account_name`       | Text                |
| **TRADE NAME**       | Name under which the entity operates                     | `trade_name`         | Text                |
| **ADDRESS**          | Mailing address of the entity                            | `address`            | Text                |
| **CITY**            | City where the entity is located                         | `city`               | Text                |
| **STATE**            | State where the entity is located                        | `state`              | Text                |
| **POSTCODE**        | Postal code of the entity’s mailing address              | `postcode`           | Text                |
| **PHONE**           | Phone number of the entity                               | `phone`              | Text                |
| **EMAIL**           | Email contact of the entity                              | `email`              | Text                |
| **APPLICATION TYPE** | Type of application filed by the entity                  | `application_type`   | Text                |
| **DISPOSITION DATE** | Date of resolution of the application                   | `disposition_date`   | Text                |
| **EFFECTIVE DATE**   | Date when the registration becomes effective             | `effective_date`     | Text                |
| **EXPIRATION DATE**  | Date when the registration expires                       | `expiration_date`    | Text                |
| **RENEWAL**         | Indicates if the registration is renewable               | `renewal`            | Checkbox            |
| **EXPORT DATE**      | Date when the data was last exported by BIC              | `export_date`        | Floating Timestamp  |
| **LATITUDE**         | Latitude of the mailing address                          | `latitude`           | Text                |
| **LONGITUDE**        | Longitude of the mailing address                         | `longitude`          | Text                |
| **COMMUNITY BOARD**  | Community board based on the mailing address            | `community_board`    | Text                |
| **COUNCIL DISTRICT** | Council district where the entity is located            | `council_district`   | Text                |
"""

"""
# Data Description
This dataset provides information about school projects currently under construction in New York City, including new schools (Capacity) and Capital Improvement Projects (CIP).
The data is collected and maintained by the School Construction Authority (SCA) and is updated quarterly. It has been publicly available since October 9, 2011.

# Dictionary Column
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
| **Latitude**             | Latitude of the site location                         | `latitude`             | Number           |
| **Longitude**            | Longitude of the site location                        | `longitude`            | Number           |
"""


# Load data
@st.cache_data
def load_data(path):
    return pd.read_csv(path)


# Data files
DATA_PATH_1 = "filtered_data_march_clean.csv"
DATA_PATH_2 = "all_data.csv"

df1 = load_data(DATA_PATH_1)  # Construction waste collection sites
df2 = load_data(DATA_PATH_2)  # School construction projects


# Function to create maps
def create_map(data, icon, color):
    nyc_coordinates = [40.7128, -74.0060]  # Center of New York City
    mapa = folium.Map(location=nyc_coordinates, zoom_start=12, tiles="OpenStreetMap")

    for _, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"<b>{row.get('account_name', row.get('name', ''))}</b><br>{row.get('projdesc', '')}<br>Lat: {row['latitude']}, Lon: {row['longitude']}",
            tooltip=f"{row.get('account_name', row.get('name', ''))} ({row['latitude']}, {row['longitude']})",
            icon=folium.Icon(icon=icon, prefix="fa", color=color)
        ).add_to(mapa)

    return mapa


# Interface with tabs
tab1, tab2 = st.tabs(["Construction & Waste", "School Construction"])

with tab1:
    st.header("Interactive Map of Construction & Waste Collection Sites in NYC")
    st_folium(create_map(df1, icon="wrench", color="orange"), width=700, height=500)

with tab2:
    st.header("Interactive Map of School Construction Projects in NYC")
    st_folium(create_map(df2, icon="graduation-cap", color="blue"), width=700, height=500)