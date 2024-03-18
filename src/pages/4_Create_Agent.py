import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import os.path as path


root =  path.abspath(path.join(__file__ ,"../../.."))

# Get Operational data
clients=pd.read_csv(f'{root}/data/reefops/clients.csv')



st.set_page_config(page_title="Create Agent", page_icon="🌍")

st.markdown("# Create Agent")
st.divider()

# Function to structure all data into dictionary
def get_data():
    data=dict(
        first_name=first,
        last_name=last,
        abbreviation=abbreviation,
        job_title=job_title,
        company=company
    )

    # Write Data to DB....
    print(data)
    st.write(data)

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

cont=st.container(border=True)
st.button("SUBMIT", on_click=get_data)