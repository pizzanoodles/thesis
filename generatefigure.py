from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go
from defaultfigure import *
import math

# EXTRA FUNCTIONS > check list zeros


def check_list_zero(dataframe, arr, title):
    if(np.sum(arr) == 0):
        fig = px.bar(dataframe, title=title, x="Label", y="Amount", color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                             "#FEE1E8", "#FED7C3"])
    else:
        fig = px.pie(dataframe, title=title, names="Label", values="Amount", color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                                      "#FEE1E8", "#FED7C3"])
    return fig

# GENERATE FIGURE REVENUES


def generate_fig_rev(excel, dt, rt, ct, yt):
    fig_tr = generate_fig_rev_tr(excel)
    fig_ntr = generate_fig_rev_ntr(excel)
    fig_ext = generate_fig_rev_ext(excel)
    fig_ext_ntc = generate_fig_rev_ext_ntc(excel)
    fig_ext_or = generate_fig_rev_ext_or(excel)
    fig_ext_cir = generate_fig_rev_ext_cir(excel)
    fig_rb = generate_fig_rev_rb(rt, ct)
    fig_ov = generate_overview_rev(excel)
    fig_gauge = gen_gauge_rev(int(yt)-1, rt, ct)
    graph1JSON = json.dumps(fig_tr, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_ntr, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_ext, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_ext_ntc, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_ext_or, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig_ext_cir, cls=plotly.utils.PlotlyJSONEncoder)
    graph7JSON = json.dumps(fig_rb, cls=plotly.utils.PlotlyJSONEncoder)
    graph8JSON = json.dumps(fig_ov, cls=plotly.utils.PlotlyJSONEncoder)
    graph9JSON = json.dumps(fig_gauge, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/datavis.html", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graph5JSON=graph5JSON, graph6JSON=graph6JSON, graph7JSON=graph7JSON, graph8JSON=graph8JSON, graph9JSON=graph9JSON, dt=dt, rt=rt, ct=ct, yt=yt, sunbInsightsRev=sunbInsightsRev, prevyear=prevyear)

# GENERATE FIGURE OVERVIEW REVENUES


def generate_overview_rev(excel):
    dict_samp = {"Sources": ["Local Sources", "Local Sources", "Local Sources", "Local Sources", "Local Sources", "Local Sources", "External Sources",
                             "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "Receipt from Borrowings"],
                 "Label1": ["Tax Revenue", "Tax Revenue", "Tax Revenue", "Non-Tax Revenue", "Non-Tax Revenue", "Non-Tax Revenue",
                            "Share from the National Internal Revenue Taxes (IRA)", "Share from GOCCs", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Receipts", "Other Receipts", "Inter-local Transfer", "Capital/Investment Receipts", "Capital/Investment Receipts", "Capital/Investment Receipts", None],
                 "Label2": ["Tax Revenue - Property", "Tax Reveue - Goods and Services", "Other Local Taxes", "Service Income", "Business Income", "Other Income and Receipts",
                            None, None, "Share from Ecozone", "Share from EVAT", "Share from National Wealth", "Share from Tobacco Excise Tax", "Grants and Donations", "Other Subsidy Income", None, "Sale of Capital Assets", "Sale of Investments", "Proceeds from Collections of Loans Receivable", None]}
    rev_init = excel.iloc[9:12, 4].values.tolist()
    rev_init1 = excel.iloc[14:17, 4].values.tolist()
    rev_init2 = excel.iloc[19:21, 4].values.tolist()
    rev_init3 = excel.iloc[22:26, 4].values.tolist()
    rev_init4 = excel.iloc[27:29, 4].values.tolist()
    rev_init5 = excel.iloc[29, 4]
    rev_init6 = excel.iloc[31:34, 4].values.tolist()
    rev_init7 = excel.iloc[34, 4]
    rev_init4.append(rev_init5)
    rev_init6.append(rev_init7)
    rev_init4.extend(rev_init6)
    rev_init3.extend(rev_init4)
    rev_init2.extend(rev_init3)
    rev_init1.extend(rev_init2)
    rev_init.extend(rev_init1)
    dict_samp['Amount'] = rev_init
    df = pd.DataFrame(dict_samp)
    fig = px.sunburst(df, path=['Sources', 'Label1', 'Label2'], color="Sources", values='Amount', title="Overview of Revenues",
                      color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                               "#FEE1E8", "#FED7C3"])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    amounts = df["Amount"]
    largestval = max(amounts)
    lowestval = amounts[amounts > 0].min(0)
    sum = amounts.sum()
    largestpercent = round(((largestval/sum)*100), 2)
    lowestpercent = round(((lowestval/sum)*100), 2)

    ####largest vars####
    largestpercent = round(((largestval/sum)*100), 2)
    largestsource = ""
    source1 = ""
    highfinlbl = ""
    #####################

    ####LARGEST VARIABLES####
    source1 = df["Sources"].loc[df["Amount"] == largestval].iloc[0]
    if(source1 == "Local Sources"):
        if((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Tax Revenue"):
            largestsource = "Tax Revenue"
            if((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Tax Revenue - Property"):
                highfinlbl = "Tax Revenue - Property"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Tax Revenue - Goods and Services"):
                highfinlbl = "Tax Revenue - Goods and Services"
            else:
                highfinlbl = "Other Local Taxes"
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Non-Tax Revenue"):
            largestsource = "Non-Tax Revenue"
            if((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Service Income"):
                highfinlbl = "Service Income"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Business Income"):
                highfinlbl = "Business Income"
            else:
                highfinlbl = "Other Income and Receipts"
    elif(source1 == "External Sources"):
        if((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Share from the National Internal Revenue Taxes (IRA)"):
            largestsource = "Share from the National Internal Revenue Taxes (IRA)"
            highfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Share from GOCCs"):
            largestsource = "Share from GOCCs"
            highfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Other Shares from National Tax Collections"):
            largestsource = "Other Shares from National Tax Collections"
            if((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Share from Ecozone"):
                highfinlbl = "Share from Ecozone"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Share from EVAT"):
                highfinlbl = "Share from EVAT"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Share from National Wealth"):
                highfinlbl = "Share from National Wealth"
            else:
                highfinlbl = "Share from Tobacco Excise Tax"
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Other Receipts"):
            largestsource = "Other Receipts"
            if((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Grants and Donations"):
                highfinlbl = "Grants and Donations"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Other Subsidy Income"):
                highfinlbl = "Other Subsidy Income"
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Inter-local Transfer"):
            largestsource = "Inter-local Transfer"
            highfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Capital/Investment Receipts"):
            largestsource = "Capital/Investment Receipts"
            if((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Sale of Capital Assets"):
                highfinlbl = "Sale of Capital Assets"
            elif((df["Label2"].loc[df["Amount"] == largestval].iloc[0]) == "Sale of Investments"):
                highfinlbl = "Sale of Investments"
            else:
                highfinlbl = "Proceeds from Collections of Loans Receivable"
    else:
        largestsource = "Receipts from Borrowings"
        highfinlbl = ""
    #########################
    ####LOWEST VARIABLES ####
     ####lowest vars#####
    lowestpercent = round(((lowestval/sum)*100), 2)
    lowestsource = ""
    source2 = ""
    lowfinlbl = ""
    #####################
    source2 = df["Sources"].loc[df["Amount"] == lowestval].iloc[0]
    if(source2 == "Local Sources"):
        if((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Tax Revenue"):
            lowestsource = "Tax Revenue"
            if((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Tax Revenue - Property"):
                lowfinlbl = "Tax Revenue - Property"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Tax Revenue - Goods and Services"):
                lowfinlbl = "Tax Revenue - Goods and Services"
            else:
                lowfinlbl = "Other Local Taxes"
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Non-Tax Revenue"):
            lowestsource = "Non-Tax Revenue"
            if((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Service Income"):
                lowfinlbl = "Service Income"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Business Income"):
                lowfinlbl = "Business Income"
            else:
                lowfinlbl = "Other Income and Receipts"
    elif(source2 == "External Sources"):
        if((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Share from the National Internal Revenue Taxes (IRA)"):
            lowestsource = "Share from the National Internal Revenue Taxes (IRA)"
            lowfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Share from GOCCs"):
            lowestsource = "Share from GOCCs"
            lowfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Other Shares from National Tax Collections"):
            lowestsource = "Other Shares from National Tax Collections"
            if((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Share from Ecozone"):
                lowfinlbl = "Share from Ecozone"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Share from EVAT"):
                lowfinlbl = "Share from EVAT"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Share from National Wealth"):
                lowfinlbl = "Share from National Wealth"
            else:
                lowfinlbl = "Share from Tobacco Excise Tax"
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Other Receipts"):
            lowestsource = "Other Receipts"
            if((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Grants and Donations"):
                lowfinlbl = "Grants and Donations"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Other Subsidy Income"):
                lowfinlbl = "Other Subsidy Income"
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Inter-local Transfer"):
            lowestsource = "Inter-local Transfer"
            lowfinlbl = ""
        elif((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Capital/Investment Receipts"):
            lowestsource = "Capital/Investment Receipts"
            if((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Sale of Capital Assets"):
                lowfinlbl = "Sale of Capital Assets"
            elif((df["Label2"].loc[df["Amount"] == lowestval].iloc[0]) == "Sale of Investments"):
                lowfinlbl = "Sale of Investments"
            else:
                lowfinlbl = "Proceeds from Collections of Loans Receivable"
    else:
        lowestsource = "Receipts from Borrowings"
        lowfinlbl = ""
    #########################
    #TOOLTIP GENERATION#
        ###TOOLTIP FOR LARGEST###
    tooltips = []
    ###SOURCE LARGEST###
    if(source1 == "Local Sources"):
        tooltips.append(
            "Revenue garnered from inside the Local Government Unit")
    elif(source1 == "External Sources"):
        tooltips.append(
            "Revenue garnered from outside the Local Government Unit")
    else:
        tooltips.append(
            "Money from loans/borrowings from both internal/external sources")
    ########################LABEL 1##########################
    if(largestsource == "Tax Revenue"):
        tooltips.append("Revenue from Various Local Taxes")
    elif(largestsource == "Non-Tax Revenue"):
        tooltips.append("Revenue from Non-Tax sources")

    elif(largestsource == "Share from the National Internal Revenue Taxes (IRA)"):
        tooltips.append(
            "Administered by the BIR. Income, Indirect, Excise, and Stamp Taxes")

    elif(largestsource == "Share from GOCCs"):
        tooltips.append("Revenue from Government Owned Controlled Corporation")

    elif(largestsource == "Other Shares from National Tax Collections"):
        tooltips.append("Revenue collected from National Taxes")

    elif(largestsource == "Other Receipts"):
        tooltips.append(
            "Other Revenues from financial transactions of the Local Government Unit")

    elif(largestsource == "Inter-local Transfer"):
        tooltips.append(
            "Revenues from other government levels to help the LGU's development")

    elif(largestsource == "Capital/Investment Receipts"):
        tooltips.append("Various revenues from investments and capital assets")
    else:
        tooltips.append("")
    #################LABEL 2 ##########################
    if(highfinlbl == "Tax Revenue - Property"):
        tooltips.append(
            "Real estate tax from properties of individuals/corporations")

    elif(highfinlbl == "Tax Revenue - Goods and Services"):
        tooltips.append(
            "Value-added tax levied on most goods and services sold for domestic consumption")

    elif(highfinlbl == "Other Local Taxes"):
        tooltips.append("Various taxes from government services")

    elif(highfinlbl == "Service Income"):
        tooltips.append("Income gained from various government Services")

    elif(highfinlbl == "Business Income"):
        tooltips.append("Income gained from various government Businesses")

    elif(highfinlbl == "Other Income and Receipts"):
        tooltips.append("Other sources of income from various sales")

    elif(highfinlbl == "Share from Ecozone"):
        tooltips.append(
            "Revenue from Special Economic Zones(SEZ), an area in a country that is subject to different economic regulations than other regions within the same country")

    elif(highfinlbl == "Share from EVAT"):
        tooltips.append("Revenue from Extended Value added Taxes")

    elif(highfinlbl == "Share from National Wealth"):
        tooltips.append(
            "Local Government's share from the National Government's revenues")

    elif(highfinlbl == "Share from Tobacco Excise Tax"):
        tooltips.append("Tax from Tobacco based products")

    elif(highfinlbl == "Grants and Donations"):
        tooltips.append(
            "Various grants and donations provided to the local government")

    elif(highfinlbl == "Other Subsidy Income"):
        tooltips.append(
            "Grants of money granted to the government or a public body to assist on a certain service")

    elif(highfinlbl == "Sale of Capital Assets"):
        tooltips.append(
            "Revenue from sale of a government owned investment item for government purposes")

    elif(highfinlbl == "Sale of Investments"):
        tooltips.append("Revenue from return of investments")

    elif(highfinlbl == "Proceeds from Collections of Loans Receivable"):
        tooltips.append(
            "Revenue garnered from the collection of various loans")
    else:
        tooltips.append("")
    ########################################LOWEST VALUE ###############################
    if(source2 == "Local Sources"):
        tooltips.append(
            "Revenue garnered from inside the Local Government Unit")
    elif(source2 == "External Sources"):
        tooltips.append(
            "Revenue garnered from outside the Local Government Unit")
    else:
        tooltips.append(
            "Money from loans/borrowings from both internal/external sources")
    ########################LABEL 1##########################
    if(lowestsource == "Tax Revenue"):
        tooltips.append("Revenue from Various Local Taxes")
    elif(lowestsource == "Non-Tax Revenue"):
        tooltips.append("Revenue from Non-Tax sources")

    elif(lowestsource == "Share from the National Internal Revenue Taxes (IRA)"):
        tooltips.append(
            "Administered by the BIR. Income, Indirect, Excise, and Stamp Taxes")

    elif(lowestsource == "Share from GOCCs"):
        tooltips.append("Revenue from Government Owned Controlled Corporation")

    elif(lowestsource == "Other Shares from National Tax Collections"):
        tooltips.append("Revenue collected from National Taxes")

    elif(lowestsource == "Other Receipts"):
        tooltips.append(
            "Other Revenues from financial transactions of the Local Government Unit")

    elif(lowestsource == "Inter-local Transfer"):
        tooltips.append(
            "Revenues from other government levels to help the LGU's development")

    elif(lowestsource == "Capital/Investment Receipts"):
        tooltips.append("Various revenues from investments and capital assets")
    else:
        tooltips.append("")
    #################LABEL 2 ##########################
    if(lowfinlbl == "Tax Revenue - Property"):
        tooltips.append(
            "Real estate tax from properties of individuals/corporations")

    elif(lowfinlbl == "Tax Revenue - Goods and Services"):
        tooltips.append(
            "Value-added tax levied on most goods and services sold for domestic consumption")

    elif(lowfinlbl == "Other Local Taxes"):
        tooltips.append("Various taxes from government services")

    elif(lowfinlbl == "Service Income"):
        tooltips.append("Income gained from various government Services")

    elif(lowfinlbl == "Business Income"):
        tooltips.append("Income gained from various government Businesses")

    elif(lowfinlbl == "Other Income and Receipts"):
        tooltips.append("Other sources of income from various sales")

    elif(lowfinlbl == "Share from Ecozone"):
        tooltips.append(
            "Revenue from Special Economic Zones(SEZ), an area in a country that is subject to different economic regulations than other regions within the same country")

    elif(lowfinlbl == "Share from EVAT"):
        tooltips.append("Revenue from Extended Value added Taxes")

    elif(lowfinlbl == "Share from National Wealth"):
        tooltips.append(
            "Local Government's share from the National Government's revenues")

    elif(lowfinlbl == "Share from Tobacco Excise Tax"):
        tooltips.append("Tax from Tobacco based products")

    elif(lowfinlbl == "Grants and Donations"):
        tooltips.append(
            "Various grants and donations provided to the local government")

    elif(lowfinlbl == "Other Subsidy Income"):
        tooltips.append(
            "Grants of money granted to the government or a public body to assist on a certain service")

    elif(lowfinlbl == "Sale of Capital Assets"):
        tooltips.append(
            "Revenue from sale of a government owned investment item for government purposes")

    elif(lowfinlbl == "Sale of Investments"):
        tooltips.append("Revenue from return of investments")

    elif(lowfinlbl == "Proceeds from Collections of Loans Receivable"):
        tooltips.append(
            "Revenue garnered from the collection of various loans")
    else:
        tooltips.append("")
    global sunbInsightsRev
    sunbInsightsRev = "Largest Appropriation: {largestapp}% ({largestrevval:,}) from <span class='jtip'>{firstsource} <span class = 'tooltiptext'>{tooltip0}</span></span> > <span class='jtip'>{largestappsrc}<span class='tooltiptext'>{tooltip1}</span></span> > <span class = 'jtip'>{lstlbl}<span class='tooltiptext'>{tooltip2}</span></span> <br/>\
        Lowest Appropriation: {lowestapp}% ({lowestrevval:,}) from <span class = 'jtip'>{secondsource}<span class = 'tooltiptext'>{tooltip3}</span></span> > <span class = 'jtip'>{lowestappsrc}<span class='tooltiptext'>{tooltip4}</span></span> > <span class ='jtip'>{lstlbl2}<span class='tooltiptext'>{tooltip5}</span></span>".format(
        largestapp=largestpercent,
        largestrevval=largestval,
        largestappsrc=largestsource,
        firstsource=source1,
        lstlbl=highfinlbl,
        lowestapp=lowestpercent,
        lowestrevval=lowestval,
        lowestappsrc=lowestsource,
        secondsource=source2,
        lstlbl2=lowfinlbl,
        tooltip0=tooltips[0],
        tooltip1=tooltips[1],
        tooltip2=tooltips[2],
        tooltip3=tooltips[3],
        tooltip4=tooltips[4],
        tooltip5=tooltips[5]
    )

    return fig


# GENERATE FIGURE REVENUES > Tax Revenue


def generate_fig_rev_tr(excel):
    dict_fig = {"Label": ["Tax Revenue - Property",
                          "Tax Revenue - Goods and Services", "Other Local Taxes"]}
    title = "Tax Revenues"
    taxrev = excel.iloc[9:12, 4].values.tolist()
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig
# GENERATE FIGURE REVENUES > Non-Tax Revenue


def generate_fig_rev_ntr(excel):
    dict_fig = {"Label": ["Service Income",
                          "Business Income", "Other Income and Receipts"]}
    title = "Non-Tax Revenues"
    taxrev = excel.iloc[14:17, 4].values.tolist()
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources


def generate_fig_rev_ext(excel):
    dict_fig = {"Label": ["Share from the National Internal Revenue Taxes (IRA)", "Share from GOCCs",
                          "Other Shares from National Tax Collections", "Other Receipts", "Inter-local Transfer", "Capital/Investment Receipts"]}
    title = "External Sources"
    taxrev = excel.iloc[19:21, 4].values.tolist()
    taxrev1 = sum(excel.iloc[22:26, 4].values.tolist())
    taxrev2 = sum(excel.iloc[27:29, 4].values.tolist())
    taxrev3 = excel.iloc[29, 4]
    taxrev4 = sum(excel.iloc[31:34, 4].values.tolist())
    lastrev = [taxrev1, taxrev2, taxrev3, taxrev4]
    taxrev.extend(lastrev)
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > National Tax Collections


def generate_fig_rev_ext_ntc(excel):
    dict_fig = {"Label": ["Share from Ecozone", "Share from EVAT",
                          "Share from National Wealth", "Share from Tobacco Excise Tax"]}
    title = "Other Shares from National Tax Collections"
    taxrev = excel.iloc[22:26, 4].values.tolist()
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > Other Receipts


def generate_fig_rev_ext_or(excel):
    dict_fig = {"Label": ["Grants and Donations", "Other Subsidy Income"]}
    title = "Other Receipts"
    taxrev = excel.iloc[27:29, 4].values.tolist()
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > Capital/Investment Receipts


def generate_fig_rev_ext_cir(excel):
    dict_fig = {"Label": ["Sale of Capital Assets", "Sale of Investments",
                          "Proceeds from Collections of Loans Receivable"]}
    title = "Capital/Investment Receipts"
    taxrev = excel.iloc[31:34, 4].values.tolist()
    dict_fig['Amount'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > Receipts from Borrowings


def generate_fig_rev_rb(rt, ct):
    dict1 = {"Year": [], "Receipts": []}
    for y in dict_scbaa['Year']:
        i = 0
        link_init = "SCBAA/" + str(y) + "/" + rt + ".xlsx"
        reg_init = pd.ExcelFile(link_init)
        city_init = pd.read_excel(
            reg_init, ct)
        rev_init = city_init.iloc[34, 4]
        dict1['Year'].append(y)
        dict1['Receipts'].append(rev_init)
    df = pd.DataFrame(data=dict1)
    fig = px.line(df, x="Year", y="Receipts", line_shape="spline",
                  color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                           "#FEE1E8", "#FED7C3"])
    fig.update_xaxes(type='category')
    fig.update_traces(mode="markers+lines")
    return fig

# GENERATE APPROPRIATIONS


def generate_fig_app(excel, dt, rt, ct, yt):
    fig_con = generate_fig_app_curr(excel)
    fig_ov = generate_overview_app(excel)
    fig_others_g1 = generate_others_debt(excel)
    fig_others_g2 = generate_others_social(excel)
    fig_others_g3 = generate_others_others(excel)
    fig_cont_app = generate_continuing_app(excel)
    fig_gauge_rev = gen_gauge_app(int(yt)-1, rt, ct)
    graph1JSON = json.dumps(fig_con, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_others_g1, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_ov, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_others_g2, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_others_g3, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig_cont_app, cls=plotly.utils.PlotlyJSONEncoder)
    graph7JSON = json.dumps(fig_gauge_rev, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/datavis.html", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graph5JSON=graph5JSON, graph6JSON=graph6JSON, graph7JSON=graph7JSON, dt=dt, rt=rt, ct=ct, yt=yt, sunbInsightsApp=sunbInsightsApp, prevyear=prevyear)

# GENERATE FIGURE OVERVIEW APPROPRIATIONS


def generate_overview_app(excel):
    dict_samp = {"Sources": ["Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Current Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", "Continuing Appropriations", ],
                 "Label1": ["General Public Services", "General Public Services", "General Public Services", "Education", "Education", "Education", "Health, Nutrition and Population Control", "Health, Nutrition and Population Control", "Health, Nutrition and Population Control", "Labor and Employment", "Labor and Employment", "Labor and Employment", "Housing and Community Development", "Housing and Community Development", "Housing and Community Development", "Social Services and Social Welfare", "Social Services and Social Welfare", "Social Services and Social Welfare", "Economic Services", "Economic Services", "Economic Services", "Other Services Sector", "Other Services Sector", "Other Services Sector", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "Other Purposes", "General Public Services", "Education", "Health, Nutrition and Population Control", "Labor and Employment",
                            "Housing and Community Development", "Social Services and Social Welfare", "Economic Services", "Other Purposes"],
                 "Label2": ["Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personnel Services", "Maintenance and Other Operating Expenses", "Capital Outlay", "Debt Service", "Debt Service", "LDRRMF", "LDRRMF", "20% Development Fund", "20% Development Fund", "Share from National Wealth", "Share from National Wealth", "Allocation for Senior Citizens and PWD",
                            "Allocation for Senior Citizens and PWD", "Others", "Others", "Others", "Capital Outlay", "Capital Outlay", "Capital Outlay", "Capital Outlay", "Capital Outlay", "Capital Outlay", "Capital Outlay", "Capital Outlay"],
                 "Label3": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "Financial Expense", "Amortization", "Maintenance and Other Operating Expenses", "Capital Outlay", "Maintenance and Other Operating Expenses", "Capital Outlay", "Maintenance and Other Operating Expenses",
                            "Capital Outlay", "Maintenance and Other Operating Expenses", "Capital Outlay", "Personal Services", "Maintenance and Other Operating Expenses", "Capital Outlay", None, None, None, None, None, None, None, None]
                 }
    rev_init = excel.iloc[40:91, 4].values.tolist()
    cleanedList = [x for x in rev_init if str(x) != 'nan']
    rev_init2 = excel.iloc[94:109, 4].values.tolist()
    cleanedList2 = [x for x in rev_init2 if str(x) != 'nan']
    cleanedList.extend(cleanedList2)
    dict_samp['Amount'] = cleanedList
    df = pd.DataFrame(dict_samp)
    fig = px.sunburst(df, title="Overview of Expenditures", names="Sources", path=['Sources', 'Label1',
                                                                                   'Label2', 'Label3'], values='Amount', color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5", "#FFCCB6", "#F3B0C3", "#C6DBDA",
                                                                                                                                                  "#FEE1E8", "#FED7C3"])
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    amounts = df["Amount"]
    largestval = max(amounts)
    lowestval = amounts[amounts > 0].min(0)
    sum = amounts.sum()
    ####largest vars####
    largestpercent = round(((largestval/sum)*100), 2)
    largestsource = ""
    source1 = ""
    highfinlbl = ""
    #####################
    ####lowest vars#####
    lowestpercent = round(((lowestval/sum)*100), 2)
    lowestsource = ""
    source2 = ""
    lowfinlbl = ""
    #####################

    ####LARGEST VARIABLES####
    if((df["Label1"].loc[df["Amount"] == largestval].iloc[0]) == "Other Purposes"):
        largestsource = df["Label2"].loc[df["Amount"] == largestval].iloc[0]
    else:
        largestsource = df["Label1"].loc[df["Amount"] == largestval].iloc[0]
    source1 = df["Sources"].loc[df["Amount"] == largestval].iloc[0]
    if((df["Label3"].loc[df["Amount"] == largestval].iloc[0]) == None):
        highfinlbl = df["Label2"].loc[df["Amount"] == largestval].iloc[0]
    else:
        highfinlbl = df["Label3"].loc[df["Amount"] == largestval].iloc[0]
    #########################
    ####LOWEST VARIABLES ####
    source2 = df["Sources"].loc[df["Amount"] == lowestval].iloc[0]
    if((df["Label1"].loc[df["Amount"] == lowestval].iloc[0]) == "Other Purposes"):
        lowestsource = df["Label2"].loc[df["Amount"] == lowestval].iloc[0]
    else:
        lowestsource = df["Label1"].loc[df["Amount"] == lowestval].iloc[0]

    if((df["Label3"].loc[df["Amount"] == lowestval].iloc[0]) == None):
        lowfinlbl = df["Label2"].loc[df["Amount"] == lowestval].iloc[0]
    else:
        lowfinlbl = df["Label3"].loc[df["Amount"] == lowestval].iloc[0]
    #########################
    #TOOLTIP GENERATION#
        ###TOOLTIP FOR LARGEST###
    tooltips = []
    ###SOURCE LARGEST###
    if(source1 == "Current Appropriations"):
        tooltips.append(
            "Budget that is set aside for various government uses for this current year")
    elif(source1 == "Continuing Appropriations"):
        tooltips.append(
            "Appropriations available to support obligations for a specified purpose or project, even when these obligations are incurred beyond the budget year")
    ########################LABEL 1##########################
    if(largestsource == "General Public Services"):
        tooltips.append(
            "Budget for General Services that the government provide to the public")

    elif(largestsource == "Education"):
        tooltips.append(
            "Budget for education related purposes, (schools,seminars, etc.)")

    elif(largestsource == "Health, Nutrition and Population Control"):
        tooltips.append("Budget for public's health-related expenses.")

    elif(largestsource == "Labor and Employment"):
        tooltips.append("Budget for the public's employment related expenses")

    elif(largestsource == "Housing and Community Development"):
        tooltips.append(
            "Budget for the public's local housing development expenses")

    elif(largestsource == "Social Services and Social Welfare"):
        tooltips.append(
            "Budget for aiding disadvantaged, distressed, or vulnerable persons or groups.")

    elif(largestsource == "Economic Services"):
        tooltips.append("Budget for economic utility expenses")

    elif(largestsource == "Other Services Sector"):
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")

    elif(largestsource == "Other Purposes"):
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")

    elif(largestsource == "Debt Service"):
        tooltips.append(
            "Budget for payment and repayment of principal capital")

    elif(largestsource == "LDRRMF"):
        tooltips.append("Budget invested in disaster risk reductions")

    elif(largestsource == "20% Development Fund"):
        tooltips.append(
            "Budget used for expenses in the development of the local government")

    elif(largestsource == "Share from National Wealth"):
        tooltips.append("Expenses made for share in the National Wealth")

    elif(largestsource == "Allocation for Senior Citizens and PWD"):
        tooltips.append(
            "Budget for expenses used for the programs, projects and activities proportionately divided among senior citizens and persons with disability")

    else:
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")
    #################LABEL 2 ##########################
    if(highfinlbl == "Financial Expense"):
        tooltips.append(
            "Expenses associated with financing the certain sector.")

    if(highfinlbl == "Amortization"):
        tooltips.append("Budget for specifically repaying of debts.")

    if(highfinlbl == "Personnel Services"):
        tooltips.append(
            "Budget for expenses on the personnel (salaries, wages, and other compensation)")

    if(highfinlbl == "Maintenance and Other Operating Expenses"):
        tooltips.append(
            "Budget for the expenses made for regulation of an operation of a sector.")

    if(highfinlbl == "Capital Outlay"):
        tooltips.append(
            "Budget for expenses made to acquire capital assets to be used for a certain sector.")
    ########################################LOWEST VALUE ###############################
    if(source2 == "Current Appropriations"):
        tooltips.append(
            "Budget that is set aside for various government uses for this current year")
    elif(source2 == "Continuing Appropriations"):
        tooltips.append(
            "Appropriations available to support obligations for a specified purpose or project, even when these obligations are incurred beyond the budget year")

    if(lowestsource == "General Public Services"):
        tooltips.append(
            "Budget for General Services that the government provide to the public")

    elif(lowestsource == "Education"):
        tooltips.append(
            "Budget for education related purposes, (schools,seminars, etc.)")

    elif(lowestsource == "Health, Nutrition and Population Control"):
        tooltips.append("Budget for public's health-related expenses.")

    elif(lowestsource == "Labor and Employment"):
        tooltips.append("Budget for the public's employment related expenses")

    elif(lowestsource == "Housing and Community Development"):
        tooltips.append(
            "Budget for the public's local housing development expenses")

    elif(lowestsource == "Social Services and Social Welfare"):
        tooltips.append(
            "Budget for aiding disadvantaged, distressed, or vulnerable persons or groups.")

    elif(lowestsource == "Economic Services"):
        tooltips.append("Budget for economic utility expenses")

    elif(lowestsource == "Other Services Sector"):
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")

    elif(lowestsource == "Other Purposes"):
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")

    elif(lowestsource == "Debt Service"):
        tooltips.append(
            "Budget for payment and repayment of principal capital")

    elif(lowestsource == "LDRRMF"):
        tooltips.append("Budget invested in disaster risk reductions")

    elif(lowestsource == "20% Development Fund"):
        tooltips.append(
            "Budget used for expenses in the development of the local government")

    elif(lowestsource == "Share from National Wealth"):
        tooltips.append("Expenses made for share in the National Wealth")

    elif(lowestsource == "Allocation for Senior Citizens and PWD"):
        tooltips.append(
            "Budget for expenses used for the programs, projects and activities proportionately divided among senior citizens and persons with disability")

    else:
        tooltips.append(
            "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)")
    #################LABEL 2 ##########################
    if(lowfinlbl == "Financial Expense"):
        tooltips.append(
            "Expenses associated with financing the certain sector.")

    if(lowfinlbl == "Amortization"):
        tooltips.append("Budget for specifically repaying of debts.")

    if(lowfinlbl == "Personnel Services"):
        tooltips.append(
            "Budget for expenses on the personnel (salaries, wages, and other compensation)")

    if(lowfinlbl == "Maintenance and Other Operating Expenses"):
        tooltips.append(
            "Budget for the expenses made for regulation of an operation of a sector.")

    if(lowfinlbl == "Capital Outlay"):
        tooltips.append(
            "Budget for expenses made to acquire capital assets to be used for a certain sector.")
    global sunbInsightsApp
    sunbInsightsApp = "Largest Appropriation: {largestapp}% ({largestrevval:,}) from <span class='jtip'>{firstsource} <span class = 'tooltiptext'>{tooltip0}</span></span> > <span class='jtip'>{largestappsrc}<span class='tooltiptext'>{tooltip1}</span></span> > <span class = 'jtip'>{lstlbl}<span class='tooltiptext'>{tooltip2}</span></span> <br/>\
        Lowest Appropriation: {lowestapp}% ({lowestrevval:,}) from <span class = 'jtip'>{secondsource}<span class = 'tooltiptext'>{tooltip3}</span></span> > <span class = 'jtip'>{lowestappsrc}<span class='tooltiptext'>{tooltip4}</span></span> > <span class ='jtip'>{lstlbl2}<span class='tooltiptext'>{tooltip5}</span></span>".format(
        largestapp=largestpercent,
        largestrevval=largestval,
        largestappsrc=largestsource,
        firstsource=source1,
        lstlbl=highfinlbl,
        lowestapp=lowestpercent,
        lowestrevval=lowestval,
        lowestappsrc=lowestsource,
        secondsource=source2,
        lstlbl2=lowfinlbl,
        tooltip0=tooltips[0],
        tooltip1=tooltips[1],
        tooltip2=tooltips[2],
        tooltip3=tooltips[3],
        tooltip4=tooltips[4],
        tooltip5=tooltips[5]
    )
    return fig

# GENERATE FIGURE CURRENT APPROPRIATIONS


def generate_fig_app_curr(excel):
    firstval = 40
    firstval2 = 43
    labels = ["Personnel Services",
              "Maintenance and Other Operating Expenses", "Capital Outlay"]
    categories = ["General Public Services", "Education", "Health, Nutrition, and Population Control", "Labor and Employment", "Housing and Community Development",
                  "Social Services and Welfare", "Economic Services", "Other Services Sector"]
    values = []
    for i in range(0, 8):
        values.append(list(excel.iloc[firstval:firstval2, 4].values.tolist()))
        firstval += 4
        firstval2 += 4
    appdict = {}
    for i in range(0, 8):
        appdict[categories[i]] = values[i]
    df = pd.DataFrame(appdict)
    fig = px.bar(
        df,
        title="Current Appropriations",
        y=categories,
        x=labels,
        barmode='group',
        color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5",
                                 "#FFCCB6", "#F3B0C3", "#C6DBDA", "#FEE1E8", "#FED7C3"]
    )
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="All Categories", method="update", args=[
                        {"visible": [True, True, True, True, True, True, True, True]}, {"title": "All Appropriation Categories"}]),
                    dict(label="General Public Services", method="update", args=[
                        {"visible": [True, False, False, False, False, False, False, False]}, {"title": "General Public Services"}]),
                    dict(label="Education", method="update", args=[
                        {"visible": [False, True, False, False, False, False, False, False]}, {"title": "Education"}]),
                    dict(label="Health, Nutrition, and Population Control", method="update", args=[
                        {"visible": [False, False, True, False, False, False, False, False]}, {"title": "Health, Nutrition, and Population Control"}]),
                    dict(label="Labor and Employment", method="update", args=[
                        {"visible": [False, False, False, True, False, False, False, False]}, {"title": "Labor and Employment"}]),
                    dict(label="Housing and Community Development", method="update", args=[
                        {"visible": [False, False, False, False, True, False, False, False]}, {"title": "Housing and Community Development"}]),
                    dict(label="Social Services and Welfare", method="update", args=[
                        {"visible": [False, False, False, False, False, True, False, False]}, {"title": "Social Services and Welfare"}]),
                    dict(label="Economic Services", method="update", args=[
                        {"visible": [False, False, False, False, False, False, True, False]}, {"title": "Economic Services"}]),
                    dict(label="Other Services Sector", method="update", args=[
                        {"visible": [False, False, False, False, False, False, False, True]}, {"title": "Other Services Sector"}]),
                ])
            )
        ]
    )
    return fig


def generate_others_debt(excel):
    dict_fig = {"Label": ["Financial Expense", "Amortization"]}
    title = "Debt Services"
    values = excel.iloc[73:75, 4].values.tolist()
    dict_fig['Amount'] = values
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, values, title)
    return fig


def generate_others_social(excel):
    firstval = 76
    firstval2 = 78
    labels = ["Maintenance and Other Operating Expenses", "Capital Outlay"]
    categories = ["LDRRMF", "20% Development Fund",
                  "Share from National Wealth", "Allocation for Senior Citizens and PWD"]
    values = []
    for i in range(0, 4):
        values.append(list(excel.iloc[firstval:firstval2, 4].values.tolist()))
        firstval += 3
        firstval2 += 3
    appdict = {}
    for i in range(0, 4):
        appdict[categories[i]] = values[i]
    df = pd.DataFrame(appdict)
    fig = px.bar(
        df,
        title="Social Expenditures",
        y=categories,
        x=labels,
        barmode='group',
        color_discrete_sequence=["#ABDEE6", "#CBAACB", "#FFFFB5",
                                 "#FFCCB6", "#F3B0C3", "#C6DBDA", "#FEE1E8", "#FED7C3"]
    )
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="All Categories", method="update", args=[
                         {"visible": [True, True, True, True]}, {"title": "All Other Categories"}]),
                    dict(label="LDRRMF", method="update", args=[
                         {"visible": [True, False, False, False]}, {"title": "All Other Categories"}]),
                    dict(label="20% Development Fund", method="update", args=[
                         {"visible": [False, True, False, False]}, {"title": "20% Development Fund"}]),
                    dict(label="Share from National Wealth", method="update", args=[{"visible": [
                         False, False, True, False]}, {"title": "Share from National Wealth"}]),
                    dict(label="Allocation for Senior Citizens and PWD", method="update", args=[{"visible": [
                         False, False, False, True]}, {"title": "Allocation for Senior Citizens and PWD"}]),
                ])
            )
        ]
    )
    return fig


def generate_others_others(excel):
    dict_fig = {"Label": ["Personnel Services",
                          "Maintenance and Other Expenses", "Capital Outlay"]}
    title = "Other Purposes"
    values = list(excel.iloc[88:91, 4].values.tolist())
    dict_fig['Amount'] = values
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, values, title)
    return fig


def generate_continuing_app(excel):
    dict_fig = {"Label": ["General Public Services", "Education", "Health, Nutrition, and Population Control", "Labor and Employment",
                          "Housing and Community Development", "Social Services and Welfare", "Economic Services", "Other Purposes"]}
    title = "Continuing Appropriations"
    values = list(excel.iloc[94:109:2, 4])
    dict_fig['Amount'] = values
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, values, title)
    return fig


def gen_gauge_rev(year, reg, city):
    global prevyear
    prevyear = year
    if(prevyear != 2015):
        prevyearExcel = pd.read_excel(
            'SCBAA/{year}/{region}.xlsx'.format(year=prevyear, region=reg), sheet_name=city)
        curryearExcel = pd.read_excel(
            'SCBAA/{year}/{region}.xlsx'.format(year=prevyear+1, region=reg), sheet_name=city)
        df = pd.read_excel('SCBAA/Defaultgraph2.xlsx')
        #currentRevs = df["Revenue"].loc[df["Year"] == year+1].sum()
        #prevRevs = df["Revenue"].loc[df["Year"] == year].sum()
        prevRevs = prevyearExcel.iloc[35][4]
        currentRevs = curryearExcel.iloc[35][4]
        diff = ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100
        diffpercent = abs(
            ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100)
        diffround = abs(math.ceil(diffpercent / 100)*100)
        difflow = -diffround
        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=diff,
            mode="gauge+number",
            title={'text': "Latest Revenue Difference in %"},
            gauge={'bar': {'color': "#FED7C3"}, 'axis': {'range': [difflow, diffround]},
                   'steps': [
                {'range': [difflow, (difflow+diffround)/2],
                 'color': "#CBAACB"},
                {'range': [(difflow+diffround)/2, (diffround/2)],
                 'color': "#FFFFB5"},
                {'range': [diffround/2, diffround], 'color': "#ABDEE6"}
            ]}))
        fig.update_layout(paper_bgcolor="lavender", font={
            'color': "darkblue", 'family': "Arial"})
    else:
        return None
    return fig


def gen_gauge_app(year, reg, city):
    global prevyear
    prevyear = year
    if(prevyear != 2015):
        prevyearExcel = pd.read_excel(
            'SCBAA/{year}/{region}.xlsx'.format(year=prevyear, region=reg), sheet_name=city)
        curryearExcel = pd.read_excel(
            'SCBAA/{year}/{region}.xlsx'.format(year=prevyear+1, region=reg), sheet_name=city)
        df = pd.read_excel('SCBAA/Defaultgraph2.xlsx')
        currentRevs = df["Appropriations"].loc[df["Year"] == year+1].sum()
        prevRevs = df["Appropriations"].loc[df["Year"] == year].sum()
        prevRevs = prevyearExcel.iloc[110][4]
        currentRevs = curryearExcel.iloc[110][4]
        diff = ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100
        diffpercent = abs(
            ((currentRevs - prevRevs)/((currentRevs+prevRevs)/2))*100)
        diffround = abs(math.ceil(diffpercent / 100)*100)
        difflow = -diffround
        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=diff,
            mode="gauge+number",
            title={'text': "Latest Approriation Difference in %"},
            gauge={'bar': {'color': "#FED7C3"}, 'axis': {'range': [difflow, diffround]},
                   'steps': [
                {'range': [difflow, (difflow+diffround)/2],
                 'color': "#CBAACB"},
                {'range': [(difflow+diffround)/2, (diffround/2)],
                 'color': "#FFFFB5"},
                {'range': [diffround/2, diffround], 'color': "#ABDEE6"}
            ]}))
        fig.update_layout(paper_bgcolor="lavender", font={
            'color': "darkblue", 'family': "Arial"})
    else:
        return None
    return fig
