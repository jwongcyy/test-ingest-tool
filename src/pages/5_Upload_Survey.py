import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

# Get Operational data
clients=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\clients.csv')
clients=clients[(clients.onboarded==True) & (clients.reeftiles==True)]
sites=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\sites.csv')
surveys=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\surveys.csv')
agents=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefops\agents.csv')
indicator_species=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefcheck\indicator_species.csv')
species_db=pd.read_csv(r'C:\Users\medo_\PycharmProjects\Ops-Dashboard\data\reefcheck\species_db.csv')

agent_names=agents.full_name
sids=[f"S{n}" for n in range(0,14)]
site_ids=sites.site_id

survey_methods=["Reef Check","Photogrammetry", "360 Video", "eDNA", "BRUV","Benthic Transect"]

dive_log_data=list()

def add_dive():

    dive_data=dict(
        date= dive_date,
        agents=dive_agents,
        start_time=dive_start_time,
        end_time=dive_end_time,
        max_depth=float(dive_max_depth),
        min_temp=float(dive_min_temp),
        max_temp=float(dive_max_temp),
        substrate_type=dive_substrate_type,
        remarks=dive_remarks,
    )
    print(dive_data)
    dive_log_data.append(dive_data)


st.set_page_config(page_title="Upload Survey Data", layout="wide",page_icon="🌍")

st.markdown("# Upload Survey Data")
st.sidebar.header("Upload Survey Data")
st.divider()


#Get list of client names
client_names=clients.name

col1,col2=st.columns(2)
col1.subheader("Survey Metadata")
col2.subheader("Dive Logs")

survey_metadata=st.container(border=True)
sm_col1,sm_col2=survey_metadata.columns(2)


# Column 1 Content
site_id=sm_col1.selectbox(label="Site ID", options=site_ids)
site_data=sites[sites.site_id==site_id].iloc[0]

survey_type=sm_col2.selectbox(label="Survey Type", options=["assessment","quarterly", "bimonthly","annual"])

if survey_type == "assessment":
    sids=["SA"]
else:
    sids=[f"S{n}" for n in range(0,14)]

survey_id=sm_col1.selectbox(label="Survey ID", options=sids)
start_date=sm_col1.date_input(label="Start Date")

methods=survey_metadata.multiselect(label="Survey Methods", options=survey_methods)


# Columnt 2 Content

agents=sm_col2.multiselect(label="Agents", options=agent_names)

end_date=sm_col2.date_input(label="End Date")

survey_metadata.divider()
transplanting=survey_metadata.toggle('Transplanting Implemented')
transplanting=survey_metadata.toggle('New Baseline')
st.divider()

st.subheader("Dive Logs")

dive_container = st.container(border=True)
dl_col1, dl_col2, dl_col3 = dive_container.columns(3)

dive_date=dl_col1.date_input(label="Date")
dive_agents=dl_col1.multiselect(label="Divers", options=agent_names)
dive_start_time=dl_col1.time_input(label="Start Time")
dive_end_time=dl_col1.time_input(label="End Time")

dive_max_depth=dl_col2.number_input(label="Max Depth (m)", value=0.0)
dive_min_temp=dl_col2.number_input(label="Min Temp (C)", value =0.0)
dive_max_temp=dl_col2.number_input(label="Max Temp (C)", value=0.0)

dive_substrate_type=dl_col2.text_input(label="Substrate Type")
dive_remarks=dl_col3.text_area(label="Remarks")

rc_done=dive_container.toggle('Reef Check')

if rc_done:
    rc_container = dive_container.container(border=True)
    rc_col1,rc_col2 = dive_container.columns(2)
 
    rc_col1.subheader("Hive Metadata")
    rc_hive_start_time=rc_col1.time_input(label="Hive Start Time")
    rc_hive_end_time=rc_col1.time_input(label="Hive End Time")
    # rc_hive_duration = rc_hive_end_time - rc_hive_start_time
    rc_hive_depth=rc_col1.number_input(label="Hive Max Depth (m)", value=0.0)
    rc_hive_temperature=rc_col1.number_input(label="Hive Temp (C)", value=0.0)
    rc_hive_visibility_m=rc_col1.number_input(label="Hive Visibility (C)", value=0.0)
    rc_hive_divers=dive_agents=rc_col1.multiselect(label="Hive Divers", options=agent_names)

    rc_col2.subheader("Control Metadata")
    rc_control_start_time=rc_col2.time_input(label="Control Start Time")
    rc_control_end_time=rc_col2.time_input(label="Control End Time")
    # rc_control_duration = rc_control_end_time - rc_control_start_time
    rc_control_depth=rc_col2.number_input(label="Control Max Depth (m)", value=0.0)
    rc_control_temperature=rc_col2.number_input(label="Control Temp (C)", value=0.0)
    rc_control_visibility_m=rc_col2.number_input(label="Control Visibility (C)", value=0.0)
    rc_control_divers=rc_col2.multiselect(label="Control Divers", options=agent_names)
    


add_button=dive_container.button("ADD", on_click=add_dive())

if add_button:
    dive_log_df=pd.read_csv("logs.csv")
    dive_log_df = pd.concat([dive_log_df,pd.DataFrame(dive_log_data)])
    dive_log_df.to_csv("logs.csv")
    st.write(dive_log_df)

st.divider()
# Reef Check Data Upload
st.header("ReefCheck Data")

geo_code=site_data.geo_code.lower()
df=pd.DataFrame(index=[n for n in range(0,101)], columns=["species","treatment","count","min_length_cm","max_length_cm","mean_length_cm"])
df["species"] = ""
df["treatment"]=""
df["count"] = 0 
df["min_length_cm"] = 0 
df["max_length_cm"] = 0 
df["mean_length_cm"] = 0 


species_list=species_db.species
count_list=[n for n in range(0,1001)]

hive_data=st.data_editor(
    df,
    column_config={
        "species": st.column_config.SelectboxColumn(
            "Species",
            help="The category of the app",
            width="medium",
            options=species_list,
            required=False,
        ),
        "count": st.column_config.SelectboxColumn(
            "Count",
            help="The category of the app",
            width="small",
            options=count_list,
            required=False,
        ),
        "treatment": st.column_config.SelectboxColumn(
            "Treatment",
            help="The category of the app",
            width="medium",
            options=["Hive", "Control"],
            required=False,
        ),
        "min_length_cm": st.column_config.SelectboxColumn(
            "Min Length (cm)",
            help="The category of the app",
            width="medium",
            options=count_list,
            required=False,
        ),
        "max_length_cm": st.column_config.SelectboxColumn(
            "Max Length (cm)",
            help="The category of the app",
            width="medium",
            options=count_list,
            required=False,
        ),
        "mean_length_cm": st.column_config.SelectboxColumn(
            "Mean Length (cm)",
            help="The category of the app",
            width="medium",
            options=count_list,
            required=False,
        )
    },
    hide_index=False,
    key="hive"
)

st.header("360 Video")

exp360_id=st.text_input(label="EXP360 Video ID")

st.button("SUBMIT")