from statistics import mean
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
# calculate the Euclidean distance between two vectors


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[0])**2
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
    return neighborsx, neighborsy, distances


def get_distances(dist):
    lst = []
    for i in range(len(dist)):
        lst.append(dist[i][1])
    return lst


def predict(nby):
    return [mean(nby)]


def get_rmse(X, Y):
    rmse_val = []
    acc = []
    opt = []
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=None, shuffle=False)
    for K in range(len(X_train)):
        K = K+1
        samp = [[X_train[i], Y_train[i]] for i in range(len(X_train))]
        nbx, nby, dist = get_neighbors(samp, X_test, K)
        pred = [predict(nby)[0] for i in range(len(Y_test))]
        error = sqrt(mean_squared_error(pred, Y_test))
        rmse_val.append(error)
        acclst = []
        opt.append(pred)

        for i in range(len(pred)):
            if pred[i] < Y_test[i]:
                acclst.append(pred[i]/Y_test[i]*100)
            else:
                acclst.append(Y_test[i]/pred[i]*100)
        acc.append(mean(acclst))
    acc.remove(acc[0])
    opt.remove(opt[0])
    return rmse_val, acc, opt, Y_test


def get_optimalK(rmse):
    initlst = list(rmse)
    initlst.remove(rmse[0])
    if(rmse.index(min(initlst))+1) == 1:
        return 2, initlst
    else:
        return ((rmse.index(min(initlst)))+1), initlst


def imputearr_lst(arr):
    samparr = list(arr)
    for i in range(len(samparr)):
        if(arr[i] == 0):
            samparr[i] = mean(arr)
    return samparr
