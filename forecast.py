from flask import render_template, url_for, request, redirect
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsRegressor
from defaultfigure import dict_scbaa
from math import *
from statistics import mean
from numerize import numerize


def forecasting(inp, reg, city):
    dict_samp = {"Total Revenues": [], "Total Appropriations": [],
                 "Year": [2016, 2017, 2018, 2019, 2020]}
    dict_pred = {"Year": [2021], "Predicted Appropriation": []}
    for y in dict_scbaa['Year']:
        link_init = "SCBAA/" + str(y) + "/" + reg + ".xlsx"
        reg_init = pd.ExcelFile(link_init)
        city_init = pd.read_excel(reg_init, city)
        total_rev = city_init.iloc[35, 4]
        total_app = city_init.iloc[110, 4]
        dict_samp['Total Revenues'].append(total_rev)
        dict_samp['Total Appropriations'].append(total_app)
    arr = np.array(dict_samp['Total Revenues'])
    df = pd.DataFrame(dict_samp)
    arr_2d = np.reshape(arr, (-1, 1))
    rmse_lst = get_rmse(arr_2d, dict_samp["Total Appropriations"], 4)
    n_num, valid_rmse = get_optimalK(rmse_lst)
    neigh = KNeighborsRegressor(n_neighbors=n_num)
    neigh.fit(arr_2d, dict_samp['Total Appropriations'])
    lst = neigh.predict([[inp]])
    predict_output = lst[0]
    nby, nbx = get_neighbors(
        neigh, inp, dict_samp["Total Appropriations"], dict_samp["Total Revenues"])
    dict_pred["Predicted Appropriation"].append(predict_output)
    df2 = pd.DataFrame(dict_pred)
    fig_bar = get_fig1(df, df2)
    fig_scat = get_fig2(df, inp, nbx, nby)
    fig_line = get_fig3(valid_rmse, n_num)
    graph1JSON = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_scat, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    predict_output = "₱{:,.2f}".format(predict_output)
    return render_template("/forecastoutput.html", output=predict_output, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, rt=reg, ct=city, neighbors=nby, rmse_lst=rmse_lst, n=n_num)


def get_fig1(df, df2):
    fig = px.bar(df, x="Year", y="Total Appropriations", text="Total Appropriations",  color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                                                "#FEE1E8", "#FED7C3"])
    fig.update_traces(
        texttemplate="₱%{text:,.0f}", textposition='outside', name="Total Appropriations", showlegend=True)
    fig2 = px.bar(df2, x="Year", y="Predicted Appropriation", text="Predicted Appropriation",
                  color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted Appropriation", showlegend=True)

    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    return fig


def get_fig2(df, inp, nbx, nby):
    fig = px.scatter(df, x="Total Revenues", y="Total Appropriations", color_discrete_sequence=["blue", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                                "#FEE1E8", "#FED7C3"])

    dict_neigh = {"Total Revenues": nbx, "Total Appropriations": nby}
    fig.add_vline(x=inp,
                  line_width=3, line_dash="dash", line_color="red")
    for i in range(len(nbx)):
        fig.add_shape(type="line", opacity=0.2, x0=inp, y0=mean(nby),
                      x1=nbx[i], y1=nby[i],  line_color="red")
    fig.update_traces(name="Neighbors", showlegend=True)
    df3 = pd.DataFrame(dict_neigh)
    fig2 = px.scatter(df3, x="Total Revenues",
                      y="Total Appropriations", color_discrete_sequence=["red"])
    fig2.update_traces(name="Chosen Neighbors", showlegend=True)
    fig.add_trace(fig2.data[0])
    fig.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    fig.update_xaxes(
        tickprefix="₱", showgrid=True
    )
    return fig


def get_fig3(rmse, min):
    df = {"K": [2, 3, 4], "RMSE": rmse}
    df2 = {"K": [min], "RMSE": [rmse[min-2]]}
    fig = px.line(df, x="K", y="RMSE")
    fig.update_traces(name="K", showlegend=True)
    fig2 = px.scatter(df2, x="K", y="RMSE",
                      color_discrete_sequence=["red"])
    fig2.update_traces(name=" Chosen K", showlegend=True)
    fig.add_trace(fig2.data[0])
    fig.update_traces(mode="markers+lines")
    return fig


def get_neighbors(model, inpt, Y, X):
    neighbor_num = model.kneighbors([[inpt]], return_distance=False)
    neighbory = [Y[i]for i in neighbor_num[0]]
    neighborx = [X[i]for i in neighbor_num[0]]
    return(neighbory, neighborx)


def get_rmse(X, Y, ra):
    rmse_val = []
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=0)
    for K in range(ra):
        K = K+1
        model = KNeighborsRegressor(n_neighbors=K)
        model.fit(X_train, Y_train)
        pred = model.predict(X_test)
        error = sqrt(mean_squared_error(Y_test, pred))
        rmse_val.append(error)
    return rmse_val


def get_optimalK(rmse):
    initlst = list(rmse)
    if(rmse.index(min(rmse))+1) == 1:
        initlst.remove(min(initlst))
        return ((rmse.index(min(initlst)))+1), initlst
    else:
        return (rmse.index(min(rmse))+1), initlst
