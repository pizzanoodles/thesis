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
from forecast import *

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
        default_template = generate_default_figs()
        return default_template


@app.route("/<dt>/<rt>/<ct>/<yt>")
def datavis(dt, rt, ct, yt):
    link_init = "SCBAA/" + str(yt) + "/" + rt + ".xlsx"
    reg_excel = pd.ExcelFile(link_init)
    city_excel = pd.read_excel(
        reg_excel, ct)
    if dt == "Revenue":
        rev_template = generate_fig_rev(city_excel, dt=dt, rt=rt, ct=ct, yt=yt)
        return rev_template
    else:
        app_template = generate_fig_app(city_excel, dt=dt, rt=rt, ct=ct, yt=yt)
        return app_template


@app.route("/forecast", methods=["POST", "GET"])
def forecast():
    if request.method == "POST":
        output = forecasting(request.form["inp1"])
        return redirect(url_for("results", output=output))
    return render_template("/forecastinput.html")


@app.route("/results/<output>")
def results(output):
    return render_template("/forecastoutput.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)
