from flask import render_template, url_for, request, redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import KNeighborsRegressor

def forecasting(inp):
    X = [[50], [54], [52], [60]]
    y = [20, 24, 25, 30]
    neigh = KNeighborsRegressor(n_neighbors=3)
    neigh.fit(X, y)
    print(neigh.predict([[inp]]))
    return neigh.predict([[inp]])