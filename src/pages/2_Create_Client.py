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
# survey_methods=["Reef Check","Photogrammetry", "360 Video", "eDNA"]
project_types=["Reef Tiles","EcoSeaWall", "Site Assessment"]

st.set_page_config(page_title="Create Site", page_icon="🌍")

st.markdown("# Create New Client")
st.divider()


#Get list of client names
client_names=clients.name

col1,col2=st.columns(2)

# Column 1 Content
company_name=col1.text_input(label="Company Name")
company_name=col1.text_input(label="Client Code")
address=col1.text_input(label="Company Address")
contact_name=col1.text_input(label="Contact Name")

contact_no=col1.text_input(label="Contact Number")



# Columnt 2 Content
country=col2.selectbox(label="Country", options=countries.name.to_list())
city=col2.text_input(label="City")
contact_department=col2.text_input(label="Contact Department")
contact_email=col2.text_input(label="Contact email")
onboarded=col2.selectbox(label="Client Onboarded", options=["Yes", "No"])


st.button("SUBMIT")