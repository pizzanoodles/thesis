
import pandas as pd
import os


def initialize_dir_region():
    dict_reg = {'value': ['NCR', 'CAR', 'Region 1', 'Region 2', 'Region 3', 'Region 4A', 'Region 4B', 'Region 5', 'Region 6', 'Region 7', 'Region 8', 'Region 9', 'Region 10', 'Region 11', 'Region 12', 'Region 13', 'ARMM', 'NIR'], 'label': [
        'NCR', 'CAR', 'Region I', 'Region II', 'Region III', 'Region IV-A', 'Region IV-B', 'Region V', 'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI', 'Region XII', 'Region XIII', 'ARMM', 'NIR']}
    return dict_reg


def get_cities(reg, yr, dt):
    link_init = "SCBAA/" + yr + "/" + reg + ".xlsx"
    sheets = pd.ExcelFile(link_init)
    cities = sheets.sheet_names
    for c in cities:
        city_init = pd.read_excel(link_init, c)
        if(dt == "Revenue"):
            sum = city_init.iloc[35, 4]
        elif(dt == "Appropriations"):
            sum = city_init.iloc[110, 4]
        if(sum == 0):
            cities.remove(c)
    return cities


def initialize_dir_year():
    ROOT_DIR = os.path.abspath(os.curdir)
    rootdir = ROOT_DIR + "/SCBAA"
    directory_contents = os.listdir(rootdir)
    init_list = list(directory_contents)
    for item in init_list:
        if(os.path.isfile(rootdir+"/"+item)):
            directory_contents.remove(item)
    return directory_contents
