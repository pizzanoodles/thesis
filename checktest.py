import pandas as pd
from defaultfigure import *
from initialize import initialize_dir_year, initialize_dir_region, get_cities, find_typedata

#CHECK CITY ERRORS WITH MISSING SCBAA
"""def get_cities(reg, yr):
    link_init = "SCBAA/" + yr + "/" + reg + ".xlsx"
    sheets = pd.ExcelFile(link_init)
    cities = sheets.sheet_names
    city_check = []
    for c in cities:
        city_init = pd.read_excel(link_init, c)
        rev = city_init.iloc[35, 4]
        app = city_init.iloc[110, 4]
        if rev == 0 and app == 0:
            city_check.append(c)
    return city_check


year = initialize_dir_year()
region = initialize_dir_region()['value']
for y in year:
    yr_lst = []
    for r in region:
        city = get_cities(r, y)
        if city:
            print(y, r, city)"""

#UPDATE defaultgraph and check cities(sheets) in region.xlsx
def update_defaultgraph():
    year = initialize_dir_year()
    region = initialize_dir_region()['value']

    dict_revapp = {"Region": [], "Year": [], "Revenue": [], "Appropriations": []}
    for y in year:
        for r in region:
            reg_excel = pd.ExcelFile("SCBAA/" + str(y) + "/" + r + ".xlsx")
            totalrev = 0
            totalapp = 0
            for c in dict_scbaa["Region"][r]:
                city_excel = pd.read_excel(reg_excel, c)
                totalrev += city_excel.iloc[35, 4]
                totalapp += city_excel.iloc[110, 4]
            dict_revapp["Region"].append(r)
            dict_revapp["Year"].append(y)
            dict_revapp["Revenue"].append(totalrev)
            dict_revapp["Appropriations"].append(totalapp)
    df = pd.DataFrame(dict_revapp)
    df.to_excel("SCBAA/Defaultgraph.xlsx")
    return "Updating Defaultgraph.xlsx Success!"
