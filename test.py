import pandas as pd
from initialize import initialize_dir_year, initialize_dir_region, get_amountallyr
df = pd.read_excel('SCBAA/Defaultgraph.xlsx')
year = initialize_dir_year()
region = initialize_dir_region()
reg_lst = region["value"]
for r in reg_lst:
    print(r)
    lst = list(df["Revenue"].loc[df["Region"] == r])
    for y in year:
        print(lst[year.index(y)])
