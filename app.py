from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go


from flask import Flask

app = Flask(__name__)

armm = ['Isabela', 'Lamitan', 'Marawi']
car = ['Baguio', 'Tabuk']
ncr = ['Caloocan', 'Las Piñas', 'Makati', 'Malabon', 'Mandaluyong', 'Manila', 'Marikina',
       'Muntinlupa', 'Navotas', 'Parañaque', 'Pasay', 'Pasig', 'Quezon', 'San Juan', 'Taguig', 'Valenzuela']
nir = ['Bacolod', 'Bago', 'Bais', 'Bayawan', 'Cadiz', 'Canlaon', 'Dumaguete', 'Escalante', 'Guihulngan',
       'Himamaylan', 'Kabankalan', 'Sagay', 'San Carlos', 'Sipalay', 'Talisay', 'Tanjay', 'Victorias']

region1 = ['Batac', 'Laoag', 'Alaminos', 'Dagupan',
           'San Carlos', 'Urdaneta', 'San Fernando', 'Candon', 'Vigan']

region2 = ['Tuguegarao', 'Cauayan', 'Ilagan', 'Santiago']

region3 = ['Balanga', 'Malolos', 'Meycauayan', 'San Jose Del Monte', 'Cabanatuan', 'Gapan',
           'Muñoz', 'Palayan', 'San Jose', 'Angeles', 'San Fernando', 'Mabalacat', 'Tarlac', 'Olongapo']

region4a = ['Batangas', 'Lipa', 'Santo Tomas', 'Tanauan', 'Bacoor', 'Cavite', 'Dasmariñas', 'General Trias', 'Imus', 'Tagaytay',
            'Trece Martires', 'Biñan', 'Cabuyao', 'Calamba', 'San Pablo', 'San Pedro', 'Santa Rosa', 'Lucena', 'Tayabas', 'Antipolo']

region4b = ['Calapan', 'Puerto Princesa']

region5 = ['Legazpi', 'Ligao', 'Tabaco',
           'Iriga', 'Naga', 'Masbate', 'Sorsogon']

region6 = ['Iloilo', 'Passi', 'Passi']

region7 = ['Tagbilaran', 'Carcar', 'Bogo', 'Cebu', 'Danao',
           'Lapu-lapu', 'Mandaue', 'Naga', 'Toledo', 'Talisay']

region8 = ['Calbayog', 'Baybay', 'Borongan',
           'Catbalogan', 'Maasin', 'Ormoc', 'Tacloban']

region9 = ['Zamboanga', 'Dapitan', 'Dipolog', 'Pagadian']

region10 = ['Tangub', 'Cagayan de Oro', 'El Salvador', 'Gingoog',
            'Iligan', 'Malaybalay', 'Oroquieta', 'Ozamiz', 'Valencia']

region11 = ['Digos', 'Davao', 'Samal', 'Panabo', 'Mati', 'Tagum']

region12 = ['Koronadal', 'Cotabato', 'General Santos', 'Kidapawan', 'Tacurong']

region13 = ['Bayugan', 'Bislig', 'Butuan', 'Cabadbaran', 'Surigao', 'Tandag']

cities = [armm, car, ncr, nir,  region1, region2, region3, region4a, region4b,
          region5, region6, region7, region8, region9, region10, region11, region12, region13]

region = ['ARMM', 'CAR', 'NCR', 'NIR', 'Region 1', 'Region 2', 'Region 3', 'Region 4A', 'Region 4B',
          'Region 5', 'Region 6', 'Region 7', 'Region 8', 'Region 9', 'Region 10', 'Region 11', 'Region 12', 'Region 13']
year = [2016, 2017, 2018, 2019, 2020]

# GRAPH 1: DEFAULT WATERFALL CHART : SURPLUS(Revenue - Apprpriations) IN 2016 - 2020
# function generate


def get_surplus():
    df = px.data.medals_wide()
    phsurplusexcel = pd.ExcelFile('SCBAA/TOTALVALS.xlsx')
    surplusperyear = pd.read_excel(phsurplusexcel, usecols='T')
    surpvals = surplusperyear.iloc[0:5, 0]
    waterfvals = []

    for i in range(len(surpvals)-1):
        if i == 0:
            waterfvals.append(surpvals[i])
            waterfvals.append(surpvals[i+1] - surpvals[i])
        else:
            waterfvals.append(surpvals[i+1] - surpvals[i])
    print(waterfvals)
    fig = go.Figure(go.Waterfall(
        name="Surplus Adventures of Philippines", orientation="v",
        measure=["relative", "relative", "relative",
                 "relative", "relative", "relative"],
        x=['2016', '2017', '2018', '2019', '2020'],
        textposition="outside",
        text=["2016 SURPLUS", str(waterfvals[1]), str(
            waterfvals[2]), str(waterfvals[3]), str(waterfvals[4])],
        y=waterfvals,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    return fig

# GRAPH 2: DEFAULT ANIMATED BAR CHART: ALL OF THE REGION'S APPROPRIATIONS AND REVENUES IN 2016-2020
# function generate


def get_reg_app_rev():
    reg_app_rev = {"Region": [], "Year": [],
                   "Revenue": [], "Appropriations": []}
    for y in year:
        i = 0
        for r in region:
            region_reven = 0
            region_app = 0
            link_init = "SCBAA/" + str(y) + "/" + r + ".xlsx"
            reg_init = pd.ExcelFile(link_init)
            for c in cities[i]:
                city_init = pd.read_excel(
                    reg_init, c)
                rev_init = city_init.iloc[35, 4]
                app_init = city_init.iloc[110, 4]
                region_app = region_app + app_init
                region_reven = region_reven + rev_init
            i = i + 1
            reg_app_rev['Region'].append(r)
            reg_app_rev['Year'].append(y)
            reg_app_rev['Revenue'].append(region_reven)
            reg_app_rev['Appropriations'].append(region_app)
    df = pd.DataFrame(data=reg_app_rev)
    fig = px.bar(df, x="Region", y=["Appropriations", "Revenue"],
                 animation_frame="Year", animation_group="Region", barmode='group')
    return fig

def dropdownchart():
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
    return fig

@ticker.FuncFormatter
def million_formatter(x, pos):
    return "%.1f M" % (x/1E6)


def billion_formatter(x, pos):
    return "%.1f B" % (x/1E9)


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/test")
def test():
    # Graph 1 WATERFALL CHART function call
    fig = get_surplus()

    # Graph 2 BAR CHART function call
    fig2 = get_reg_app_rev()

    # Graph 3 Sample
    long_df = px.data.medals_long()

    fig3 = px.bar(long_df, x="nation", y="count",
                  color="medal", title="Long-Form Input")
    fig4 = dropdownchart()

    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/layout.html", title="Thesis", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON)


if __name__ == "__main__":
    app.run(debug=True)
