from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go


def generate_fig_rev(excel, dt, rt, ct, yt):

    #fig_tr = generate_fig_rev_tr(excel)
    fig_tr = generate_fig_app(excel)
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

def generate_fig_app(excel):
    firstval = 40
    firstval2 = 43
    labels=["Personnel Services","Maintenance and Other Operating Expenses","Capital Outlay"]
    categories=["General Public Services","Education","Health, Nutrition, and Population Control","Labor and Employment","Housing and Community Development",
        "Social Services and Welfare","Economic Services","Other Services Sector"]
    values = []
    for i in range(0,8):
        values.append(list(excel.iloc[firstval:firstval2,4].values.tolist()))
        firstval+=4
        firstval2+=4
    appdict = {}
    for i in range(0,8):
        appdict[categories[i]] = values[i]
    df = pd.DataFrame(appdict)
    fig = px.bar(
        df,
        y=categories,
        x=labels,
        barmode='group'
    )
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="All Categories",method="update",args=[
                        {"visible":[True,True,True,True,True,True,True,True]},{"title":"All Appropriation Categories"}]),
                    dict(label="General Public Services",method="update",args=[
                        {"visible":[True,False,False,False,False,False,False,False]},{"title":"General Public Services"}]),
                    dict(label="Education",method="update",args=[
                        {"visible":[False,True,False,False,False,False,False,False]},{"title":"Education"}]),
                    dict(label="Health, Nutrition, and Population Control",method="update",args=[
                        {"visible":[False,False,True,False,False,False,False,False]},{"title":"Health, Nutrition, and Population Control"}]),
                    dict(label="Labor and Employment",method="update",args=[
                        {"visible":[False,False,False,True,False,False,False,False]},{"title":"Labor and Employment"}]),
                    dict(label="Housing and Community Development",method="update",args=[
                        {"visible":[False,False,False,False,True,False,False,False]},{"title":"Housing and Community Development"}]),
                    dict(label="Social Services and Welfare",method="update",args=[
                        {"visible":[False,False,False,False,False,True,False,False]},{"title":"Social Services and Welfare"}]),
                    dict(label="Economic Services",method="update",args=[
                        {"visible":[False,False,False,False,False,False,True,False]},{"title":"Economic Services"}]),
                    dict(label="Other Services Sector",method="update",args=[
                        {"visible":[False,False,False,False,False,False,False,True]},{"title":"Other Services Sector"}]),
                ])
            )
        ]
    )
    return fig