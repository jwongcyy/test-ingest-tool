import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import *
from ReefOps import time_stage_label
import pandas as pd
# ReefSFM Plots

def composition_plot(data_df, write_html=False):
    data_df = data_df.sort_values("survey_id")
    xlabels=["Baseline", "Current"]
    sids=data_df.survey_id.unique()
    dates=data_df.date.unique()
    xlabels=[time_stage_label(xl, date, date_format="%Y-%m-%d") for xl,date in zip(xlabels, dates)]

    xlabel_map=dict(zip(sids,xlabels))
    data_df["xlabel"]=[xlabel_map[sid] for sid in data_df.survey_id]

    fig = px.bar(data_df, 
                 x="xlabel", 
                 y="composition", 
                 color="taxa", 
                 pattern_shape="taxa",
                 text="taxa",
                 barmode="stack",
                 hover_data=dict(taxa=False,xlabel=False),
                 color_discrete_sequence=COLORS, 
                 pattern_shape_sequence=PATTERNS,
                 labels=dict(x="Time Stage", 
                             y="Composition (%)", 
                             composition="Composition")
                             
                    )
    
    fig.update_traces(
                textfont_size=15,
                width=0.5,
                marker=dict(
                        line_color="grey", 
                        pattern_fillmode="replace"
                        ),
            
                     )

    fig.update_layout(
                barmode='stack',
                yaxis_title='Composition (%)',
                xaxis_title="Time Stage",
                yaxis_tickformat=".0%",
                hovermode="x",
                showlegend=False
            )

    fig.update_layout(BAR_PLOT_LAYOUT)

    if write_html:
        fig.write_html(COMPOSITION_WRITE_OUTPUT)
    else:
        return fig

def survivorship_plot(data_df,write_html=False):

    data=[]
    labels=[]
    taxa=[]
    healthy= [x for x in data_df.percent_healthy]
    healthy_l= ["healthy" for x in data_df.percent_healthy]
    bleached= [x for x in data_df.percent_bleached]
    bleached_l= ["bleached" for x in data_df.percent_bleached]
    dead= [x for x in data_df.percent_dead]
    dead_l= ["dead" for x in data_df.percent_dead]

    data.extend(healthy)
    data.extend(bleached)
    data.extend(dead)
    labels.extend(healthy_l)
    labels.extend(bleached_l)
    labels.extend(dead_l)

    for i in range(0,3):
        taxa.extend(data_df.taxa.to_list())
    data_df=pd.DataFrame(dict(taxa=taxa,value=data,status=labels))
    
    colors = COLORS[0:len(data_df)]
    patterns = ["", "x", "/"]


    fig = px.bar(
                data_df, 
                x="taxa", 
                y="value", 
                color="taxa", 
                pattern_shape="status",
                hover_data=dict(taxa=False,),
                color_discrete_sequence=colors, 
                pattern_shape_sequence=patterns,
                labels=dict(x="Coral Genus", 
                             y="Survivorship (%)",
                             status="Status",
                             value="Value",
                             taxa="Coral Genus")
                 )
    
    fig.update_layout(
                hovermode="x unified",
                yaxis_title='Survivorship (%)',
                xaxis_title="Coral Genus",
                yaxis_tickformat=".1%",
                showlegend=False,
                hoverlabel=dict( 
                    bgcolor="white"
                    )
    )
    fig.update_traces(
                width=0.5,
                marker=dict(
                line_color="grey", 
                pattern_fillmode="replace")
                        )
    
    fig.update_layout(BAR_PLOT_LAYOUT)
    fig.update_layout(font=dict(family="Lexend"))
    if write_html:
        fig.write_html(SURVIVORSHIP_WRITE_OUTPUT)
    else:
        return fig


def model_coral_cover(data, forecast_period=10, write_html=False):
    data.date = [datetime.strptime(date, "%Y-%m-%d") for date in data.date]
    cover_data = data.cover
    start_date = data.date[0]
    total_months = forecast_period * 4
    end_date = start_date + relativedelta(months=total_months)
    quaterly = [start_date + relativedelta(months=3 * m) for m in range(1, round(total_months), 3)]
    quaterly.insert(0, start_date)
    data = data.sort_values("survey_id")

    base = data.cover[0]  # Attain baseline data

    rate = 0.03  # Coral cover increase rate: 2-4%/yr (Lourey et al. 2000)
    monthly_rate = rate / 12

    start_year = data.year[0]
    end_year = start_year + forecast_period

    years = list(range(start_year, end_year))

    def month_diff(date1, date2):
        days_delta = (date2 - date1).days
        return days_delta / 30

    modelled_cover = data.cover.to_list()
    base = modelled_cover[-1]
    dates = quaterly[:len(data) - 1]

    # Different scenarios with 5% & 1% coral cover increase rate (modify according to +/- 1.5 °C or w/o intervention or ...)
    rate_high = 0.05 / 12
    rate_low = 0.01 / 12
    scenario1 = [cover * (1 + rate_high) ** month_diff(start_date, quarter) for cover, quarter in
                 zip(modelled_cover, dates)]
    scenario2 = [cover * (1 + rate_low) ** month_diff(start_date, quarter) for cover, quarter in
                 zip(modelled_cover, dates)]

    modelled_dates = quaterly[len(data) - 2:]

    modelled_cover.extend([base * (1 + monthly_rate) ** month_diff(start_date, quarter) for quarter in
                           modelled_dates])  # Assume consistent recovery

    scenario1.extend([base * (1 + rate_high) ** month_diff(start_date, quarter) for quarter in modelled_dates])
    scenario2.extend([base * (1 + rate_low) ** month_diff(start_date, quarter) for quarter in modelled_dates])

    fig = go.Figure([
        go.Scatter(
            name='10-yr Projection',
            x=quaterly,
            y=modelled_cover,
            mode='markers+lines',
            line=dict(color='#0B4B7A'),
            # hovertemplate = "%{y:.00%}"

        ),
        go.Scatter(
            name='Current State',
            x=data['date'],
            y=data['cover'],
            mode='lines+markers',
            line=dict(color='#FBC85F'),
            # hovertemplate = "%{y:.00%}",
            marker=dict(size=15)
        ),
        go.Scatter(
            name='+1.5 degree C',
            x=quaterly,
            y=scenario1,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
            # hovertemplate = "%{y:.00%}"
        ),
        go.Scatter(
            name='-1.5 degree C',
            x=quaterly,
            y=scenario2,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(169, 185, 216, 0.3)',
            fill='tonexty',
            showlegend=False,
            # hovertemplate = "%{y:.00%}"
        )
    ])

    # fig.add_vline(x="2026-03-01",
    #                 line_dash="dash", line_color="#B5684C", opacity=1, line_width=2,
    #                 annotation_text="End of 3rd year", annotation_position="top right",)
    fig.update_layout(
        yaxis_title='Coral Cover',
        yaxis_tickformat=".2%",
        hovermode="x"
    )
    fig.update_layout(BAR_PLOT_LAYOUT)
    fig.layout.template = 'simple_white'

    if write_html:
        fig.write_html(CORAL_COVER_WRITE_OUTPUT)
    else:
        return fig