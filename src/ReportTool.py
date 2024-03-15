from ReefOps import *
from ReefCheck import *
from config import *
from reefsfm_plots import *
from dateutil.relativedelta import relativedelta

# Image Paths
site_img = f"{IMAGES}/site_img.jpg"
dpl_img = f"{IMAGES}/deployment.jpg"
indicators = f"{ASSETS}/images/indicator_species.png"
porites = f"{ASSETS}/images/porites.jpg"
siderastrea = f"{ASSETS}/images/siderastrea.jpg"
# Template Path
template_path = f"{ROOT}/src/report_template/new_template.html"


# Indicator Species Image Gallery Generator
def is_image_gallery_generator(species_dict):
    # Set image gallery html for each species type
    fish_image_gallery_html = "<div class='species-gallery__body' id='fish'>"
    invert_image_gallery_html = "<div class='species-gallery__body' id='invert'>"

    # Sort the species dictionary list according to count attribute
    species_dict.sort(key=lambda item: item['count'], reverse=True)

    # Add html elements according to attributes for image component
    for item in species_dict:
        fig_class = "species-item"
        count_html_component = ""
        # if item['present']:
        #     fig_class += " present"
        if item['count'] > 0:
            fig_class += " present"
            count_html_component += f"<span class='ribbon'>{item['count']}</span>"
        image_file = item['species'].replace(' ', '_').replace('.', '').lower()
        image_html_component = f"""
            <figure class="{fig_class}">
            <img src="./assets/images/species/{image_file}.jpg" alt="{item['species']}">
            <figcaption class="text-h4">{item['common_name']}</figcaption>
            <p class="text-body-4">{item['species']}</p>
            {count_html_component}</figure>
            """
        if item['type'].lower() == "fish":
            fish_image_gallery_html += image_html_component
        elif item['type'].lower() == "invert":
            invert_image_gallery_html += image_html_component

    fish_image_gallery_html += "</div>"
    invert_image_gallery_html += "</div>"
    return fish_image_gallery_html, invert_image_gallery_html


class ReportTool:
    def __init__(self, site_id, survey_id):
        self.name = "Archireef Report Tool v1.0"
        self.site_id = site_id
        self.survey_id = survey_id
        self.survey_id_int=int(self.survey_id.replace("S",""))

    def build_report(self):
        self.outpath = f"{REPORTS}/build_v2.0/report.html"
        # Get Data
        print(f"Retrieving Data for Site: {self.site_id}, Survey ID: {self.survey_id}")
        site = Site(site_id=self.site_id)
        site.map(write_html=True)
        survey = Survey(site=site, survey_id=self.survey_id)

        # Get Labels for baseline, current and target with dates included
        current_label=time_stage_label("Current", date=survey.survey_df.end_date)
        baseline_label=time_stage_label("Baseline", date=survey.baseline_survey_df.end_date)
        target_date = (site.end_date + relativedelta(years=15)).strftime("%d/%m/%Y")
        target_label=time_stage_label("Target", date=target_date)

        reefcheck = ReefCheck(self.site_id, self.survey_id)
        reefcheck.compare_plot(write_html=True)
        reefcheck.indicator_species_proportion(write_html=True)
        match_species = reefcheck.indicator_species_match()
        fish_image_gallery_html, invert_image_gallery_html = is_image_gallery_generator(match_species)
        # print(image_gallery_html)
        print("Building Report...")

        # Read ReefSFM data
        coral_metrics_db=pd.read_csv(CORAL_METRICS_DB, index_col=0).reset_index()
        current_coral_metrics=coral_metrics_db[(coral_metrics_db.survey_id == self.survey_id) & (coral_metrics_db.site_id == self.site_id)]
        baseline_coral_metrics=coral_metrics_db[(coral_metrics_db.survey_id == survey.baseline_id) & (coral_metrics_db.site_id == self.site_id)]
        # Composition plot based on coral metrics data
        composition_data = pd.concat([current_coral_metrics,baseline_coral_metrics],ignore_index=True)
        composition_plot(composition_data, write_html=True)
        # Survivorship plot
        survivorship_plot(current_coral_metrics,write_html=True)

        reef_metrics_db=pd.read_csv(REEF_METRICS_DB, index_col=0).reset_index()
        current_reef_metrics=reef_metrics_db[(reef_metrics_db.survey_id == self.survey_id) & (reef_metrics_db.site_id == self.site_id)].iloc[0]
        baseline_reef_metrics=reef_metrics_db[(reef_metrics_db.survey_id == survey.baseline_id) & (reef_metrics_db.site_id == self.site_id)].iloc[0]
        # Coral Projection plot based on reef metrics data
        coral_cover_data = reef_metrics_db[reef_metrics_db.site_id == self.site_id]
        model_coral_cover(coral_cover_data, forecast_period=10, write_html=True)

        # Retrieve ReefSFM Metrics required for Dashboard
        # Coral Composition Metrics
        genera_count=len(current_coral_metrics.taxa)
        colony_count=int(current_reef_metrics["count"])

        # Coral Cover Metrics
        current_coral_cover= current_reef_metrics.cover * 100
        baseline_coral_cover=baseline_reef_metrics.cover * 100
        coral_cover_delta = percent_change(baseline_coral_cover,current_coral_cover)
        current_coral_cover= round(current_coral_cover,1)
        baseline_coral_cover=round(baseline_coral_cover,1)
        coral_cover_target = COVER_TARGET * 100 

        current_coral_area_m2= current_reef_metrics.area_m2
        baseline_coral_area_m2=baseline_reef_metrics.area_m2
        coral_area_m2_delta = percent_change(baseline_coral_area_m2,current_coral_area_m2)
        coral_area_target = site.site_df.area_m2 * COVER_TARGET
        current_coral_area_m2= round(current_coral_area_m2,1)
        baseline_coral_area_m2=round(baseline_coral_area_m2,1)
        coral_cover_target = COVER_TARGET * 100


        # Coral Survivorship
        baseline_survivorship=round(baseline_reef_metrics.percent_healthy * 100) 
        current_survivorship=round(current_reef_metrics.percent_healthy * 100)
        survivorship_delta = current_survivorship - baseline_survivorship
        target_survivorship=SURIVORSHIP_TARGET

        # Rugosity
        baseline_rugosity= baseline_reef_metrics.site_rugosity.round(1)
        current_rugosity = current_reef_metrics.site_rugosity.round(1)
        rugosity_delta = percent_change(baseline_rugosity, current_rugosity)
        target_rugosity=round(baseline_rugosity + (baseline_rugosity * RUGOSITY_TARGET), 1)


        # GET EXP360 ID - should be dynamic in the future
        exp360_id = survey.survey_df.exp360_id
        # INSERT VARIABLES INTO HTML STRING
        with open(template_path, 'r') as f:
            html_template = f.read()
        html_template = html_template.format(
                                            site=site, 
                                            survey=survey, 
                                            survey_id_int=self.survey_id_int,
                                            current_label="Current",
                                            baseline_label="Baseline",
                                            target_label="Target",
                                            reefcheck=reefcheck,
                                            ARCHIREEF_LOGO=ARCHIREEF_LOGO, 
                                            CLIENT_LOGO=CLIENT_LOGO,
                                            colony_count=colony_count, 
                                            genera_count=genera_count,
                                            current_coral_cover=current_coral_cover,
                                            baseline_coral_cover=baseline_coral_cover,
                                            coral_cover_delta=coral_cover_delta,
                                            coral_cover_target=coral_cover_target,
                                            current_coral_area_m2=current_coral_area_m2,
                                            baseline_coral_area_m2=baseline_coral_area_m2,
                                            coral_area_m2_delta=coral_area_m2_delta,
                                            coral_area_target=coral_area_target,
                                            baseline_survivorship=baseline_survivorship,
                                            current_survivorship=current_survivorship,
                                            survivorship_delta=survivorship_delta,
                                            target_survivorship=target_survivorship,
                                            baseline_rugosity=baseline_rugosity,
                                            current_rugosity=current_rugosity,
                                            rugosity_delta=rugosity_delta,
                                            target_rugosity=target_rugosity,
                                            MAP_HTML=MAP_READ_HTML, CORAL_MAP_HTML=CORAL_MAP_READ_HTML,
                                            COMMUNITY_PLOT_HTML=COMMUNITY_READ_HTML,
                                            INDICATOR_PROP_PLOT=INDICATOR_PROP_READ_HTML,
                                            COMPOSITION_PLOT=COMPOSITION_READ_HTML,
                                            CORAL_COVER_PLOT=CORAL_COVER_READ_HTML,
                                            SURVIVORSHIP_PLOT=SURVIVORSHIP_READ_HTML,
                                            fish_image_gallery=fish_image_gallery_html,
                                            invert_image_gallery=invert_image_gallery_html,
                                            exp360_id=exp360_id, indicator_metrics=reefcheck.indicator_metrics)
        f = open(self.outpath, 'w')
        f.write(html_template)
        f.close()

        

        
