from flask import render_template
from initialize import initialize_dir_year, initialize_dir_region, get_amountallyr
from statistics import mean
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import math

dict_scbaa = {"Region": {
    "ARMM": ['Isabela', 'Lamitan', 'Marawi'],
    "CAR": ['Baguio', 'Tabuk'],
    "NCR": ['Caloocan', 'Las Piñas', 'Makati', 'Malabon', 'Mandaluyong', 'Manila', 'Marikina', 'Muntinlupa', 'Navotas', 'Parañaque', 'Pasay', 'Pasig', 'Quezon', 'San Juan', 'Taguig', 'Valenzuela'],
    "NIR": ['Bacolod', 'Bago', 'Bais', 'Bayawan', 'Cadiz', 'Canlaon', 'Dumaguete', 'Escalante', 'Guihulngan', 'Himamaylan', 'Kabankalan', 'Sagay', 'San Carlos', 'Sipalay', 'Talisay', 'Tanjay', 'Victorias'],
    "Region 1": ['Batac', 'Laoag', 'Alaminos', 'Dagupan', 'San Carlos', 'Urdaneta', 'San Fernando', 'Candon', 'Vigan'],
    "Region 2": ['Tuguegarao', 'Cauayan', 'Ilagan', 'Santiago'],
    "Region 3": ['Balanga', 'Malolos', 'Meycauayan', 'San Jose Del Monte', 'Cabanatuan', 'Gapan', 'Muñoz', 'Palayan', 'San Jose', 'Angeles', 'San Fernando', 'Mabalacat', 'Tarlac', 'Olongapo'],
    "Region 4A": ['Batangas', 'Lipa', 'Santo Tomas', 'Tanauan', 'Bacoor', 'Cavite', 'Dasmariñas', 'General Trias', 'Imus', 'Tagaytay', 'Trece Martires', 'Biñan', 'Cabuyao', 'Calamba', 'San Pablo', 'San Pedro', 'Santa Rosa', 'Lucena', 'Tayabas', 'Antipolo'],
    "Region 4B": ['Calapan', 'Puerto Princesa'],
    "Region 5": ['Legazpi', 'Ligao', 'Tabaco', 'Iriga', 'Naga', 'Masbate', 'Sorsogon'],
    "Region 6": ['Iloilo', 'Passi', 'Passi'],
    "Region 7": ['Tagbilaran', 'Carcar', 'Bogo', 'Cebu', 'Danao', 'Lapu-lapu', 'Mandaue', 'Naga', 'Toledo', 'Talisay'],
    "Region 8": ['Calbayog', 'Baybay', 'Borongan', 'Catbalogan', 'Maasin', 'Ormoc', 'Tacloban'],
    "Region 9": ['Zamboanga', 'Dapitan', 'Dipolog', 'Pagadian'],
    "Region 10": ['Tangub', 'Cagayan de Oro', 'El Salvador', 'Gingoog', 'Iligan', 'Malaybalay', 'Oroquieta', 'Ozamiz', 'Valencia'],
    "Region 11": ['Digos', 'Davao', 'Samal', 'Panabo', 'Mati', 'Tagum'],
    "Region 12": ['Koronadal', 'Cotabato', 'General Santos', 'Kidapawan', 'Tacurong'],
    "Region 13": ['Bayugan', 'Bislig', 'Butuan', 'Cabadbaran', 'Surigao', 'Tandag']},
    "Year": initialize_dir_year()
}
# GENERATE DEFAULT FIGURES FUNCTION


def generate_default_figs():
    year = initialize_dir_year()
    region = initialize_dir_region()
    # Graph 1 WATERFALL CHART function call
    fig, insights = get_surplus()
    # Graph 2 BAR CHART function call
    fig2, insights2 = get_reg_app_rev()
    fig3 = reg_app_line()
    fig4 = gauge_surp()
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/layout.html", title="Thesis", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, chart1insight=insights, chart2insight=insights2, year=year, region=region)


# GRAPH 1: DEFAULT WATERFALL CHART : SURPLUS(Revenue - Apprpriations) IN 2016 - 2020
# function generate


def get_surplus():
    phsurplusexcel = pd.ExcelFile('SCBAA/TOTALVALS.xlsx')
    surplusperyear = pd.read_excel(phsurplusexcel, usecols='T')
    surpvals = surplusperyear.iloc[0:5, 0]
    years = initialize_dir_year()
    waterfvals = []
    percents = []
    pospercent = []
    negpercent = []
    # GET VALUES TO BE USED FOR WATERFALL CHART
    for i in range(len(surpvals)-1):
        if i == 0:
            waterfvals.append(surpvals[i])
            waterfvals.append(surpvals[i+1] - surpvals[i])
        else:
            waterfvals.append(surpvals[i+1] - surpvals[i])
    # GET PERCENTAGES
    for i in range(len(surpvals)-1):
        if(i == 0):
            percents.append(100)
            if(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2) < 0):
                negpercent.append(
                    abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))
            else:
                pospercent.append(
                    abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))
            percents.append(
                abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))
        else:
            if(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2) < 0):
                negpercent.append(
                    abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))
            else:
                pospercent.append(
                    abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))
            percents.append(
                abs(round((((surpvals[i+1] - surpvals[i])/surpvals[i]) * 100), 2)))

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative",
                 "relative", "relative", "relative"],
        x=years,
        textposition="outside",
        text=[years[0]+" SURPLUS", str(percents[1])+'%', str(
            percents[2])+'%', str(percents[3])+'%', str(percents[4])+'%'],
        y=waterfvals,
        increasing={"marker": {"color": "#ABDEE6"}},
        decreasing={"marker": {"color": "#CBAACB"}},
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))
    fig.update_layout(
        title="Surplus Values from "+years[0]+" to "+years[-1]
    )
    insights = "Highest Increase: {highinc}% during {highincyear}<br>Highest Decrease: {highdec}% during {highdecyear}<br>Difference of {yearmax} Surplus to {yearmin} Surplus: {yeardiff}%".format(
        highinc=max(pospercent[1:]),
        highincyear=years[np.argmax([percents == max(pospercent[1:])])],
        highdec=max(negpercent[1:]),
        highdecyear=years[np.argmax([percents == max(negpercent[1:])])],
        yearmin=years[0],
        yearmax=years[-1],
        yeardiff=abs(round((((surpvals[4] - surpvals[0])/surpvals[0]) * 100), 2)))
    return fig, insights

# GRAPH 2: DEFAULT ANIMATED BAR CHART: ALL OF THE REGION'S APPROPRIATIONS AND REVENUES IN 2016-2020
# function generate


def get_reg_app_rev():
    df = pd.read_excel('SCBAA/Defaultgraph.xlsx')
    year = initialize_dir_year()
    int_year = [int(i) for i in year]
    valsdf = [df.loc[df['Year'] == y] for y in int_year]
    insights2 = ""
    for i in range(len(year)):
        insights2 += "\
        <ul class='year{num}'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev:,} from {maxrevreg}</li>\
        <li>Lowest Revenue: {minrev:,} from {minrevreg} </li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp:,} from {maxappreg}</li>\
                <li>Lowest Appropriation: {minapp:,} from {minappreg}</li>\
        </ul></ul>".format(maxrev=max(valsdf[i]["Revenue"]), minrev=min(valsdf[i]["Revenue"]),
                           maxapp=max(valsdf[i]["Appropriations"]), minapp=min(valsdf[i]["Appropriations"]),
                           minrevreg=valsdf[i]["Region"].loc[valsdf[i]["Revenue"]
                                                             == valsdf[i]["Revenue"].min()].iloc[0],
                           maxrevreg=valsdf[i]["Region"].loc[valsdf[i]["Revenue"]
                                                             == valsdf[i]["Revenue"].max()].iloc[0],
                           maxappreg=valsdf[i]["Region"].loc[valsdf[i]["Appropriations"]
                                                             == valsdf[i]["Appropriations"].max()].iloc[0],
                           minappreg=valsdf[i]["Region"].loc[valsdf[i]["Appropriations"]
                                                             == valsdf[i]["Appropriations"].min()].iloc[0],
                           num=i+1)

    fig = px.bar(df, x="Region", y=["Revenue", "Appropriations"],
                 animation_frame="Year", animation_group="Region", barmode='group',  color_discrete_sequence=["#ABDEE6", "#CBAACB"],
                 title="Revenue and Appropriations per Region "+year[0]+" to "+year[-1])
    return fig, insights2
# Pie chart of Revenues and Appropriations 2016 to 2020


def reg_app_line():
    df = pd.read_excel('SCBAA/Defaultgraph.xlsx')
    yearstr = initialize_dir_year()
    yearsi = [int(i) for i in yearstr]
    totaldicts = {
        "Years": yearsi,
        "Revenues": [],
        "Appropriations": []}
    for i in yearsi:
        totaldicts["Revenues"].append(
            (df["Revenue"].loc[df["Year"] == i]).sum())
    for i in yearsi:
        totaldicts["Appropriations"].append(
            (df["Appropriations"].loc[df["Year"] == i]).sum())
    linedf = pd.DataFrame(totaldicts)
    fig = px.line(
        data_frame=linedf,
        x="Years", y=["Revenues", "Appropriations"], color_discrete_sequence=["#ABDEE6", "#CBAACB"], markers=True, line_shape="spline",
        title="Revenues and Appropriations of all Local Government Units from " +
        yearstr[0]+" to "+yearstr[-1]
    )
    return fig
# GRAPH 4: DROPDOWN CHART: SAMPLE
# function generate


def gauge_surp():
    phsurplusexcel = pd.ExcelFile('SCBAA/TOTALVALS.xlsx')
    df = pd.read_excel(phsurplusexcel, usecols='T')
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    lat = latest[0]
    prev = previous[0]
    diff = ((lat - prev)/((lat+prev)/2))*100
    diffpercent = abs(((lat - prev)/((lat+prev)/2))*100)
    diffround = abs(math.ceil(diffpercent / 100)*100)
    difflow = -diffround
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=diff,
        mode="gauge+number",
        title={'text': "Latest Surplus Difference in %"},
        gauge={'bar': {'color': "#FED7C3"}, 'axis': {'range': [difflow, diffround]},
               'steps': [
            {'range': [difflow, (difflow+diffround)/2],
             'color': "#CBAACB"},
            {'range': [(difflow+diffround)/2, (diffround/2)],
             'color': "#FFFFB5"},
            {'range': [diffround/2, diffround], 'color': "#ABDEE6"}
        ]}))
    fig.update_layout(paper_bgcolor="lavender", font={
                      'color': "darkblue", 'family': "Arial"})
    return fig


def gen_reference(r, c, i):
    year = initialize_dir_year()
    year = list(map(int, year))
    arr = get_amountallyr(r, c, i)
    dict_samp = remov_zero(arr, i, year)
    df = pd.DataFrame(dict_samp)
    fig = px.bar(df, x="Year", y=i,  color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                              "#FEE1E8", "#FED7C3"])
    fig.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name=i, showlegend=True)
    df2 = pd.DataFrame(imputearr(arr, i, year))
    fig2 = px.bar(df2, x="Year", y="Imputed "+i, title=c + " " + i+" through "+str(year[0])+"-"+str(year[-1]),
                  text="Imputed "+i, color_discrete_sequence=["#FFFFB5"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Imputed "+i, showlegend=True)
    fig2.add_trace(fig.data[0])

    fig2.update_layout(uniformtext_minsize=8,
                       uniformtext_mode='hide', showlegend=True)
    fig2.update_yaxes(
        tickprefix="₱", showgrid=True)
    return fig2


def imputearr(arr, inp, year):
    df = {"Imputed "+inp: [], "Year": []}
    for i in range(len(arr)):
        if(arr[i] == 0):
            df["Imputed "+inp].append(mean(arr))
            df['Year'].append(year[i])
    return df


def remov_zero(arr, inp, year):
    df = {inp: [], "Year": []}
    for i in range(len(arr)):
        if(arr[i] != 0):
            df[inp].append(arr[i])
            df['Year'].append(year[i])
    return df
