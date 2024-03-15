import pandas as pd
from datetime import datetime, timedelta
import folium
from folium.plugins import HeatMap
import base64
import numpy as np
from config import REEFOPS_DATA, MAP_WRITE_OUTPUT, ICON, DATE_STR_FORMAT, TILE_AREA, agents
import calendar
# Agents data should be in csv file and made to an Agent Class in the future



def format_date(date, date_format=DATE_STR_FORMAT):
    return datetime.strptime(date, date_format)

def get_month_str(date, short=False):
    if short:
        return calendar.month_abbr[date.month]
    else:
        return calendar.month_name[date.month]

def get_year(date,short=False):
    if short:
        return str(date.year)[2:]
    else:
        return str(date.year)

def time_stage_label(stage,date, date_format=DATE_STR_FORMAT):
    date=format_date(date,date_format=date_format)
    month= get_month_str(date,date_format)
    year=get_year(date,short=True)
    return f"{stage} | {month} '{year}"


def get_baseline_id(data):
    data=data[data.done==True]
    survey_ids=data.survey_id.unique()

    ids=[f"S{i}" for i in range(0,13)]    
    for id in ids:
        if id in survey_ids:
            return id

# Helper functions
def total_month(num_days):
    return num_days // 30


def remaining_day(num_days):
    return num_days % 30


def convert_dtime_date(date_time):
    return date_time.date()


def convert_dtime_days(date_time):
    if type(date_time) is timedelta:
        return date_time.days
    return 0


def format_date_df(date_df, str_format):
    date_df = pd.to_datetime(date_df, format=str_format)
    return pd.DataFrame(map(convert_dtime_date, date_df))[0]


def format_date_str(date, str_format):
    return datetime.strptime(date, str_format).date()

def readable_date(date):
    day=date.day
    month=calendar.month_name[date.month]
    year=date.year
    return f"{day} {month}, {year}"

def abbrv_name(name, format="first"):
    name= name.split(" ")
    first=name[0]
    last=name[1]
    f_initial=first[0]
    l_initial=last[0]

    if format =="first":
        return f"{f_initial}. {last}"

    if format == "last":
        return f"{first} {l_initial}."
    
class Survey:
    loaded_surveys = pd.read_csv(f"{REEFOPS_DATA}/surveys.csv")

    def __init__(self, site, survey_id=None, pytest=None):
        # get baseline id for site surveys
        survey_df_b = Survey.loaded_surveys[Survey.loaded_surveys['site_id'] == site.site_id]
        # Get Baseline Survey ID
        self.baseline_id = get_baseline_id(survey_df_b)
        # load Survey data file just for the first class instance
        if pytest is not None:
            Survey.loaded_surveys = pd.read_csv(f"{REEFOPS_DATA}/test_sample/surveys.csv")  # Read survey metadata
        if survey_id is None:
            self.survey_df = Survey.loaded_surveys[Survey.loaded_surveys['site_id'] == site.site_id]
            first_column = self.survey_df.pop('survey_id')
            # insert column using insert(position,column_name,
            # first_column) function
            self.survey_df.insert(0, 'survey_id', first_column)
        else:
            # self.survey_id_list = self.survey_df.survey_id.to_list()
            self.survey_id = survey_id
            self.survey_n = survey_id.replace("S", "").zfill(2)
            # Pass Survey dataframe for specific survey ID
            self.survey_df = Survey.loaded_surveys[(Survey.loaded_surveys.survey_id == survey_id) & (Survey.loaded_surveys.site_id == site.site_id)].iloc[0]
            self.baseline_survey_df = Survey.loaded_surveys[(Survey.loaded_surveys.survey_id == self.baseline_id) & (Survey.loaded_surveys.site_id == site.site_id)].iloc[0]
            self.client_code = self.survey_df['client_code']
            self.site_id = self.survey_df['site_id']
            self.survey_type = self.survey_df['survey_type']
            self.status = self.survey_df['status']
            
            self.start_date = format_date_str(self.survey_df.start_date, DATE_STR_FORMAT)
            self.end_date = format_date_str(self.survey_df.end_date, DATE_STR_FORMAT)
            self.report_date = format_date_str(self.survey_df.report_date, DATE_STR_FORMAT)
            self.report_date_str = readable_date(self.report_date)
            self.agents = self.survey_df['agents']
            self.transplanting = self.survey_df['transplanting']
            self.reef_check = self.survey_df['reef_check']
            self.sfm = self.survey_df['sfm']
            self.vid360 = self.survey_df['vid360']
            self.edna = self.survey_df['edna']
            self.dir = self.survey_df['dir']
            self.rc_path = self.survey_df['rc_path']
            self.sfm_path = self.survey_df['sfm_path']
            self.vid360_path = self.survey_df['vid360_path']
            self.remarks = self.survey_df['remarks']
            self.elapsed = (self.end_date - site.end_date).days
            # self.elapsed = list(map(convert_dtime_days, self.elapsed))
            self.months = total_month(self.elapsed)
            self.days = remaining_day(self.elapsed)
            self.end_date_str = readable_date(self.end_date)
           
            # NEEDS refactoring - include Agent class in ReefOps
            self.team = ", ".join([abbrv_name(agents[agt.strip()], "first") for agt in self.agents.split(",")])
            self.report_team = ",".join([abbrv_name(agents[agt.strip()], "first") for agt in self.survey_df.report_author.split(",")])

    def get_survey_id(self, survey_id):
        return self.survey_df[self.survey_df.survey_id == survey_id].iloc[0]  # get survey data
    # def status(self):
    #     # Quarterly Mitigations
    #     self.data[self.data.survey_type == "quarterly"]
    #     status_counts = self.data.status.value_counts().to_dict()
    #     print(status_counts)


# Archireef Site class - takes site metadata and builds a class
class Site:
    loaded_sites = pd.read_csv(f"{REEFOPS_DATA}/sites.csv")

    def __init__(self, site_id, pytest=None):
        # load Sites data file just for the first class instance
        if pytest is not None:
            Site.loaded_sites = pd.read_csv(f"{REEFOPS_DATA}/test_sample/sites.csv")  # Read site metadata
        self.site_id = site_id
        self.site_df = Site.loaded_sites[Site.loaded_sites['site_id'] == self.site_id].iloc[0]
        self.name = self.site_df['site_name']
        self.client = self.site_df['client_code']
        self.geo_code=self.site_df.geo_code
        self.tile_count = int(self.site_df['deployed_tiles'])
        self.frag = int(self.site_df['coral_frag'])
        self.locality = self.site_df['locality_name']
        self.lat = float(self.site_df['latitude'])
        self.lon = float(self.site_df['longitude'])
        self.start_date = format_date_str(self.site_df['start_date'], '%d/%m/%Y')
        self.end_date = format_date_str(self.site_df['end_date'], '%d/%m/%Y')
      
        self.end_date_str = readable_date(self.end_date)
   
        self.elapsed = (datetime.now().date() - self.start_date).days
        self.months = total_month(self.elapsed)
        self.days = remaining_day(self.elapsed)
        self.tile_area_m2 = round(TILE_AREA * self.tile_count)
        self.area_m2= int(self.site_df["area_m2"])
        self.surveys = Survey(self)
        
        # self.surveys = Survey(self,survey_id)
        # self.baseline_id=self.surveys.baseline_id
        # self.survey_data=self.surveys.loaded_surveys[self.surveys.loaded_surveys.site_id==self.site_id]
        

    def map(self, write_html=True):
        # CartoDB Positron
        icon = folium.features.CustomIcon(ICON, icon_size=(40, 40))

        map = folium.Map(location=[self.lat, self.lon], tiles="CartoDB Positron", zoom_start=11)
        folium.Marker([self.lat, self.lon],
                      icon=icon).add_to(map)
        folium.LayerControl().add_to(map)
        if write_html:
            map.save(MAP_WRITE_OUTPUT)
        else:
            return map
