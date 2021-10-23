from flask import render_template, url_for, request, redirect
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
    "Year": [2016, 2017, 2018, 2019, 2020]
}
# GENERATE DEFAULT FIGURES FUNCTION


def generate_default_figs():
    year = initialize_dir_year()
    region = initialize_dir_region()
    # Graph 1 WATERFALL CHART function call
    fig = get_surplus()
    # Graph 2 BAR CHART function call
    fig2 = get_reg_app_rev()
    fig3 = reg_app_pie()
    fig4 = gauge_surp()
    # Graph 3 Sample
    #long_df = px.data.medals_long()
    #fig3 = px.bar(long_df, x="nation", y="count",color="medal", title="Long-Form Input")
    #fig4 = dropdownchart()
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    #graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    #graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/layout.html", title="Thesis", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON,graph4JSON=graph4JSON ,chart1insight=insights, chart2insight=insights2, year=year, region=region)


# GRAPH 1: DEFAULT WATERFALL CHART : SURPLUS(Revenue - Apprpriations) IN 2016 - 2020
# function generate


def get_surplus():
    phsurplusexcel = pd.ExcelFile('SCBAA/TOTALVALS.xlsx')
    surplusperyear = pd.read_excel(phsurplusexcel, usecols='T')
    surpvals = surplusperyear.iloc[0:5, 0]
    years = ['2016', '2017', '2018', '2019', '2020']
    waterfvals = []
    percents = []
    pospercent = []
    negpercent = []
    insight = ""
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
        text=["2016 SURPLUS", str(percents[1])+'%', str(
            percents[2])+'%', str(percents[3])+'%', str(percents[4])+'%'],
        y=waterfvals,
        increasing={"marker": {"color": "#ABDEE6"}},
        decreasing={"marker": {"color": "#CBAACB"}},
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))
    fig.update_layout(
        title="Surplus Values from 2016 to 2020"
    )
    global insights
    insights = "Highest Increase: {highinc}% during {highincyear}<br>Highest Decrease: {highdec}% during {highdecyear}<br>Difference of 2020 Surplus to 2016 Surplus: {yeardiff}%".format(
        highinc=max(pospercent[1:]),
        highincyear=years[np.argmax([percents == max(pospercent[1:])])],
        highdec=max(negpercent[1:]),
        highdecyear=years[np.argmax([percents == max(negpercent[1:])])],
        yeardiff=abs(round((((surpvals[4] - surpvals[0])/surpvals[0]) * 100), 2)))
    return fig

# GRAPH 2: DEFAULT ANIMATED BAR CHART: ALL OF THE REGION'S APPROPRIATIONS AND REVENUES IN 2016-2020
# function generate


def get_reg_app_rev():
    df = pd.read_excel('SCBAA/Defaultgraph2.xlsx')
    vals2016 = df.loc[df['Year'] == 2016]
    vals2017 = df.loc[df['Year'] == 2017]
    vals2018 = df.loc[df['Year'] == 2018]
    vals2019 = df.loc[df['Year'] == 2019]
    vals2020 = df.loc[df['Year'] == 2020]
    global insights2
    insights2 = "\
        <ul class='year1'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev2016:,} from {maxrev2016reg}</li>\
        <li>Lowest Revenue: {minrev2016:,} from {minrev2016reg}</li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp2016:,} from {maxapp2016reg}</li>\
                <li>Lowest Appropriation: {minapp2016:,} from {minapp2016reg}</li>\
        </ul></ul>\
        \
            <ul class = 'year2'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev2017:,} from {maxrev2017reg}</li>\
        <li>Lowest Revenue: {minrev2017:,} from {minrev2017reg}</li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp2017:,} from {maxapp2017reg}</li>\
                <li>Lowest Appropriation: {minapp2017:,} from {minapp2017reg}</li>\
        </ul></ul>\
        \
            <ul class = 'year3'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev2018:,} from {maxrev2018reg}</li>\
        <li>Lowest Revenue: {minrev2018:,} from {minrev2018reg}</li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp2018:,} from {maxapp2018reg}</li>\
                <li>Lowest Appropriation: {minapp2018:,} {minapp2018reg}</li>\
        </ul></ul>\
        \
            <ul class='year4'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev2019:,} from {maxrev2019reg}</li>\
        <li>Lowest Revenue: {minrev2019:,} from {minrev2019reg}</li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp2019:,} from {maxapp2019reg}</li>\
                <li>Lowest Appropriation: {minapp2019:,} from {minapp2019reg}</li>\
        </ul></ul>\
        \
            <ul class = 'year5'>Revenues\
            <ul>\
        <li>Highest Revenue: {maxrev2020:,} from {maxrev2020reg}</li>\
        <li>Lowest Revenue: {minrev2020:,} from {minrev2020reg}</li>\
            </ul>\
        Appropriations\
            <ul>\
                <li>Highest Appropriation: {maxapp2020:,} from {maxapp2020reg}</li>\
                <li>Lowest Appropriation: {minapp2020:,} from {minapp2020reg}</li>\
        </ul></ul>".format(
        maxrev2016=vals2016["Revenue"].max(), minrev2016=vals2016["Revenue"].min(),
        maxrev2016reg=vals2016["Region"].loc[vals2016["Revenue"]
                                             == vals2016["Revenue"].max()].iloc[0],
        minrev2016reg=vals2016["Region"].loc[vals2016["Revenue"]
                                             == vals2016["Revenue"].min()].iloc[0],

        maxapp2016=vals2016["Appropriations"].max(), minapp2016=vals2016["Appropriations"].min(),
        maxapp2016reg=vals2016["Region"].loc[vals2016["Appropriations"]
                                             == vals2016["Appropriations"].max()].iloc[0],
        minapp2016reg=vals2016["Region"].loc[vals2016["Appropriations"]
                                             == vals2016["Appropriations"].min()].iloc[0],

        maxrev2017=vals2017["Revenue"].max(), minrev2017=vals2017["Revenue"].min(),
        maxrev2017reg=vals2017["Region"].loc[vals2017["Revenue"]
                                             == vals2017["Revenue"].max()].iloc[0],
        minrev2017reg=vals2017["Region"].loc[vals2017["Revenue"]
                                             == vals2017["Revenue"].min()].iloc[0],

        maxapp2017=vals2017["Appropriations"].max(), minapp2017=vals2017["Appropriations"].min(),
        maxapp2017reg=vals2017["Region"].loc[vals2017["Appropriations"]
                                             == vals2017["Appropriations"].max()].iloc[0],
        minapp2017reg=vals2017["Region"].loc[vals2017["Appropriations"]
                                             == vals2017["Appropriations"].min()].iloc[0],

        maxrev2018=vals2018["Revenue"].max(), minrev2018=vals2018["Revenue"].min(),
        maxrev2018reg=vals2018["Region"].loc[vals2018["Revenue"]
                                             == vals2018["Revenue"].max()].iloc[0],
        minrev2018reg=vals2018["Region"].loc[vals2018["Revenue"]
                                             == vals2018["Revenue"].min()].iloc[0],

        maxapp2018=vals2018["Appropriations"].max(), minapp2018=vals2018["Appropriations"].min(),
        maxapp2018reg=vals2018["Region"].loc[vals2018["Appropriations"]
                                             == vals2018["Appropriations"].max()].iloc[0],
        minapp2018reg=vals2018["Region"].loc[vals2018["Appropriations"]
                                             == vals2018["Appropriations"].min()].iloc[0],

        maxrev2019=vals2019["Revenue"].max(), minrev2019=vals2019["Revenue"].min(),
        maxrev2019reg=vals2019["Region"].loc[vals2019["Revenue"]
                                             == vals2019["Revenue"].max()].iloc[0],
        minrev2019reg=vals2019["Region"].loc[vals2019["Revenue"]
                                             == vals2019["Revenue"].min()].iloc[0],

        maxapp2019=vals2019["Appropriations"].max(), minapp2019=vals2019["Appropriations"].min(),
        maxapp2019reg=vals2019["Region"].loc[vals2019["Appropriations"]
                                             == vals2019["Appropriations"].max()].iloc[0],
        minapp2019reg=vals2019["Region"].loc[vals2019["Appropriations"]
                                             == vals2019["Appropriations"].min()].iloc[0],

        maxrev2020=vals2020["Revenue"].max(), minrev2020=vals2020["Revenue"].min(),
        maxrev2020reg=vals2020["Region"].loc[vals2020["Revenue"]
                                             == vals2020["Revenue"].max()].iloc[0],
        minrev2020reg=vals2020["Region"].loc[vals2020["Revenue"]
                                             == vals2020["Revenue"].min()].iloc[0],

        maxapp2020=vals2020["Appropriations"].max(), minapp2020=vals2020["Appropriations"].min(),
        maxapp2020reg=vals2020["Region"].loc[vals2020["Appropriations"]
                                             == vals2020["Appropriations"].max()].iloc[0],
        minapp2020reg=vals2020["Region"].loc[vals2020["Appropriations"]
                                             == vals2020["Appropriations"].min()].iloc[0]
    )
    fig = px.bar(df, x="Region", y=["Appropriations", "Revenue"],
                 animation_frame="Year", animation_group="Region", barmode='group',  color_discrete_sequence=["#ABDEE6", "#CBAACB"],
                 title="Revenue and Appropriations per Region 2016 to 2020")
    return fig
#Pie chart of Revenues and Appropriations 2016 to 2020
def reg_app_pie():
    df = pd.read_excel('SCBAA/Defaultgraph2.xlsx')
    years = ["2016","2017","2018","2019","2020"]
    yearsi = [2016,2017,2018,2019,2020]
    totalrevs = []
    totaldicts = {
        "Years":["2016","2017","2018","2019","2020"],
        "Revenues":[],
        "Appropriations":[]}
    for i in yearsi:
        totaldicts["Revenues"].append((df["Revenue"].loc[df["Year"] == i]).sum())
    totalapps = []
    for i in yearsi:
        totaldicts["Appropriations"].append((df["Appropriations"].loc[df["Year"] == i]).sum())
    linedf = pd.DataFrame(totaldicts)
    fig = px.line(
        data_frame = linedf,
        x="Years", y=["Revenues", "Appropriations"],color_discrete_sequence=["#ABDEE6", "#CBAACB"], markers=True, line_shape="spline",
        title="Revenues and Appropriations of all Local Government Units from 2016 to 2020"
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
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = diff,
    mode = "gauge+number",
    title = {'text': "Latest Surplus Difference in %"},
    gauge = {'bar': {'color': "#FED7C3"},'axis': {'range': [difflow, diffround]},
             'steps' : [
                 {'range': [difflow,(difflow+diffround)/2], 'color': "#CBAACB"},
                 {'range': [(difflow+diffround)/2,(diffround/2)], 'color': "#FFFFB5"},
                 {'range': [diffround/2,diffround], 'color': "#ABDEE6"}
                 ]}))
    fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    return fig

""" def dropdownchart():
    ncr2016 = pd.ExcelFile('SCBAA/2016/NCR.xlsx')
    caloocan2016 = pd.read_excel(
        ncr2016, "Caloocan", skiprows=range(1, 10), usecols="D:E")
    laspinas2016 = pd.read_excel(
        ncr2016, "Las Piñas", skiprows=range(1, 10), usecols="D:E")
    taxrev = caloocan2016.iloc[0:3, 1]
    nontrev = caloocan2016.iloc[5:8, 1]
    ext = (caloocan2016.iloc[10:26, 1])
    ext = ext.dropna()
    lptaxrev = laspinas2016.iloc[0:3, 1]
    lpnontrev = laspinas2016.iloc[5:8, 1]
    lpext = (laspinas2016.iloc[10:26, 1])
    lpext = lpext.dropna()

    caloocantotaltax = caloocan2016.iloc[3, 1]
    caloocantotalnontax = caloocan2016.iloc[8, 1]
    caloocanextdf = pd.DataFrame(ext)
    caloocanextdf.astype('float_')
    caloocantotalext = np.nansum(caloocanextdf)
    revs = [caloocantotaltax, caloocantotalnontax, caloocantotalext]
    combined = pd.DataFrame({'Caloocan': taxrev, 'Las Pinas': lptaxrev})
    comblbls = [s.strip() for s in caloocan2016.iloc[0:3, 0].str.strip()]

    fig = px.bar(
        combined,
        y=['Caloocan', 'Las Pinas'],
        x=comblbls,
        title='Tax Revenue',
        barmode='group',
        opacity=0.7,
        # color=['red','blue','green'],
        # color_discrete_map="identity"
        color_discrete_sequence=["#6a0c0b", "#b97d10",
                                 "blue", "goldenrod", "magenta"],
        #title="Explicit color sequence"
        #
    )

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Both", method="update", args=[
                         {"visible": [True, True]}, {"title": "Caloocan and Las Piñas"}]),
                    dict(label="Caloocan", method="update", args=[
                         {"visible": [True, False]}, {"title": "Caloocan Revenue"}]),
                    dict(label="Las Piñas", method="update", args=[
                         {"visible": [False, True]}, {"title": "Las Piñas Revenue"}])
                ])
            )
        ]
    )
    np.random.seed(42)
    random_x = np.random.randint(1, 101, 100)
    random_y = np.random.randint(1, 101, 100)
    x = ['A', 'B', 'C', 'D']
    fig = px.bar(
        x=x,
        y=[[100,200,500,673],[56,123,982,213]],
        barmode='group'
    )
    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True]},
                           {"title": "Both"}]),
                dict(label="Data 1",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": "Data 1",
                            }]),
                dict(label="Data 2",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"title": "Data 2",
                            }]),
            ]),
        )
    ]) 
    return fig """


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
    fig2 = px.bar(df2, x="Year", y="Imputed "+i, title=c + " " + i+" through 2016-2020",
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
