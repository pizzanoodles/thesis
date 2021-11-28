from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
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
    rmse_lst, acc, predmods, y_tst = get_rmse(X, Y)
    n_num, valid_rmse = get_optimalK(rmse_lst)
    k = [x+2 for x in range(len(valid_rmse))]
    nbx, nby, distances = get_neighbors(dataset, [float(inp)], n_num)
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
    fig_acc, insight7 = get_fig4(acc, n_num, k, predmods, y_tst)
    fig_diff, insight6 = get_prevgauge(optm_predict_output, Y, year, forectype)

    ginsight = get_insightgeneral()
    graph1JSON = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_scat, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_preds, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_inp, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig_acc, cls=plotly.utils.PlotlyJSONEncoder)
    graph7JSON = json.dumps(fig_diff, cls=plotly.utils.PlotlyJSONEncoder)
    predict_output = "₱{:,.2f}".format(optm_predict_output[0])
    input = "₱{:,.2f}".format(float(inp))
    accuracy = "{:0.2f}%".format(acc[n_num-2])
    return render_template("/forecastoutput.html", accy=accuracy, output=predict_output, graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                           graph4JSON=graph4JSON, graph5JSON=graph5JSON, graph6JSON=graph6JSON, graph7JSON=graph7JSON, rt=reg, ct=city, neighbors=nby, rmse_lst=rmse_lst, n=n_num, inp=input, inptype=inptype,
                           forectype=forectype, insight=insight1, insight2=insight2, insight3=insight3, insight4=insight4, insight7=insight7, insight5=insight5, insight6=insight6, ginsight=ginsight), optm_predict_output


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


def get_fig4(acc, min, k, predmods, y_tst):
    df = {"K": k, "Accuracy Score": acc}
    df2 = {"K": [min], "Accuracy Score": [acc[min-2]]}
    insight = get_insightacc(k, acc, predmods, y_tst)
    fig = px.line(df, x="K", y="Accuracy Score", line_shape="spline",
                  title="Accuracy Score Model")

    fig.update_traces(name="Score", showlegend=True)
    fig2 = px.scatter(df2, x="K", y="Accuracy Score",
                      color_discrete_sequence=["red"])
    fig2.update_traces(name=" Optimal Score", showlegend=True)
    fig.add_hline(y=90,
                  line_width=2, opacity=0.3, line_dash="dash", line_color="green", annotation_text="Allowable Accuracy 90%",
                  annotation_position="top", annotation_font_color="green")
    fig.add_trace(fig2.data[0])
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(type='category')
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)
    return fig, insight


def get_prevgauge(output, y, yearlst, forectype):
    prevyear = yearlst[-1]+1
    insight = ''
    prevRevs = y[-1]
    currentRevs = output[0]
    diff = ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100
    diffpercent = abs(
        ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100)
    diffround = abs(ceil(diffpercent / 100)*100)
    difflow = -diffround
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=diff,
        mode="gauge+number",
        title={'text': "Current "+forectype+" Difference in % Last Year"},
        gauge={'bar': {'color': "#FED7C3"}, 'axis': {'range': [difflow, diffround]},
               'steps': [
            {'range': [difflow, (difflow+diffround)/2],
                'color': "#CBAACB"},
            {'range': [(difflow+diffround)/2, (diffround/2)],
                'color': "#FFFFB5"},
            {'range': [diffround/2, diffround], 'color': "#ABDEE6"}
        ]}))
    insight = get_insightforegauge(
        currentRevs, prevRevs, prevyear, diff, forectype)
    fig.update_layout(height=600)
    fig.update_layout(legend_font_size=9)

    return fig, insight
