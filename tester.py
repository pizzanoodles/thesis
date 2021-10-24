
import pandas as pd
from defaultfigure import *
from initialize import initialize_dir_year, initialize_dir_region, get_cities, find_typedata
year = initialize_dir_year()
int_year = [int(i) for i in year]
region = initialize_dir_region()['value']
df = pd.read_excel('SCBAA/Defaultgraph.xlsx')
valsdf = [df.loc[df['Year'] == y] for y in int_year]
maxrev = max(valsdf[0]["Revenue"])
minrev2020reg = valsdf[0]["Region"].loc[valsdf[0]["Revenue"]
                                        == valsdf[0]["Revenue"].min()].iloc[0]
print(minrev2020reg)
print(valsdf[0]["Region"].loc[valsdf[0]["Appropriations"]
                                        == valsdf[0]["Appropriations"].min()].iloc[0])
