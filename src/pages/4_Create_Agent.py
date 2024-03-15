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


st.set_page_config(page_title="Create Agent", page_icon="🌍")

st.markdown("# Create Agent")
st.divider()


#Get list of client names
client_names=clients.name

col1,col2=st.columns(2)
# Add a selectbox to the sidebar:

# Column 1 Content
first=col1.text_input(label="First Name")
last=col1.text_input(label="Last Name")
abbreviation=col1.text_input(label="Abbreviation")
job_title=col2.text_input(label="Job Title")
company=col2.text_input(label="Company Name")


# Columnt 2 Content




st.button("SUBMIT")