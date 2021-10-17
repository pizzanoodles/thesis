from flask import render_template, url_for, request, redirect, jsonify
import pandas as pd
import matplotlib.ticker as ticker
from defaultfigure import *
from initialize import *
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


@app.route('/city/<reg>/<yr>/<dt>')
def city(reg, yr, dt):
    cities = get_cities(reg, yr, dt)
    return jsonify({'city': cities})


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
    year = initialize_dir_year()
    region = initialize_dir_region()
    if request.method == "POST":
        forec = request.form["forec_select"]
        inp_type = request.form["inp_select"]
        reg = request.form["reg_select"]
        city = request.form["cit_select"]
        input = request.form["inp1"]
        return redirect(url_for("results", inp=input, rt=reg, ct=city, inpt=inp_type, forect=forec))
    return render_template("forecastinput.html", year=year, region=region)


@app.route('/viewref/<r>/<c>')
def viewref(r, c):
    fig = gen_reference(r, c)
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graph1JSON)


@ app.route("/results/<rt>/<ct>/<inp>/<inpt>/<forect>")
def results(inp, rt, ct, inpt, forect):
    forecast_template = forecasting(inp, rt, ct, inpt, forect)
    return forecast_template


if __name__ == "__main__":
    app.run(debug=True)
