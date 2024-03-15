import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

# Get Operational data
clients=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\clients.csv')
sites=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\sites.csv')
surveys=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\surveys.csv')
agents=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\agents.csv')
indicator_species=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefcheck\indicator_species.csv')
species_db=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefcheck\species_db.csv')
countries=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\countries.csv', encoding = "ISO-8859-1")
agent_names=agents.full_name

site_ids=sites.site_id
sids=[f"S{n}" for n in range(0,14)]
count_list=[n for n in range(0,1001)]
area_size_list=[n for n in range(0,1001,5)]
# survey_methods=["Reef Check","Photogrammetry", "360 Video", "eDNA"]
project_types=["Reef Tiles","EcoSeaWall", "Site Assessment"]

st.set_page_config(page_title="Create Site", page_icon="🌍")

st.markdown("# Create Site")
st.divider()


#Get list of client names
client_names=clients.name

col1,col2=st.columns(2)


# Column 1 Content
site_id=col1.selectbox(label="Client", options=client_names)
site_name=col1.text_input(label="Project Name")
project_manager=col1.selectbox(label="Project Manager", options=agent_names)
project_type=col1.selectbox(label="Site Name", options=project_types)
start_date=col1.date_input(label="Deployment Start Date")
deployment_end_date=col1.date_input(label="Deployment End Date")
# site_data=sites[sites.site_id==site_id].iloc[0]
# start_date=col1.date_input(label="Start Date")
# survey_type=col1.selectbox(label="Survey Type", options=["quarterly", "bimonthly","annual"])

# Columnt 2 Content
site_id=col2.selectbox(label="Country", options=countries.name.to_list())
quantity=col2.selectbox(label="Quantity", options=count_list)
site_area_m2=col2.selectbox(label="Site Area (m2)", options=area_size_list)
locality_name=col2.text_input(label="Locality Name")
longitude = col2.text_input("Longitude",  placeholder="Longitude...", value="0.0000")
latitude = col2.text_input("Latitude", placeholder="Latitude...",  value="0.0000")


latitude=float(latitude)
longitude=float(longitude)

map_data = pd.DataFrame(dict(lat= [latitude],lon = [longitude]))
st.map(map_data)


st.button("SUBMIT")