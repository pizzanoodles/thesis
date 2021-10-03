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
    # Graph One
    df = px.data.medals_wide()
    ncr2017 = pd.ExcelFile('SCBAA/2017/NCR.xlsx')
    caloocan2017 = pd.read_excel(
        ncr2017, "Caloocan", skiprows=range(1, 10), usecols="D:E")
    laspinas2017 = pd.read_excel(
        ncr2017, "Las Piñas", skiprows=range(1, 10), usecols="D:E")

    # caloocan2017
    # print(laspinas2017)
    ncrcities=['Caloocan','Las Piñas','Taguig','San Juan','Quezon','Pasig','Pasay','Parañaque','Navotas','Muntinlupa','Marikina','Manila','Mandaluyong','Malabon','Makati','Valenzuela']
    #####CALOOCAN#####
    taxrev = caloocan2017.iloc[0:3, 1]
    nontrev = caloocan2017.iloc[5:8, 1]
    ext = (caloocan2017.iloc[10:26, 1])
    ext = ext.dropna()
    ypos = np.arange(len(taxrev))
    #####LAS PINAS#####
    lptaxrev = laspinas2017.iloc[0:3, 1]
    lpnontrev = laspinas2017.iloc[5:8, 1]
    lpext = (laspinas2017.iloc[10:26, 1])
    lpext = lpext.dropna()
    lpypos = np.arange(len(lptaxrev))
    combined = pd.DataFrame({'Caloocan': taxrev, 'Las Piñas': lptaxrev})
    comblbls = [s.strip() for s in caloocan2017.iloc[0:3, 0].str.strip()]
    cx = combined.plot.bar(rot=0)
    cx.yaxis.set_major_formatter(billion_formatter)
    cx.set_xticks([0, 1, 2], minor=False)
    cx.set_xticklabels(comblbls)

    fig3 = px.bar(
        combined,
        y=['Caloocan', 'Las Piñas'],
        x=comblbls,
        title='Tax Revenue',
        barmode='group',
        opacity=0.7,
        # color=['red','blue','green'],
        # color_discrete_map="identity"
        color_discrete_sequence=["#6a0c0b", "#b97d10",
                                 "blue", "goldenrod", "magenta"],
        #title="Explicit color sequence"

    )
    years = ['2016','2017','2018','2019','2020']
    phsurplusexcel = pd.ExcelFile('C:/Users/Jens/Desktop/PythonVisualizationTest/TOTALS.xlsx')
    surplusperyear = pd.read_excel(phsurplusexcel,usecols='T')
    surpvals = surplusperyear.iloc[0:5,0]
    waterfvals = []

    for i in range(len(surpvals)-1):
        if i == 0:
            waterfvals.append(surpvals[i])
            waterfvals.append(surpvals[i+1] - surpvals[i])
        else:
            waterfvals.append(surpvals[i+1] - surpvals[i])
    print(waterfvals)
    fig = go.Figure(go.Waterfall(
        name = "Surplus Adventures of Philippines", orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "relative", "relative"],
        x = ['2016','2017','2018','2019','2020'],
        textposition = "outside",
        text = ["2016 SURPLUS", str(waterfvals[1]),str(waterfvals[2]) ,str(waterfvals[3]) ,str(waterfvals[4])],
        y = waterfvals,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
))
    fig2 = px.bar(df, x="nation", y=[
                  'gold', 'silver', 'bronze'], title="Thesis2")
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/test.html", title="Thesis", graph1JSON=graph1JSON, graph3JSON=graph3JSON, graph2JSON=graph2JSON)


if __name__ == "__main__":
    app.run(debug=True)
