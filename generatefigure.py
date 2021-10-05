from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go


def generate_fig_rev(excel, dt, rt, ct, yt):

    fig_tr = generate_fig_rev_tr(excel)
    graph1JSON = json.dumps(fig_tr, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/datavis.html", graph1JSON=graph1JSON, dt=dt, rt=rt, ct=ct, yt=yt)


def generate_fig_rev_tr(excel):
    dict_tax_rev = {"Label": ["Tax Revenue - Property",
                    "Tax Revenue - Goods and Services", "Other Local Taxes"]}
    taxrev = excel.iloc[9:12, 4].values.tolist()
    dict_tax_rev['Data'] = taxrev
    df = pd.DataFrame(data=dict_tax_rev)
    fig = px.bar(df, x="Label", y="Data", color_discrete_sequence=["#3D9970"],)
    return fig
