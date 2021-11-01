import pandas as pd
from numpy import nan
from defaultfigure import *
from initialize import initialize_dir_year, initialize_dir_region, get_cities, find_typedata

# UPDATE defaultgraph and check missing scbaa in region.xlsx
def checkrev(city_init):
    rev_init = city_init.iloc[9:12, 4].values.tolist()
    rev_init1 = city_init.iloc[14:17, 4].values.tolist()
    rev_init2 = city_init.iloc[19:21, 4].values.tolist()
    rev_init3 = city_init.iloc[22:26, 4].values.tolist()
    rev_init4 = city_init.iloc[27:29, 4].values.tolist()
    rev_init5 = city_init.iloc[29, 4]
    rev_init6 = city_init.iloc[31:34, 4].values.tolist()
    rev_init7 = city_init.iloc[34, 4]
    rev_init4.append(rev_init5)
    rev_init6.append(rev_init7)
    rev_init4.extend(rev_init6)
    rev_init3.extend(rev_init4)
    rev_init2.extend(rev_init3)
    rev_init1.extend(rev_init2)
    rev_init.extend(rev_init1)
    try:
        a=rev_init.index(nan)
    except ValueError:
        return False
    else:
        return True


def check_app(city_init):
    rev_init = city_init.iloc[40:91, 4].values.tolist()
    cleanedList = [x for x in rev_init if str(x) != 'nan']
    rev_init2 = city_init.iloc[94:109, 4].values.tolist()
    cleanedList2 = [x for x in rev_init2 if str(x) != 'nan']
    cleanedList.extend(cleanedList2)
    if len(cleanedList) == 45:
        return False
    else:
        return True

def update_defaultgraph():
    year = initialize_dir_year()
    region = initialize_dir_region()['value']
    dict_revapp = {"Region": [], "Year": [],
                   "Revenue": [], "Appropriations": []}
    dict_checknull = {}
    dict_missingscbaa = {}
    for y in year:
        y = int(y)
        dict_missingscbaa[y] = {}
        dict_checknull[y] = {}
        for r in region:
            reg_excel = pd.ExcelFile("SCBAA/" + str(y) + "/" + r + ".xlsx")
            totalrev = 0
            totalapp = 0
            lst_checkmissingscbaa = []
            lst_checknull = []
            for c in dict_scbaa["Region"][r]:
                app, rev = 0, 0
                city_excel = pd.read_excel(reg_excel, c)
                rev = city_excel.iloc[35, 4]
                app = city_excel.iloc[110, 4]
                totalrev += rev
                totalapp += app
                if rev == 0 and app == 0:
                    lst_checkmissingscbaa.append(c)
                if(checkrev(city_excel) or check_app(city_excel)):
                    lst_checknull.append(c)
            if lst_checkmissingscbaa:
                dict_missingscbaa[y][r] = lst_checkmissingscbaa
            if lst_checknull:
                dict_checknull[y][r] = lst_checknull
            dict_revapp["Region"].append(r)
            dict_revapp["Year"].append(y)
            dict_revapp["Revenue"].append(totalrev)
            dict_revapp["Appropriations"].append(totalapp)
    df = pd.DataFrame(dict_revapp)
    df.to_excel("SCBAA/Defaultgraph.xlsx")
    return "Updating Defaultgraph.xlsx Success!", dict_missingscbaa,dict_checknull

x, y,z = update_defaultgraph()
print(x)
"""
success = True
for y in z:
    for r in z[y]:
        if r:
            success = False
if success:
    print("Success")
else:
    print("FAILED")"""
