from statistics import mean
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
# calculate the Euclidean distance between two vectors


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

# Locate the most similar neighbors returning neighborx and neighbory


def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighborsx = list()
    neighborsy = list()
    for i in range(num_neighbors):
        neighborsx.append(distances[i][0][0])
        neighborsy.append(distances[i][0][1])
    return neighborsx, neighborsy


def predict(nby):
    return [mean(nby)]


def get_rmse(X, Y, ra):
    rmse_val = []
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=0)
    for K in range(ra):
        K = K+1
        samp = [[X_train[i], Y_train[i]] for i in range(len(X_train))]
        nbx, nby = get_neighbors(samp, X_test, K)
        pred = predict(nby)
        error = sqrt(mean_squared_error([pred], Y_test))
        rmse_val.append(error)
    return rmse_val


def get_optimalK(rmse):
    initlst = list(rmse)
    if(rmse.index(min(rmse))+1) == 1:
        initlst.remove(min(initlst))
        return ((rmse.index(min(initlst)))+1), initlst
    else:
        initlst.remove(rmse[1])
        return ((rmse.index(min(initlst)))+1), initlst


def imputearr(arr, inp, year):
    df = {"Imputed "+inp: [], "Year": []}
    for i in range(len(arr)):
        if(arr[i] == 0):
            df["Imputed "+inp].append(mean(arr))
            df['Year'].append(year[i])
    return df
