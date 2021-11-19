from flask import render_template, url_for, request, redirect, jsonify
import pandas as pd
from defaultfigure import generate_default_figs, gen_reference
from initialize import initialize_dir_region, initialize_dir_year, get_cities, get_allapptype, get_allrevtype, get_amountallyr
from generatefigure import generate_fig_rev, generate_fig_app
from forecast import forecasting
from knnalgo import imputearr_lst
from checktest import *
import plotly
import json
import ast
import zipfile

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        password = request.form["passw"]
        passw, cookie1, cookie2 = get_adminaccess()
        if password == passw:
            return render_template("admingetcookie.html", cok1=cookie1, cok2=cookie2)
        else:
            return render_template("adminlogin.html", err=1)
    else:
        return render_template("adminlogin.html")


@app.route("/checkcookies/<c1>/<c2>")
def checkcookies(c1, c2):
    passw, cookie1, cookie2 = get_adminaccess()
    bol1 = False
    if c1 == cookie1 and c2 == cookie2:
        bol1 = True
    return jsonify({'check': bol1})


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route('/admin', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    add_s = request.form['add_select']
    print(add_s)
    if uploaded_file.filename != '':
        uploaded_file.save("SCBAAsamp/tempuploadzip/"+uploaded_file.filename)
    x = add_year(add_s)
    with zipfile.ZipFile("SCBAAsamp/tempuploadzip/"+uploaded_file.filename, 'r') as zip_ref:
        zip_ref.extractall(x)
    os.remove("SCBAAsamp/tempuploadzip/"+uploaded_file.filename)
    return redirect(url_for('admin'))


@app.route("/adminupd")
def adminupd():
    miss, err = update_scan()
    return jsonify({'miss': miss, 'lenmiss': len(miss), 'errpath': err['path'], 'errfix': err['fix'], 'lenerr': len(err['path'])})


@app.route("/canceladminupd")
def canceladminupd():
    x = cancel_upd()
    y = update_defaultgraph()
    return jsonify({'none': x, 'none2': y})


@app.route("/confirmadminupd")
def confirmadminupd():
    x = confirm_upd()
    y = update_defaultgraph()
    return jsonify({'none': x, 'none2': y})


@app.route("/admindelinit")
def admindelinit():
    year = initialize_dir_year()
    return jsonify({'oldest': year[0], 'newest': year[-1]})


@app.route("/delyear/<yr>")
def delyear(yr):
    x = delete_year(yr)
    y = update_defaultgraph()
    return jsonify({'none': x})


@app.route("/adminaddinit")
def adminaddinit():
    year = initialize_dir_year()
    return jsonify({'oldest': int(year[0])-1, 'newest': int(year[-1])+1})


@app.route("/datavisdefault", methods=["POST", "GET"])
def datavisdefault():
    if request.method == "POST":
        data = request.form["data_select"]
        reg = request.form["reg_select"]
        city = request.form["cit_select"]
        year = request.form["yr_select"]
        return redirect(url_for("datavis", dt=data, rt=reg, ct=city, yt=year))
    else:
        default_template = generate_default_figs()
        return default_template


@app.route('/city/<reg>/<yr>/<dt>/<pg>')
def city(reg, yr, dt, pg):
    cities = get_cities(reg, yr, dt, pg)
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


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/forecast", methods=["POST", "GET"])
def forecast():
    year = initialize_dir_year()
    region = initialize_dir_region()
    if request.method == "POST":
        forec = request.form["forectype_select"]
        inp_type = request.form["inptype_select"]
        reg = request.form["reg_select"]
        city = request.form["cit_select"]
        input = request.form["inp1"]
        year = [int(i) for i in year]
        dict_samp = {"Year": year}
        dict_samp[inp_type] = imputearr_lst(
            get_amountallyr(reg, city, inp_type))
        dict_samp[forec] = imputearr_lst(get_amountallyr(reg, city, forec))
        return redirect(url_for("results", inp=input, rt=reg, ct=city, inpt=inp_type, forect=forec, dict_samp=dict_samp))
    return render_template("forecastinput.html", year=year, region=region)


@app.route('/viewref/<r>/<c>/<i>')
def viewref(r, c, i):
    fig = gen_reference(r, c, i)
    graph1JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graph1JSON)


@app.route('/gettype/<i>/<c>/<r>')
def gettype(i, c, r):
    if(i == "Revenues"):
        forel, forev = get_allapptype(r, c)
        inpl, inpv = get_allrevtype(r, c)
    elif(i == "Appropriations"):
        inpl, inpv = get_allapptype(r, c)
        forel, forev = get_allrevtype(r, c)
    return jsonify({'inputl': inpl, 'inputv': inpv, 'forecastl': forel, 'forecastv': forev})


@ app.route("/results/<rt>/<ct>/<inp>/<inpt>/<forect>/<dict_samp>", methods=["POST", "GET"])
def results(inp, rt, ct, inpt, forect, dict_samp):
    dict_samp = ast.literal_eval(dict_samp)
    forecast_template, predict = forecasting(
        inp, rt, ct, inpt, forect, dict_samp)
    if request.method == "POST":
        dict_samp[inpt].append(float(inp))
        dict_samp[forect].append(predict[0])
        dict_samp["Year"].append(dict_samp["Year"][-1]+1)
        inp = request.form["inp1"]
        return redirect(url_for("results", inp=inp, rt=rt, ct=ct, inpt=inpt, forect=forect, dict_samp=dict_samp))
    return forecast_template


if __name__ == "__main__":
    app.run(debug=False)
