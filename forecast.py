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


def forecasting(inp, reg, city, inptype, forectype):
    dict_samp = {inptype: [], forectype: [],
                 "Year": [2016, 2017, 2018, 2019, 2020]}
    for y in dict_scbaa['Year']:
        link_init = "SCBAA/" + str(y) + "/" + reg + ".xlsx"
        reg_init = pd.ExcelFile(link_init)
        city_init = pd.read_excel(reg_init, city)
        total_rev = city_init.iloc[35, 4]
        total_app = city_init.iloc[110, 4]
        dict_samp[inptype].append(total_rev)
        dict_samp[forectype].append(total_app)
    arr = np.array(dict_samp[inptype])
    df = pd.DataFrame(dict_samp)
    arr_2d = np.reshape(arr, (-1, 1))
    rmse_lst = get_rmse(arr_2d, dict_samp[forectype], 4)
    n_num, valid_rmse = get_optimalK(rmse_lst)
    neigh = KNeighborsRegressor(n_neighbors=n_num, p=1)
    neigh.fit(arr_2d, dict_samp[forectype])
    lst = neigh.predict([[inp]])
    optm_predict_output = lst[0]
    nby, nbx = get_neighbors(
        neigh, inp, dict_samp[forectype], dict_samp[inptype])
    allpred = fig1_krange(arr_2d, dict_samp[forectype], inp)
    fig_inp = get_figinp(inp, reg, city, inptype)
    fig_preds = get_fig0(allpred, optm_predict_output, n_num)
    fig_bar = get_fig1(df, optm_predict_output, forectype)
    fig_scat = get_fig2(df, inp, nbx, nby, inptype, forectype)
    fig_line = get_fig3(valid_rmse, n_num)
    graph1JSON = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_scat, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_preds, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_inp, cls=plotly.utils.PlotlyJSONEncoder)
    predict_output = "₱{:,.2f}".format(optm_predict_output)
    input = "₱{:,.2f}".format(float(inp))
    return render_template("/forecastoutput.html", output=predict_output, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graph5JSON=graph5JSON, rt=reg, ct=city, neighbors=nby, rmse_lst=rmse_lst, n=n_num, inp=input, inptype=inptype, forectype=forectype)


def fig1_krange(arr, arr2, inp):
    res = []
    k = [2, 3, 4]
    for ra in k:
        model = KNeighborsRegressor(n_neighbors=ra)
        model.fit(arr, arr2)
        pred = model.predict([[inp]])
        res.append(pred[0])
    return res


def get_figinp(inp, reg, city, inptype):
    dict_samp = {"Year": [2016, 2017, 2018, 2019, 2020], inptype: []}
    dict_inp = {"Year": [2021], "Input Revenue": [float(inp)]}
    for y in dict_scbaa['Year']:
        link_init = "SCBAA/" + str(y) + "/" + reg + ".xlsx"
        reg_init = pd.ExcelFile(link_init)
        city_init = pd.read_excel(reg_init, city)
        total_rev = city_init.iloc[35, 4]
        dict_samp[inptype].append(total_rev)
    df = pd.DataFrame(dict_samp)
    df2 = pd.DataFrame(dict_inp)
    fig = px.bar(df, x="Year", y=inptype,
                 text=inptype,  color_discrete_sequence=["#ABDEE6"])
    fig.update_traces(
        texttemplate="₱%{text:,.0f}", textposition='outside', name=inptype, showlegend=True)
    fig2 = px.bar(df2, x="Year", y="Input Revenue",
                  text="Input Revenue", color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Input Revenue", showlegend=True)

    fig2.add_trace(fig.data[0])

    fig2.update_layout(uniformtext_minsize=8,
                       uniformtext_mode='hide', showlegend=True)
    fig2.update_yaxes(
        tickprefix="₱", showgrid=True)
    return fig2


def get_fig0(lst, pred, optm_k):
    init_k = [2, 3, 4]
    init_preds = list(lst)
    init_k.remove(optm_k)
    init_preds.remove(pred)
    df = {"K": init_k, "Predicted Appropriations": init_preds}
    df2 = {"K": [optm_k], "Optimal Predicted Appropriation": [pred]}
    fig = px.bar(df, x="K", y="Predicted Appropriations",
                 text="Predicted Appropriations",  color_discrete_sequence=["#ABDEE6"])
    fig.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted Appropriations", showlegend=True)
    fig2 = px.bar(df2, x="K", y="Optimal Predicted Appropriation",
                  text="Optimal Predicted Appropriation", color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Optimal Predicted Appropriation", showlegend=True)

    fig2.add_trace(fig.data[0])

    fig2.update_layout(uniformtext_minsize=8,
                       uniformtext_mode='hide', showlegend=True)
    fig2.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    return fig2


def get_fig1(df, pred, forectype):
    df2 = {"Year": [2021], "Predicted Appropriation": [pred]}
    fig = px.bar(df, x="Year", y=forectype, text=forectype,  color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                      "#FEE1E8", "#FED7C3"])
    fig.update_traces(
        texttemplate="₱%{text:,.0f}", textposition='outside', name=forectype, showlegend=True)
    fig2 = px.bar(df2, x="Year", y="Predicted Appropriation",
                  text="Predicted Appropriation", color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted Appropriation", showlegend=True)

    fig2.add_trace(fig.data[0])

    fig2.update_layout(uniformtext_minsize=8,
                       uniformtext_mode='hide', showlegend=True)
    fig2.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    return fig2


def get_fig2(df, inp, nbx, nby, inptype, forectype):
    fig = px.scatter(df, x=inptype, y=forectype, color_discrete_sequence=["blue", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                          "#FEE1E8", "#FED7C3"])

    dict_neigh = {inptype: nbx, forectype: nby}
    fig.add_vline(x=inp,
                  line_width=3, line_dash="dash", line_color="red")
    for i in range(len(nbx)):
        fig.add_shape(type="line", opacity=0.2, x0=inp, y0=mean(nby),
                      x1=nbx[i], y1=nby[i],  line_color="red")
    fig.update_traces(name="Neighbors", showlegend=True)
    df3 = pd.DataFrame(dict_neigh)
    fig2 = px.scatter(df3, x=inptype,
                      y=forectype, color_discrete_sequence=["red"])
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
        error = sqrt(mean_squared_error(pred, Y_test))
        rmse_val.append(error)
    return rmse_val


def get_optimalK(rmse):
    initlst = list(rmse)
    if(rmse.index(min(rmse))+1) == 1:
        initlst.remove(min(initlst))
        return ((rmse.index(min(initlst)))+1), initlst
    else:
        initlst.remove(rmse[1])
        return ((rmse.index(min(initlst)))+1), initlst
