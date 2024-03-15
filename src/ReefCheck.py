import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from ReefOps import Site, Survey, time_stage_label
from config import *
import datetime
import calendar


# Retrieve Reef Check data from all sites and consolidate into a single csv
# Used for preparing final Reef Check database
def reefcheck_db():
    rc_files = os.listdir(REEFCHECK_DATA)
    rc_files = [file for file in rc_files if "_RC.csv" in file]
    df_list = list()
    indicator_species = pd.read_csv(f"{REEFCHECK_DATA}/indicator_species.csv")
    for rc in rc_files:
        df = pd.read_csv(f"{REEFCHECK_DATA}/{rc}")
        df["site_id"] = rc.replace("_RC.csv", "")
        df_list.append(df)
    rc_db = pd.concat(df_list)
    rc_db.indicator = rc_db.species.apply(lambda sp: indicator_species.species.str.contains(str(sp)).any())
    rc_db.to_csv(f"{REEFCHECK_DATA}/reefcheck_db.csv", index=False)


def percent_change(control_state, current_state):
    return round((current_state - control_state) / control_state * 100)


def get_species_counts(species_name, location):
    c = location.groupby("species").sum()
    try:
        return int(c.loc[species_name]["count"])
    except:
        return 0


def simpsons_index(data):
    # Simpson's Index of Diversity formula
    # n = the total number of organisms of a particular species
    # N = the total number of organisms of all species

    n = data["count"].apply(lambda n: n * (n - 1)).sum()
    total_count = data["count"].sum()
    N = total_count * (total_count - 1)

    si = round(1 - (n / N), 2)
    return si


def eco_table(reefcheck_df, hive, control):
    species = list(reefcheck_df.species.unique())

    h_c = [get_species_counts(sp, hive) for sp in species]
    c_c = [get_species_counts(sp, control) for sp in species]

    eco_data = {
        'species': species,
        'hive': h_c,
        'control': c_c
    }
    return pd.DataFrame(eco_data)


# Calculate basic metrics function
def basic_metrics(reefcheck):
    reefcheck_df = reefcheck.reefcheck_df
    baseline_df = reefcheck.baseline_df
    hive = reefcheck.hive
    baseline_hive = reefcheck.baseline_hive
    control = reefcheck.control
    baseline_control = reefcheck.baseline_control

    # Calculate Basic Statistics
    species_c = reefcheck_df.groupby("treatment").count().species
    baseline_species_c = baseline_df.groupby("treatment").count().species

    hive_c = species_c.hive
    control_c = species_c.control
    hive_control_species_p = round((hive_c - control_c) / hive_c * 100)

    baseline_hive_c = baseline_species_c.hive
    baseline_control_c = baseline_species_c.control

    hive_si = simpsons_index(data=hive)  # Simpson's index for current state
    baseline_hive_si = simpsons_index(data=baseline_hive)  # Baseline index for baseline state
    hive_baseline_si_p = percent_change(baseline_hive_si, hive_si)
    # % Change from baseline
    hive_baseline_species_p = percent_change(baseline_hive_c, hive_c)

    # Count fish and invert species at Hive
    hive_fish_c = hive[hive.type == "Fish"].__len__()
    hive_invert_c = hive[hive.type == "Invert"].__len__()

    baseline_fish_c = baseline_hive[baseline_hive.type == "Fish"].__len__()
    baseline_invert_c = baseline_hive[baseline_hive.type == "Invert"].__len__()

    hive_a = int(hive["count"].sum())  # Total Abundance at Hive Site
    control_a = control["count"].sum()  # Total Abundance at Control Site
    baseline_hive_a = int(baseline_hive["count"].sum())  # Total Abundance at Baseline Hive Site
    baseline_control_a = baseline_control["count"].sum()  # Total Abundance at Baseline Control Site
    hive_baseline_a_p = percent_change(baseline_hive_a, hive_a)
    # Count fish and invert species at Control Site
    control_fish_c = control[control.type == "Fish"].__len__()
    control_invert_c = control[control.type == "Invert"].__len__()

    # Percentage difference in species and abundance between hive vs control
    fish_p = round((hive_fish_c - control_fish_c) / hive_fish_c * 100)
    invert_p = round((hive_invert_c - control_invert_c) / hive_invert_c * 100)
    hive_a_p = round((hive_a - control_a) / hive_a * 100)

    # Relative Abundance
    totals = reefcheck_df.groupby("treatment").sum()["count"]
    hive["ra"] = hive["count"] / totals.hive
    control["ra"] = control["count"] / totals.control
    ra = pd.concat([hive, control])
    ra = ra.groupby(["common_name", "treatment"]).sum().reset_index()[["common_name", "species", "treatment",  "site_id","survey_id","ra"]]

    output = dict(
        total_species_count=len(reefcheck_df.species.unique()),
        total_fish_count=len(reefcheck_df[reefcheck_df.type == "Fish"].species.unique()),
        total_invert_count=len(reefcheck_df[reefcheck_df.type == "Invert"].species.unique()),
        hive_c=hive_c,
        control_c=control_c,
        hive_control_species_p=hive_control_species_p,
        baseline_hive_c=baseline_hive_c,
        baseline_control_c=baseline_control_c,

        hive_baseline_species_p=hive_baseline_species_p,  # Percent change in  Unique species count compared to baseline
        hive_baseline_a_p=hive_baseline_a_p,  # Percent change in Total Abundance compared to baseline
        baseline_control_a=baseline_control_a,
        # Count fish and invert species at Hive
        hive_fish_c=hive_fish_c,
        hive_invert_c=hive_invert_c,

        hive_a=hive_a,  # Current Abundance at Hive
        baseline_hive_a=baseline_hive_a,  # Baseline abundance at hive

        hive_si=hive_si,
        baseline_hive_si=baseline_hive_si,
        hive_baseline_si_p=hive_baseline_si_p,
        # Count fish and invert species at Control Site
        control_fish_c=control_fish_c,
        control_invert_c=control_invert_c,

        # Total Abundance at Control Site
        control_a=control_a,

        # Percentage difference in species and abundance between hive vs control
        fish_p=fish_p,
        invert_p=invert_p,
        hive_a_p=hive_a_p,

        # Relative Abundance
        totals=totals,
        ra=ra
    )
    return output


def indicator_metrics(reefcheck):
    # Get current Survey Data
    current_df = reefcheck.reefcheck_df
    current_df = current_df[(current_df.indicator == True) & (current_df.treatment == "hive")]
    current_fish = current_df[current_df.type == "Fish"]
    current_invert = current_df[current_df.type == "Invert"]

    # Get Baseline Survey Data
    baseline_df = reefcheck.baseline_df
    baseline_df = baseline_df[(baseline_df.indicator == True) & (baseline_df.treatment == "hive")]
    baseline_fish = baseline_df[baseline_df.type == "Fish"]
    baseline_invert = baseline_df[baseline_df.type == "Invert"]

    # Get Indicator Species Data
    indicator_df = reefcheck.indicator_species
    indicator_fish = indicator_df[indicator_df.type == "Fish"]
    indicator_invert = indicator_df[indicator_df.type == "Invert"]

    output = dict(

        current_fish_count=len(current_fish),
        current_invert_count=len(current_invert),

        baseline_fish_count=len(baseline_fish),
        baseline_invert_count=len(baseline_invert),

        indicator_fish_count=len(indicator_fish),
        indicator_invert_count=len(indicator_invert),

        current_fish_p=round((len(current_fish) / len(indicator_fish)) * 100),
        current_invert_p=round((len(current_invert) / len(indicator_invert) * 100)),

        baseline_fish_p=round(len(baseline_fish) / len(indicator_fish) * 100),
        baseline_invert_p=round(len(baseline_invert) / len(indicator_invert) * 100)
    )
    return output


# Reef Check Statistics Class
# Reads the Reef Check Database (a concatenated CSV file) and pulls data for a given site or survey
class ReefCheck:
    loaded_db = pd.read_csv(f"{REEFCHECK_DATA}/reefcheck_db.csv")
    loaded_db.species = loaded_db.species.apply(lambda x: x.rstrip())
    indicator_species = pd.read_csv(f"{REEFCHECK_DATA}/indicator_species.csv")

    # Constructor to build ReefCheck for all survey of specific site
    # or for specific survey of a site
    def __init__(self, site_id, survey_id=None, pytest=None):
        if pytest is not None:
            ReefCheck.loaded_db = pd.read_csv(f"{REEFCHECK_DATA}/test_sample/reefcheck_db.csv")
        # print("Reef Check Database Imported")
        # print("================================================")
        # print(f"Rows: {len(self.db)}")
        if survey_id is None:
            self.reefcheck_df = ReefCheck.loaded_db[ReefCheck.loaded_db.site_id == site_id]

        else:
            self.survey_id = f"S{survey_id}"
            self.reefcheck_df = ReefCheck.loaded_db[
                (ReefCheck.loaded_db.site_id == site_id) & (ReefCheck.loaded_db.survey_id == survey_id)]

            # Initialize Site Class with passed Site ID
            self.site = Site(site_id=site_id)
            self.survey = Survey(site=self.site, survey_id=survey_id)
            # Get Indicator species list for Geographic code of Site
            geo_code = self.site.geo_code
            self.indicator_species = self.indicator_species[self.indicator_species[geo_code.lower()] == True]

            # Get Baseline Data
            self.baseline_df = ReefCheck.loaded_db[
                (ReefCheck.loaded_db.site_id == self.site.site_id) & (
                            ReefCheck.loaded_db.survey_id == self.survey.baseline_id)]

            # Get Data for Restoration (hive) and Control site
            self.hive = self.reefcheck_df[self.reefcheck_df.treatment == 'hive']
            self.control = self.reefcheck_df[self.reefcheck_df.treatment == 'control']

            # Get Eco Table and Metrics
            self.eco = eco_table(self.reefcheck_df, self.hive, self.control)
            self.baseline_hive = self.baseline_df[self.baseline_df.treatment == 'hive']
            self.baseline_control = self.baseline_df[self.baseline_df.treatment == 'control']
            self.metrics = basic_metrics(self)
            # self.baseline_metrics= basic_metrics(self.baseline_df,self.baseline_hive,self.baseline_control)

            self.indicator_metrics = indicator_metrics(self)

    # Bray-Curtis Dissimilarity Index
    ## Calculates the dissimilarity between hibe and the control site
    ## https://en.wikipedia.org/wiki/Bray%E2%80%93Curtis_dissimilarity
    def dissimilarity(self):
        eco = self.eco
        common = eco[(eco.hive != 0) & (eco.control != 0)]

        # cij = Lesser counts between common species
        cij = common[["hive", "control"]].apply(lambda x: x.min(), axis=1).sum()

        # s1 = Total number of specimens counted on Site 1 (hive)
        s1 = self.hive["count"].sum()
        # s2 = Total number of specimens counted on Site 2 (control)
        s2 = self.control["count"].sum()

        # Calculated Bray-curtis Dissimilarity
        bcij = round(1 - (2 * cij) / (s1 + s2), 2)
        self.metrics.update(dict(bcij=bcij))
        return bcij

    ## Jaccard Similarity = (number of observations in both sets) / (number in either set)
    ## https://en.wikipedia.org/wiki/Jaccard_index




    def similarity(self):
        eco = self.eco
        # Number of observations in both sets
        both = eco[(eco.hive != 0) & (eco.control != 0)].species.count()

        # Number of Observations in either Set
        s1_c = self.hive.species.count()
        s2_c = self.control.species.count()

        # Calculate Jaccard Similairty Index
        ji = round(both / (s1_c + s2_c), 2)
        self.metrics.update(dict(ji=ji))
        return ji

    # Find match species in survey species according to indicator species reference data
    def indicator_species_match(self):
        df1 = self.hive
        df1 = df1[df1.indicator == True]
        df2 = self.indicator_species
        common_values1 = df1['species'].isin(df2['species'])
        result_m1 = df1[common_values1]
        get_part1 = lambda x: x.split()[0]
        df1['species_p1'] = df1['species'].apply(get_part1)
        genus_species = df2.species.str.contains("spp.")
        genus_species = df2[genus_species]
        genus_species['species_p1'] = genus_species['species'].apply(get_part1)
        common_values2 = df1['species_p1'].isin(genus_species['species_p1'])
        result_m2 = df1[common_values2]
        match_species = pd.concat([result_m1, result_m2], ignore_index=True)
        match_species.rename(columns={"n": "count"}, inplace=True)
        match_species = match_species.astype({"count": int})
        match_species = match_species[['common_name', 'species', 'type', 'count']]
        indicator_final = df2[~(df2['species'].isin(result_m1['species']) | df2['species'].apply(get_part1).isin(
            result_m2['species_p1']))]
        indicator_final = indicator_final[['common_name', 'species', 'type']]
        indicator_final['count'] = 0
        indicator_final = pd.concat([match_species, indicator_final], ignore_index=True)
        indicator_final_dict = indicator_final.to_dict('records')
        return  indicator_final_dict



    # Stacked Bar plots comparing Hive and Control site - using Plotly library
    def compare_plot(self, write_html=True):
        # write_html if True, writes plots html file to the COMMUNITY_PLOT REEFCHECK_DATA, if false will plots the chart
        ra = self.metrics["ra"].sort_values("treatment")
        locality = self.site.locality
        x = [locality if x == "hive" else x.title() for x in ra.treatment]
      
        fig = px.bar(ra, x,
                     y="ra",
                     color="common_name",
                     pattern_shape="common_name",
                     text="common_name",
                     labels=dict(x="Site", ra="Relative Abundance (%)", common_name="Species"),
                     pattern_shape_sequence=PATTERNS,
                     color_discrete_sequence=COLORS,
                     )

        fig.update_layout(BAR_PLOT_LAYOUT)
        fig.update_layout(showlegend=False,
                          yaxis_tickformat=".0%",)
        fig.update_traces(width=0.5,
                          textfont_size=12,
                          marker=dict(line_color="grey", pattern_fillmode="replace")
                          )
        if write_html:
            fig.write_html(COMMUNITY_WRITE_OUTPUT)
        else:
            fig.show()

    # Plotting function for proportion of regional indicator species found from master list 
    def indicator_species_proportion(self, write_html=False):
        fish_p = self.indicator_metrics["current_fish_count"] / self.indicator_metrics["indicator_fish_count"]
        baseline_fish_p = self.indicator_metrics["baseline_fish_count"] / self.indicator_metrics["indicator_fish_count"]
        invert_p = self.indicator_metrics["current_invert_count"] / self.indicator_metrics["indicator_invert_count"]
        baseline_invert_p = self.indicator_metrics["baseline_invert_count"] / self.indicator_metrics[
            "indicator_invert_count"]

        fish_delta = 1 - fish_p
        baseline_fish_delta = 1 - baseline_fish_p
        invert_delta = 1 - invert_p
        baseline_invert_delta = 1 - baseline_invert_p

        data = dict(type=["fish", "fish", "invertebrates", "inverebtrates"],
                    percent=[fish_p, baseline_fish_p, invert_p, baseline_invert_p],
                    time_stage=["current", "baseline", "current", "baseline"])

        baseline_xlabel = time_stage_label("Baseline", self.survey.baseline_survey_df.end_date)
        current_xlabel = time_stage_label("Current", self.survey.survey_df.end_date)


        

        time_stage = [baseline_xlabel, current_xlabel]

        fig = go.Figure(data=[
            go.Bar(name='Fish', 
                   y=time_stage, 
                   x=[baseline_fish_p, fish_p], 
                   marker_color="#FBCD6F", 
                   text="Fish",
                   orientation="h"),
            go.Bar(name='Invertebrates', 
                   y=time_stage, 
                   x=[baseline_invert_p, invert_p], 
                   marker_color='#0B4B7A', 
                   orientation="h",
                   text="Invertebarates")
        ])
        # Change the bar mode
        fig.update_layout(barmode='group', 
                          xaxis_title='Proportion of Indicator Species',
                          yaxis_title="Time Stage",
                          xaxis_tickformat=".0%",
                          hovermode="y unified",
                          showlegend=False,
                          hoverlabel=dict( 
                                    bgcolor="white"
                            )
                          )

        fig.update_yaxes(tickangle=270)
        fig.update_layout(BAR_PLOT_LAYOUT)
        fig.update_layout(margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=5
        ),)

        if write_html:
            fig.write_html(INDICATOR_PROP_WRITE_OUTPUT)
        else:
            fig.show()

