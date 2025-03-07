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

# Define NYC bounding box for filtering data
NYC_BOUNDS = {
    "lat_min": 40.4774,  # Southernmost point
    "lat_max": 40.9176,  # Northernmost point
    "lon_min": -74.2591,  # Westernmost point
    "lon_max": -73.7004  # Easternmost point
}


def filter_nyc_data(data):
    return data[
        (data['latitude'] >= NYC_BOUNDS['lat_min']) &
        (data['latitude'] <= NYC_BOUNDS['lat_max']) &
        (data['longitude'] >= NYC_BOUNDS['lon_min']) &
        (data['longitude'] <= NYC_BOUNDS['lon_max'])
        ]


df1 = filter_nyc_data(df1)
df2 = filter_nyc_data(df2)


# Function to create maps
def create_map(data, color):
    nyc_coordinates = [40.7128, -74.0060]  # Center of New York City
    mapa = folium.Map(location=nyc_coordinates, zoom_start=12, tiles="OpenStreetMap",
                      max_bounds=True,
                      min_lat=NYC_BOUNDS['lat_min'], max_lat=NYC_BOUNDS['lat_max'],
                      min_lon=NYC_BOUNDS['lon_min'], max_lon=NYC_BOUNDS['lon_max'])

    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=6,
            popup=f"<b>{row.get('account_name', row.get('name', 'Unknown'))}</b><br>Lat: {row['latitude']}, Lon: {row['longitude']}",
            tooltip=f"{row.get('account_name', row.get('name', 'Unknown'))} ({row['latitude']}, {row['longitude']})",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
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
    st.write("""
    ## Data Description

    This dataset contains information about companies registered by the Business Integrity Commission (BIC) to collect and dispose of waste materials resulting exclusively from demolition, construction, alterations, or excavations in New York City.

    Each record represents an entity approved to operate under the classification of Class 2 C&D Registrants. The information is updated daily and has been publicly available since April 4, 2017.

    ## Dictionary 


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
    | **CENSUS TRACT**     | Census tract associated with the mailing address        | `census_tract`      | Text                |
    | **BIN**             | Building Identification Number (BIN)                     | `bin`                | Text                |
    | **BBL**             | Borough-Block-Lot (BBL) number                           | `bbl`                | Text                |
    | **NTA**             | Neighborhood Tabulation Area                             | `nta`                | Text                |
    | **BORO**            | Borough where the entity is located                      | `boro`               | Text                |

    """)
    st_folium(create_map(df1, color="orange"), width=700, height=500)

elif selected_tab == "School Projects":
    st.subheader("School Construction Projects in NYC")
    st.write("""
    ## Data Description

    This dataset provides information about school projects currently under construction in New York City, including new schools (Capacity) and Capital Improvement Projects (CIP).

    The data is collected and maintained by the School Construction Authority (SCA) and is updated quarterly. It has been publicly available since October 9, 2011.

    ## Dictionary 

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
    | **Community Board**      | NYC community district associated with the site      | `community_board`      | Number           |
    | **Council District**     | NYC City Council district where the site is located  | `community_council`    | Number           |
    | **BIN**                 | Building Identification Number (BIN)                  | `bin`                  | Number           |
    | **BBL**                 | Borough, Block, and Lot number (BBL)                  | `bbl`                  | Number           |
    | **Census Tract (2020)**  | Census tract where the site is located (Census 2020) | `census_tract`         | Number           |
    | **Neighborhood Tabulation Area (NTA) (2020)** | NYC Neighborhood Tabulation Area (Census 2020) | `nta`                  | Text             |
    | **Location 1**           | System-generated column for mapping representation   | `location_1`           | Location         |

    """)
    st_folium(create_map(df2, color="blue"), width=700, height=500)
