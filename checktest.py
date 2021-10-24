from initialize import initialize_dir_year, initialize_dir_region
import pandas as pd


def get_cities(reg, yr):
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
            print(y, r, city)
