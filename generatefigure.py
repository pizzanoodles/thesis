from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go
from defaultfigure import dict_scbaa

# EXTRA FUNCTIONS > check list zeros


def check_list_zero(dataframe, arr, title):
    if(np.sum(arr) == 0):
        fig = px.bar(dataframe, title = title,x="Label", y="Data", color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA",
                                                                                            "#FEE1E8","#FED7C3"])
        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=list([
                        dict(label="Bar", method="restyle",
                             args=["type", "bar"]),
                        dict(label="Pie", method="restyle",
                             args=["type", "pie"]),
                    ]),
                    direction="down"
                )
            ]
        )
    else:
        fig = px.pie(dataframe, title = title,names="Label", values="Data", color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA",
                                                                                            "#FEE1E8","#FED7C3"])                                                                               
        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=list([
                        dict(label="Pie", method="restyle",
                             args=["type", "pie"]),
                        dict(label="Bar", method="restyle",
                             args=["type", "bar"]),
                    ]),
                    direction="down"
                )
            ]
        )
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
    graph1JSON = json.dumps(fig_tr, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_ntr, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_ext, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_ext_ntc, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_ext_or, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig_ext_cir, cls=plotly.utils.PlotlyJSONEncoder)
    graph7JSON = json.dumps(fig_rb, cls=plotly.utils.PlotlyJSONEncoder)
    graph8JSON = json.dumps(fig_ov, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/datavis.html", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graph5JSON=graph5JSON, graph6JSON=graph6JSON, graph7JSON=graph7JSON, graph8JSON=graph8JSON, dt=dt, rt=rt, ct=ct, yt=yt)

# GENERATE FIGURE OVERVIEW REVENUES


def generate_overview_rev(excel):
    dict_samp = {"Sources": ["Local Sources", "Local Sources", "Local Sources", "Local Sources", "Local Sources", "Local Sources", "External Sources",
                             "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "External Sources", "Receipt from Borrowings"],
                 "Label1": ["Tax Revenue", "Tax Revenue", "Tax Revenue", "Non-Tax Revenue", "Non-Tax Revenue", "Non-Tax Revenue",
                            " Share from the National Internal Revenue Taxes (IRA)", "Share from GOCCs", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Shares from National Tax Collections", "Other Receipts", "Other Receipts", "Inter-local Transfer", "Capital/Investment Receipts", "Capital/Investment Receipts", "Capital/Investment Receipts", None],
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
    dict_samp['Data'] = rev_init
    df = pd.DataFrame(dict_samp)
    fig = px.sunburst(df, path=['Sources', 'Label1', 'Label2'], values='Data', title="Overview of Revenues", 
                        color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA",
                                                                                            "#FEE1E8","#FED7C3"])
    return fig


# GENERATE FIGURE REVENUES > Tax Revenue


def generate_fig_rev_tr(excel):
    dict_fig = {"Label": ["Tax Revenue - Property",
                          "Tax Revenue - Goods and Services", "Other Local Taxes"]}
    title = "Tax Revenues"
    taxrev = excel.iloc[9:12, 4].values.tolist()
    dict_fig['Data'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig
# GENERATE FIGURE REVENUES > Non-Tax Revenue


def generate_fig_rev_ntr(excel):
    dict_fig = {"Label": ["Service Income",
                          "Business Income", "Other Income and Receipts"]}
    title = "Non-Tax Revenues"                          
    taxrev = excel.iloc[14:17, 4].values.tolist()
    dict_fig['Data'] = taxrev
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
    dict_fig['Data'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > National Tax Collections


def generate_fig_rev_ext_ntc(excel):
    dict_fig = {"Label": ["Share from Ecozone", "Share from EVAT",
                "Share from National Wealth", "Share from Tobacco Excise Tax"]}
    title="Other Shares from National Tax Collections"                
    taxrev = excel.iloc[22:26, 4].values.tolist()
    dict_fig['Data'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > Other Receipts


def generate_fig_rev_ext_or(excel):
    dict_fig = {"Label": ["Grants and Donations", "Other Subsidy Income"]}
    title="Other Receipts"
    taxrev = excel.iloc[27:29, 4].values.tolist()
    dict_fig['Data'] = taxrev
    df = pd.DataFrame(data=dict_fig)
    fig = check_list_zero(df, taxrev, title)
    return fig

# GENERATE FIGURE REVENUES > External Sources > Capital/Investment Receipts


def generate_fig_rev_ext_cir(excel):
    dict_fig = {"Label": ["Sale of Capital Assets", "Sale of Investments",
                          "Proceeds from Collections of Loans Receivable"]}
    title = "Capital/Investment Receipts"                          
    taxrev = excel.iloc[31:34, 4].values.tolist()
    dict_fig['Data'] = taxrev
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
    fig = px.line(df, x="Year", y="Receipts",
                  color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA",
                                                                                            "#FEE1E8","#FED7C3"])
    fig.update_xaxes(type='category')
    return fig

# GENERATE APPROPRIATIONS


def generate_fig_app(excel, dt, rt, ct, yt):
    fig_con = generate_fig_app_curr(excel)
    fig_ov = generate_overview_app(excel)
    fig_others_g1 = generate_others_debt(excel)
    fig_others_g2 = generate_others_social(excel)
    fig_others_g3 = generate_others_others(excel)
    fig_cont_app = generate_continuing_app(excel)
    graph1JSON = json.dumps(fig_con, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig_others_g1, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig_ov, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig_others_g2, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig_others_g3, cls=plotly.utils.PlotlyJSONEncoder)
    graph6JSON = json.dumps(fig_cont_app, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("/datavis.html", graph1JSON=graph1JSON, graph2JSON=graph2JSON, graph3JSON=graph3JSON,graph4JSON=graph4JSON,graph5JSON=graph5JSON,graph6JSON=graph6JSON, dt=dt, rt=rt, ct=ct, yt=yt)

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
    dict_samp['Data'] = cleanedList
    df = pd.DataFrame(dict_samp)
    fig = px.sunburst(df, title="Overview of Expenditures",path=['Sources', 'Label1',
                                'Label2', 'Label3'], values='Data', color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA",
                                                                                            "#FEE1E8","#FED7C3"])
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
        color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA","#FEE1E8","#FED7C3"]
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
    dict_fig = {"Label": ["Financial Expense","Amortization"]}
    title = "Debt Services"
    values=excel.iloc[73:75,4].values.tolist()
    dict_fig['Data'] = values
    df = pd.DataFrame(data = dict_fig)
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
        color_discrete_sequence=["#ABDEE6", "#CBAACB","#FFFFB5","#FFCCB6","#F3B0C3","#C6DBDA","#FEE1E8","#FED7C3"]
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
    dict_fig = {"Label": ["Personnel Services","Maintenance and Other Expenses","Capital Outlay"]}
    title="Other Purposes"
    values=list(excel.iloc[88:91,4].values.tolist())
    dict_fig['Data'] = values
    df = pd.DataFrame(data = dict_fig)
    fig = check_list_zero(df, values, title)
    return fig

def generate_continuing_app(excel):
    dict_fig = {"Label":["General Public Services", "Education", "Health, Nutrition, and Population Control", "Labor and Employment", "Housing and Community Development", "Social Services and Welfare", "Economic Services", "Other Purposes"]}
    title="Continuing Appropriations"
    values = list(excel.iloc[94:109:2,4])
    dict_fig['Data'] = values
    df = pd.DataFrame(data = dict_fig)
    fig = check_list_zero(df, values, title)
    return fig