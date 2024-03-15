import streamlit as st


import numpy as np
import pandas as pd
from ReefOps import time_stage_label
from streamlit_calendar import calendar
from config import DATE_STR_FORMAT
import calendar
import datetime



st.set_page_config(page_title="ReefOps Tool", layout="wide",page_icon="🌍")

# Function to get survey data for pretty view
def get_survey_content(sdata):
    output=sdata.apply(lambda x: x.to_dict(), axis = 1).to_list()
    output = [dict(zip(x.keys(),x.values())) for x in output]
    return output

def format_bool(bool):
   if bool == True:
       return ":white_check_mark:"
   else:
       return ":x:"

regions=["United Arab Emirates", "Hong Kong"]


# Get Operational data
clients=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\clients.csv')
clients=clients[(clients.onboarded==True) & (clients.reeftiles==True)]
sites=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\sites.csv')
surveys=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\surveys.csv')
surveys["start_dt"]=pd.to_datetime(surveys.start_date,format=DATE_STR_FORMAT)
surveys["end_dt"]=pd.to_datetime(surveys.end_date,format=DATE_STR_FORMAT)
#Get list of client names
client_names=clients.name



# Add a selectbox to the sidebar:
client_selection = st.sidebar.selectbox(
      'Select Client',
      client_names
   )

selected_client=clients[clients.name==client_selection].iloc[0]
selected_site=sites[sites.client_code == selected_client.client_code].iloc[0]
selected_survey=surveys[surveys.site_id == selected_site.site_id]

st.header(f"{selected_client["name"]}")
st.divider()

cl_col1,cl_col2,cl_col3 = st.columns([1,1,3])
cl_col1.subheader("Address")

address=selected_client.address.split(",")
for ad in address:
   cl_col1.write(ad)

cl_col2.subheader("Primary Contact")
cl_col2.write(selected_client.contact_name)
cl_col2.write(selected_client.contact_department)
cl_col2.write(selected_client.primary_mobile_no)
cl_col2.write(selected_client.primary_email)
#    st.write(selected_client.region)



st.divider()
st.header(f"Site: {selected_site.site_id}")
st.subheader(selected_site.site_name)

st.divider()

col1, col2, col3 = st.columns([1,1,3])

# Column 1 content
col1.metric(label="Deployment Type" , value=selected_site["type"].replace("_", " ").title())
col1.metric(label="Locality:" , value=selected_site.locality_name)
col1.metric(label="Country" , value=selected_site.country)
col1.metric(label="City" , value=selected_site.city)

# Column 2 content
col2.metric(label="Start Date" , value=selected_site.start_date)
col2.metric(label="End Date" , value=selected_site.end_date)
col2.metric(label="Project Area" , value=f"{int(selected_site.area_m2)} m2")
col2.metric(label="Quantity" , value=int(selected_site.quantity))

# Column 3 content
map_data = pd.DataFrame(dict(lat= [selected_site.latitude],lon = [selected_site.longitude]))
col3.map(map_data)


st.divider()
st.header(f"Survey Information")
st.divider()
col1, col2 = st.columns(2)

completed_surveys=selected_survey[selected_survey.done == True].sort_values("end_dt", ascending = True).reset_index(drop=True)
upcoming_surveys=selected_survey[selected_survey.done == False].sort_values("start_dt").reset_index(drop=True)

last_survey=completed_surveys.iloc[-1]
last_survey_date=time_stage_label(last_survey.survey_id, last_survey.end_date)

next_survey=upcoming_surveys.iloc[0]
next_survey_date=time_stage_label(next_survey.survey_id, next_survey.start_date)

col1.metric(label="Completed Surveys", value=len(completed_surveys))
col1.metric(label=f"Last Survey", value=last_survey_date)


col2.metric(label="Remaining Surveys", value=len(upcoming_surveys))
col2.metric(label=f"Next Survey", value=next_survey_date)
st.divider()
st.subheader(":white_check_mark: Completed Surveys")
st.write("")

# Pull tab content from server
completed_surveys_content = get_survey_content(completed_surveys)
# Create tabs
n_cols = len(completed_surveys_content)
cols = st.columns(n_cols)
 
# Iterate through each tab and build content
for col, s_content in zip(cols, completed_surveys_content):
    with col:
        date = s_content['end_dt']
        cont=col.container(border=True)
        cont.header(s_content['survey_id'])
        cont.subheader(f"{date.day} {calendar.month_abbr[date.month]}, {date.year}")
        cont.markdown(f"**{s_content["survey_type"].title()}**")
        cont.write(s_content["agents"])
        cont.markdown(f"{format_bool(s_content["reef_check"])} **ReefCheck**")
        cont.markdown(f"{format_bool(s_content["sfm"])} **Photogrammetry**")
        cont.markdown(f"{format_bool(s_content["vid360"])} **360 Video:**")

st.divider()
st.subheader(":date: Upcoming Surveys")
st.write("")


# Pull tab content from server
upcoming_surveys_content = get_survey_content(upcoming_surveys[upcoming_surveys.start_date.isnull() == False].head())
# Create tabs
n_cols = len(upcoming_surveys_content)
cols = st.columns(n_cols)
 
now = datetime.datetime.now()
# Iterate through each tab and build content
for col, s_content in zip(cols, upcoming_surveys_content):
    with col:
        date = s_content['start_dt']
        cont=col.container(border=True)
        cont.header(s_content['survey_id'])
        cont.subheader(f"{date.day} {calendar.month_abbr[date.month]}, {date.year}")
        cont.markdown(f"**{s_content["survey_type"].title()}**")
        
        time_delta = date- now
        cont.write(f"{time_delta.days} remaining days")
      #   cont.markdown(f"{format_bool(s_content["reef_check"])} **ReefCheck**")
      #   cont.markdown(f"{format_bool(s_content["sfm"])} **Photogrammetry**")
      #   cont.markdown(f"{format_bool(s_content["vid360"])} **360 Video:**")



 





