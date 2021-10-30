from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from math import *
from statistics import mean
from initialize import initialize_dir_year
from knnalgo import *
from defaultfigure import gen_reference
from insights import *


def forecasting(inp, reg, city, inptype, forectype, dict_samp):
    X = dict_samp[inptype]
    Y = dict_samp[forectype]
    year = dict_samp["Year"]
    df = pd.DataFrame(dict_samp)
    dataset = [[X[i], Y[i]] for i in range(len(X))]
    rmse_lst = get_rmse(X, Y)
    n_num, valid_rmse = get_optimalK(rmse_lst)
    k = [x+2 for x in range(len(valid_rmse))]
    nbx, nby, distances = get_neighbors(dataset, [float(inp)], n_num)
    print(distances)
    dist = get_distances(distances)
    optm_predict_output = predict(nby)
    allpred = fig1_krange(dataset, [float(inp)], k)
    fig_inp, insight1 = get_figinp(inp, reg, city, inptype, year, dict_samp)
    fig_preds, insight3 = get_fig0(
        allpred, optm_predict_output, n_num, forectype, k)
    fig_bar, insight2 = get_fig1(optm_predict_output, reg, city,
                                 forectype, year, dict_samp)
    fig_scat, insight5 = get_fig2(
        df, inp, nbx, nby, inptype, forectype, dist, distances)
    fig_line, insight4 = get_fig3(valid_rmse, n_num, k)

    ginsight = get_insightgeneral()
    graph1JSON = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_scat, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_preds, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_inp, cls=plotly.utils.PlotlyJSONEncoder)
    predict_output = "₱{:,.2f}".format(optm_predict_output[0])
    input = "₱{:,.2f}".format(float(inp))
    return render_template("/forecastoutput.html", output=predict_output, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                           graph4JSON=graph4JSON, graph5JSON=graph5JSON, rt=reg, ct=city, neighbors=nby, rmse_lst=rmse_lst, n=n_num, inp=input, inptype=inptype,
                           forectype=forectype, insight=insight1, insight2=insight2, insight3=insight3, insight4=insight4, insight5=insight5, ginsight=ginsight), optm_predict_output


def fig1_krange(dataset, inp, k):
    res = []
    for ra in k:
        nbx, nby, dist = get_neighbors(dataset, inp, ra)
        pred = predict(nby)
        res.append(pred[0])
    return res


def get_figinp(inp, reg, city, inptype, year, dict):
    insight1 = get_insightinp(year, dict, inptype, inp)
    dict_inp = {"Year": year[-1]+1, "Input "+inptype: [float(inp)]}
    df2 = pd.DataFrame(dict_inp)
    dict_samp = {"Year": [], "Previous Input "+inptype: []}
    year_check = initialize_dir_year()
    year_check = [int(i) for i in year_check]
    check_dictsamp = False
    for i in range(len(dict["Year"])):
        if year_check[-1] < dict["Year"][i]:
            check_dictsamp = True
            dict_samp["Year"].append(dict["Year"][i])
            dict_samp["Previous Input "+inptype].append(dict[inptype][i])
    df3 = pd.DataFrame(dict_samp)
    fig = gen_reference(reg, city, inptype)
    fig3 = px.bar(df3, x="Year", y="Previous Input "+inptype,
                  text="Previous Input "+inptype, color_discrete_sequence=["#F3B0C3"])
    fig3.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Previous Input "+inptype, showlegend=True)
    if check_dictsamp:
        fig.add_trace(fig3.data[0])
    fig2 = px.bar(df2, x="Year", y="Input "+inptype,
                  text="Input "+inptype, color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Input "+inptype, showlegend=True)
    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True)
    fig.update_layout(title_text=city+" "+inptype +
                      " through "+str(year[0])+"-"+str(year[-1]+1))
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    return fig, insight1


def get_fig0(lst, pred, optm_k, forectype, k):
    init_preds = list(lst)
    init_k = list(k)
    init_k.remove(optm_k)
    init_preds.remove(pred[0])

    df = {"K": init_k, "Predicted "+forectype: init_preds}
    insights3 = get_insightopts(pred, optm_k, df, forectype)
    df2 = {"K": [optm_k], "Optimal Predicted "+forectype: pred}
    fig = px.bar(df, x="K", y="Predicted "+forectype,
                 text="Predicted "+forectype,  color_discrete_sequence=["#ABDEE6"], title="Predicted Outputs w/ different K-values")
    fig.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted "+forectype, showlegend=True)
    fig2 = px.bar(df2, x="K", y="Optimal Predicted "+forectype,
                  text="Optimal Predicted "+forectype, color_discrete_sequence=["#CBAACB"], title="Predicted Outputs w/ different K-values")
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Optimal Predicted "+forectype, showlegend=True)

    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    fig.update_xaxes(type='category')
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    return fig, insights3


def get_fig1(optm_predict_output, reg, city, forectype, year, dict):
    insight2 = get_insightfore(year, dict, forectype, optm_predict_output)
    dict_inp = {"Year": year[-1]+1, "Predicted " +
                forectype: optm_predict_output}
    df2 = pd.DataFrame(dict_inp)
    dict_samp = {"Year": [], "Previous Predicted "+forectype: []}
    year_check = initialize_dir_year()
    year_check = [int(i) for i in year_check]
    check_dictsamp = False
    for i in range(len(dict["Year"])):
        if year_check[-1] < dict["Year"][i]:
            check_dictsamp = True
            dict_samp["Year"].append(dict["Year"][i])
            dict_samp["Previous Predicted " +
                      forectype].append(dict[forectype][i])
    df3 = pd.DataFrame(dict_samp)
    fig = gen_reference(reg, city, forectype)
    fig3 = px.bar(df3, x="Year", y="Previous Predicted "+forectype,
                  text="Previous Predicted "+forectype, color_discrete_sequence=["#F3B0C3"])
    fig3.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Previous Predicted "+forectype, showlegend=True)
    if check_dictsamp:
        fig.add_trace(fig3.data[0])
    fig2 = px.bar(df2, x="Year", y="Predicted "+forectype,
                  text="Predicted "+forectype, color_discrete_sequence=["#CBAACB"])
    fig2.update_traces(
        texttemplate="₱%{y:,.0f}", textposition='outside', name="Predicted "+forectype, showlegend=True)

    fig.add_trace(fig2.data[0])

    fig.update_layout(uniformtext_minsize=8,
                      uniformtext_mode='hide', showlegend=True)
    fig.update_yaxes(
        tickprefix="₱", showgrid=True)
    fig.update_layout(title_text=city+" "+forectype +
                      " through "+str(year[0])+"-"+str(year[-1]+1))
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    return fig, insight2


def get_fig2(df, inp, nbx, nby, inptype, forectype, dist, distances):
    fig = px.scatter(df, x=inptype, y=forectype, color_discrete_sequence=["blue", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                          "#FEE1E8", "#FED7C3"])
    dict_neigh = {inptype: nbx, forectype: nby}
    insight5 = get_insightneighbors(
        df, dict_neigh, inptype, forectype, inp, dist, distances)
    fig.add_vline(x=inp,
                  line_width=2, opacity=0.3, line_dash="dash", line_color="red")
    for i in range(len(nbx)):
        fig.add_shape(type="line", opacity=0.2, x0=inp, y0=mean(nby),
                      x1=nbx[i], y1=nby[i],  line_color="red")
    fig.update_traces(name="Neighbors", showlegend=True)
    df3 = pd.DataFrame(dict_neigh)
    fig2 = px.scatter(df3, x=inptype,
                      y=forectype, color_discrete_sequence=["red"])
    fig2.update_traces(name="Nearest Neighbors", showlegend=True)
    fig.add_trace(fig2.data[0])
    fig.update_yaxes(
        tickprefix="₱", showgrid=True
    )
    fig.update_xaxes(
        tickprefix="₱", showgrid=True
    )
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    fig.update_layout(title_text="Neighbors distance")
    return fig, insight5


def get_fig3(rmse, min, k):
    df = {"K": k, "RMSE": rmse}
    df2 = {"K": [min], "RMSE": [rmse[min-2]]}
    insight4 = get_insightrmse(df, df2)
    fig = px.line(df, x="K", y="RMSE", line_shape="spline",
                  title="RMSE check(for optimal K-Neighbors)")
    fig.update_traces(name="K", showlegend=True)
    fig2 = px.scatter(df2, x="K", y="RMSE",
                      color_discrete_sequence=["red"])
    fig2.update_traces(name=" Optimal K", showlegend=True)
    fig.add_trace(fig2.data[0])
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(type='category')
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    return fig, insight4
