from flask import render_template
from initialize import initialize_dir_year, get_amountallyr
import pandas as pd
import json
import plotly
import plotly.express as px
from math import *
from statistics import mean
from knnalgo import *
from defaultfigure import gen_reference


def forecasting(inp, reg, city, inptype, forectype):
    test_list = initialize_dir_year()
    year = list(map(int, test_list))
    dict_samp = {"Year": year}
    dict_samp[inptype] = imputearr_lst(get_amountallyr(reg, city, inptype))
    dict_samp[forectype] = imputearr_lst(get_amountallyr(reg, city, forectype))
    X = dict_samp[inptype]
    Y = dict_samp[forectype]
    dataset = [[X[i], Y[i]] for i in range(len(X))]
    k = [x+2 for x in range(len(dataset)-2)]
    rmse_lst = get_rmse(X, Y)
    n_num, valid_rmse = get_optimalK(rmse_lst)
    nbx, nby = get_neighbors(dataset, [float(inp)], n_num)
    optm_predict_output = predict(nby)
    print(len(k))
    print(len(valid_rmse))
    df = pd.DataFrame(dict_samp)
    #get_new = check_inp(inp, dict_samp[inptype], dict_samp[forectype])
    allpred = fig1_krange(dataset, [float(inp)], k)
    #fig_inp = get_figinp(inp, reg, city, inptype, year)
    fig_inp = get_figinp(inp, reg, city, inptype, year)
    fig_preds = get_fig0(allpred, optm_predict_output, n_num, forectype, k)
    fig_bar = get_fig1(optm_predict_output, reg, city, forectype, year)
    fig_scat = get_fig2(df, inp, nbx, nby, inptype, forectype)
    fig_line = get_fig3(valid_rmse, n_num, k)

    graph1JSON = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_scat, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_preds, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_inp, cls=plotly.utils.PlotlyJSONEncoder)
    predict_output = "₱{:,.2f}".format(optm_predict_output[0])
    input = "₱{:,.2f}".format(float(inp))
    return render_template("/forecastoutput.html", output=predict_output, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                           graph4JSON=graph4JSON, graph5JSON=graph5JSON, rt=reg, ct=city, neighbors=nby, rmse_lst=rmse_lst, n=n_num, inp=input, inptype=inptype,
                           forectype=forectype)


"""def check_inp(inp, arr1, arr2):
    if(float(inp) < min(arr1)):
        chng_rate = (float(inp)-min(arr1))/min(arr1)
        newarr2 = [i+(i * chng_rate) for i in arr2]
        return newarr2
"""


def fig1_krange(dataset, inp, k):
    res = []
    for ra in k:
        nbx, nby = get_neighbors(dataset, inp, ra)
        pred = predict(nby)
        res.append(pred[0])
    return res


def get_figinp(inp, reg, city, inptype, year):
    dict_inp = {"Year": year[-1]+1, "Input "+inptype: [float(inp)]}
    df2 = pd.DataFrame(dict_inp)
    fig = gen_reference(reg, city, inptype)
    fig2 = px.bar(df2, x="Year", y="Input "+inptype,
                  text="Input "+inptype, color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Input "+inptype, showlegend=True)

    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True)
    return fig


def get_fig0(lst, pred, optm_k, forectype, k):
    init_preds = list(lst)
    init_k = list(k)
    init_k.remove(optm_k)
    init_preds.remove(pred[0])
    df = {"K": init_k, "Predicted "+forectype: init_preds}
    df2 = {"K": [optm_k], "Optimal Predicted "+forectype: pred}
    fig = px.bar(df, x="K", y="Predicted "+forectype,
                 text="Predicted "+forectype,  color_discrete_sequence=["#ABDEE6"])
    fig.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted "+forectype, showlegend=True)
    fig2 = px.bar(df2, x="K", y="Optimal Predicted "+forectype,
                  text="Optimal Predicted "+forectype, color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Optimal Predicted "+forectype, showlegend=True)

    fig2.add_trace(fig.data[0])

    fig2.update_layout(uniformtext_minsize=8,
                       uniformtext_mode='hide', showlegend=True)
    fig2.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    return fig2


def get_fig1(optm_predict_output, reg, city, forectype, year):
    dict_inp = {"Year": year[-1]+1, "Predicted " +
                forectype: optm_predict_output}
    df2 = pd.DataFrame(dict_inp)
    fig = gen_reference(reg, city, forectype)
    fig2 = px.bar(df2, x="Year", y="Predicted "+forectype,
                  text="Predicted "+forectype, color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted "+forectype, showlegend=True)

    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True)
    return fig


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


def get_fig3(rmse, min, k):
    df = {"K": k, "RMSE": rmse}
    df2 = {"K": [min], "RMSE": [rmse[min-2]]}
    print(df)
    fig = px.line(df, x="K", y="RMSE")
    fig.update_traces(name="K", showlegend=True)
    fig2 = px.scatter(df2, x="K", y="RMSE",
                      color_discrete_sequence=["red"])
    fig2.update_traces(name=" Chosen K", showlegend=True)
    fig.add_trace(fig2.data[0])
    fig.update_traces(mode="markers+lines")
    return fig
