import pandas as pd
from numpy import nan
from defaultfigure import *
from initialize import initialize_dir_year, initialize_dir_region, get_cities, find_typedata
import os
import shutil
from shutil import copyfile
from openpyxl import load_workbook
import string
import random


def cancel_upd():
    year = initialize_dir_year()
    for y in year:
        directory_contents = os.listdir('SCBAA/'+y)
        init_list = list(directory_contents)
        for i in init_list:
            if(i.find("-copy.xlsx") != -1):
                os.remove('SCBAA/'+y+'/'+i)
    return None


def get_adminaccess():
    filepath = "SCBAAsamp/passw/passw.xlsx"
    reg_excel = pd.ExcelFile(filepath)
    city_excel = pd.read_excel(reg_excel, "Password")
    x = city_excel.iloc[0, 0]
    y = city_excel.iloc[1, 0]
    z = city_excel.iloc[2, 0]
    return x, y, z


def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def confirm_upd():
    year = initialize_dir_year()
    for y in year:
        directory_contents = os.listdir('SCBAA/'+y)
        init_list = list(directory_contents)
        for i in init_list:
            del_file = ''
            if(i.find("-copy.xlsx") != -1):
                del_file = i.replace('-copy.xlsx', '')
                os.remove('SCBAA/'+y+'/'+del_file+'.xlsx')
                os.rename('SCBAA/'+y+'/'+del_file+'-copy.xlsx',
                          'SCBAA/'+y+'/'+del_file+'.xlsx')
    return None


def update_scan():
    year = initialize_dir_year()
    lst_val = [9, 10, 11, 14, 15, 16, 19, 20, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34, 40, 41, 42, 44, 45, 46, 48, 49, 50, 52, 53, 54, 56,
               57, 58, 60, 61, 62, 64, 65, 66, 68, 69, 70, 73, 74, 76, 77, 79, 80, 82, 83, 85, 86, 88, 89, 90, 94, 96, 98, 100, 102, 104, 106, 108]
    lst_checkerrs = {"path": [], "fix": []}
    total_amlst = [12, 17, 35, 91]
    region = initialize_dir_region()['value']
    lst_checkmissingscbaa = []
    for y in year:
        y = int(y)
        for r in region:
            filepath = "SCBAA/" + str(y) + "/" + r + ".xlsx"
            copyfile(filepath, "SCBAA/" + str(y) + "/" + r + "-copy.xlsx")
            check_errorfile = False
            wb = load_workbook("SCBAA/" + str(y) + "/" + r + "-copy.xlsx")
            reg_excel = pd.ExcelFile(filepath)
            for c in dict_scbaa["Region"][r]:
                ws = wb[c]
                app, rev = 0, 0
                city_excel = pd.read_excel(reg_excel, c)
                rev = city_excel.iloc[35, 4]
                app = city_excel.iloc[110, 4]
                for i in range(102):
                    val = city_excel.iloc[i+7, 4]
                    if i+7 in lst_val:
                        if str(val) == "nan":
                            check_errorfile = True
                            lst_checkerrs['path'].append(
                                "SCBAA/"+str(y)+"/"+r+".xlsx/"+c+"/E"+str((i+7)+2))
                            lst_checkerrs['fix'].append(
                                str(val) + " -> float value")
                            ws["E"+str((i+7)+2)] = 0.0
                    elif i+7 in total_amlst:
                        pass
                    else:
                        if str(val) != "nan":
                            check_errorfile = True
                            lst_checkerrs['path'].append(
                                "SCBAA/"+str(y)+"/"+r+".xlsx/"+c+"/E"+str((i+7)+2))
                            lst_checkerrs['fix'].append(str(val) + " -> nan")
                            ws["E"+str((i+7)+2)] = None
                if rev == 0 and app == 0:
                    lst_checkmissingscbaa.append(
                        "SCBAA/"+str(y)+"/"+r+".xlsx/"+c)
            wb.save("SCBAA/" + str(y) + "/" + r + "-copy.xlsx")
            if check_errorfile == False:
                os.remove("SCBAA/" + str(y) + "/" + r + "-copy.xlsx")
    return lst_checkmissingscbaa, lst_checkerrs


def update_defaultgraph():
    year = initialize_dir_year()
    region = initialize_dir_region()['value']
    dict_revapp = {"Region": [], "Year": [],
                   "Revenue": [], "Appropriations": []}
    for y in year:
        y = int(y)
        for r in region:
            reg_excel = pd.ExcelFile("SCBAA/" + str(y) + "/" + r + ".xlsx")
            totalrev = 0
            totalapp = 0
            for c in dict_scbaa["Region"][r]:
                app, rev = 0, 0
                city_excel = pd.read_excel(reg_excel, c)
                rev = city_excel.iloc[35, 4]
                app = city_excel.iloc[110, 4]
                totalrev += rev
                totalapp += app
            dict_revapp["Region"].append(r)
            dict_revapp["Year"].append(y)
            dict_revapp["Revenue"].append(totalrev)
            dict_revapp["Appropriations"].append(totalapp)
    df = pd.DataFrame(dict_revapp)
    df.to_excel("SCBAA/Defaultgraph.xlsx")
    return None


"""y, z = update_defaultgraph()
print(y)
print("---------")
print(z)"""
"""success = True
for y in z:
    for r in z[y]:
        if r:
            success = False
if success:
    print("Success")
else:
    print("FAILED")"""


def delete_year(year):
    year = str(year)
    path = "SCBAA/"+year
    if(os.path.exists(path)):
        shutil.rmtree(path)
    else:
        pass
    return None


def add_year(year):
    year = str(year)
    path = "SCBAA/"+year
    if(os.path.exists(path)):
        pass
    else:
        os.makedirs(path)
    return path
