import ast
import json
dict = {"Year":[2016,2017,2018,2019,2020],"X":[1,2,3,4,5],"Y":[1,2,3,4,5]}
year = [2016,2017,2018]
dict_samp = {"Year":[],"X":[],"Y":[]}
for i in range(len(dict["Year"])):
    if year[-1] < dict["Year"][i]:
        dict_samp["Year"].append(dict["Year"][i])
        dict_samp["X"].append(dict["X"][i])
        dict_samp["Y"].append(dict["Y"][i])
print(dict_samp)