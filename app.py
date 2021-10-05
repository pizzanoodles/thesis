from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go
from defaultfigure import *
from generatefigure import *

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


@app.route("/test", methods=["POST", "GET"])
def test():
    if request.method == "POST":
        data = request.form["data_select"]
        reg = request.form["reg_select"]
        city = request.form["cit_select"]
        year = request.form["yr_select"]
        return redirect(url_for("datavis", dt=data, rt=reg, ct=city, yt=year))
    else:
        # Graph 1 WATERFALL CHART function call
        fig = get_surplus()

        # Graph 2 BAR CHART function call
        #fig2 = get_reg_app_rev()

        # Graph 3 Sample
        long_df = px.data.medals_long()

        fig3 = px.bar(long_df, x="nation", y="count",
                      color="medal", title="Long-Form Input")
        fig4 = dropdownchart()

        graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
       # graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("/layout.html", title="Thesis", graph1JSON=graph1JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON)


@app.route("/<dt>/<rt>/<ct>/<yt>")
def datavis(dt, rt, ct, yt):
    link_init = "SCBAA/" + str(yt) + "/" + rt + ".xlsx"
    reg_excel = pd.ExcelFile(link_init)
    city_excel = pd.read_excel(
        reg_excel, ct)
    if dt == "Revenue":
        rev_template = generate_fig_rev(city_excel, dt=dt, rt=rt, ct=ct, yt=yt)
        return rev_template
    elif dt == "Appropriations":
        return render_template("/datavis.html", dt=dt, rt=rt, ct=ct, yt=yt)


if __name__ == "__main__":
    app.run(debug=True)
