from initialize import get_actualbel, get_definition
# FORECASTING


def get_insightinp(year, dict, inptype, inp):
    insight = '<div class="modal fade" id="insightinp" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Input Type: {inptype}</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <h6>CURRENT INPUT: ₱{inp:,.2f} on {year}</h6>\
                    <br><h6>DATA:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">{inptype}</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(inptype=inptype, inp=float(inp), year=year[-1]+1)
    for i in range(len(dict['Year'])):
        insight += '<tr>\
                <th scope="row">{year}</th>\
                <td>₱{amount:,.2f}</td>\
            </tr>'.format(year=dict["Year"][i], amount=dict[inptype][i])
    insight += '</tbody>\
                    </table></br>\
                    <div class="container-fluid">\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>{label1}</strong> - {def1}</li>\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                            <li><strong>Training Set</strong> - is usally split from the input type(X) and forecast type(Y) that will fit from KNN Regression Model will be used for the prediction\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set.\
                        </ul>\
                        <br>\
                        <h6 class="mb-2">PURPOSES:</h6><p></p>\
                        <p class="pl-2">The data above will be used in the following:\
                        <ul>\
                            <li>RMSE(Root-Mean-Square-Error) for getting the Optimal K</li>\
                            <ul><li>80% of the data set will be used as training data set</li>\
                                <li>20% of the data set will be used as test data set</li>\
                                    </ul>\
                            <li>Training data set for the prediction by getting the closest neighbors with the value of Optimal K</li>\
                        </ul>\
                        The Imputed values are computed by getting the mean of the existing data set but not with the current or previous inputs.<br> The Previous Inputs will be stored and used as a training data set if the prediction is called again for the continuous years.<br> The Current Input will be the basis of the output by getting closest values with KNN Regression implementation.</p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'.format(label1=get_actualbel(inptype), def1=get_definition(get_actualbel(inptype)))
    return insight


def get_insightfore(year, dict, forectype, output):
    insight = '<div class="modal fade" id="insightfore" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Forecast Type: {forectype}</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <h6>CURRENT PREDICTION: ₱{opt:,.2f} on {year}</h6>\
                    <br><h6>DATA:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">{forectype}</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(forectype=forectype, opt=output[0], year=year[-1]+1)
    for i in range(len(dict['Year'])):
        insight += '<tr>\
                <th scope="row">{year}</th>\
                <td>₱{amount:,.2f}</td>\
            </tr>'.format(year=dict["Year"][i], amount=dict[forectype][i])
    insight += '</tbody>\
                    </table></br>\
                    <div class="container-fluid">\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>{label1}</strong> - {def1}</li>\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                            <li><strong>Training Set</strong> - is usally split from the input type(X) and forecast type(Y) that will fit from KNN Regression Model will be used for the prediction\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set.\
                        </ul>\
                        <br>\
                        <h6 class="mb-2">PURPOSES:</h6>\
                        <p class="pl-2">The data above will be used in the following:\
                        <ul>\
                            <li>RMSE(Root-Mean-Squared-Error) for getting the Optimal K</li>\
                            <ul><li>80% of the data set will be used as training data set</li>\
                                <li>20% of the data set will be used as test data set</li>\
                                    </ul>\
                            <li>Training data set for the prediction by getting the closest neighbors with the value of Optimal K</li>\
                        </ul>\
                        The Imputed values are computed by getting the mean of the existing data set but not with the current or previous predictions.<br> The Previous Predictions will be stored and used as a test data set if forecasting is called again for the continuous years.<br> The Current Prediction is the output by getting closest values with KNN Regression implementation.</p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'.format(label1=get_actualbel(forectype), def1=get_definition(get_actualbel(forectype)))
    return insight


def get_insightopts(pred, optm_k, df, forectype):
    lst = list(df["Predicted "+forectype])
    lst.append(pred[0])
    insight = '<div class="modal fade" id="insightopts" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">All Predictions with different K Values</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <h6>OPTIMAL PREDICTION: ₱{opt:,.2f} on K={optm_k}</h6>\
                    <br><h6>DATA:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">K</th>\
                                <th scope="col">Predicted {forectype}</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(forectype=forectype, opt=pred[0], optm_k=optm_k)
    for i in range(len(df['K'])):
        insight += '<tr>\
                <th scope="row">{k}</th>\
                <td>₱{amount:,.2f}</td>\
            </tr>'.format(k=df["K"][i], amount=df["Predicted "+forectype][i])
    insight += '</tbody>\
                    </table></br>\
                    <div class="container-fluid">\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h6 class="mb-2">PURPOSES:</h6>\
                        <p class="pl-2">The data above shows the different outputs with different K values and was gathered during the rmse check for the Optimal K. The data can be used as a range for basis instead of using a single outcome however, the rmse of the data provided must not be ignored since there is a chance that the prediction has an exponentially higher residuals than the optimal value.\
                        The graph can be used to show the relationship between the K and the predicted outputs depending on the growing number of K and data training set for different outcomes.</p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'
    return insight


def get_insightrmse(df, df2):
    insight = '<div class="modal fade" id="insightrmse" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">RMSE Evaluation</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <h6>LOWEST RMSE: {rmse:,.2f} on K={optm_k}</h6>\
                    <br><h6>DATA:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">K</th>\
                                <th scope="col">RMSE</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(rmse=df2["RMSE"][0], optm_k=df2["K"][0])
    for i in range(len(df['K'])):
        insight += '<tr>\
                <th scope="row">{k}</th>\
                <td>{rmse:,.2f}</td>\
            </tr>'.format(k=df["K"][i], rmse=df["RMSE"][i])
    insight += '</tbody>\
                    </table></br>\
                    <div class="container-fluid">\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h6 class="mb-2">PURPOSES:</h6>\
                        <p class="pl-2">The data above shows the rmse values of different K values for the Optimal K. The data can be used to check the other predictions of their rmse values.\
                        The graph can be used to show the relationship between the K and the rmse values depending on the growing number of K and data traning set that will be used to split train:test ratio of 80:20.</p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'
    return insight


def get_insightneighbors(df, dict_neigh, inptype, forectype, inp, dist, distances):
    insight = '<div class="modal fade" id="insightneigh" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Nearest Neighbors</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <h6>INPUT: ₱{inp:,.2f}</h6><br>\
                    <h6>NEIGHBORS: {n}</h6><br>\
                    <h6>DATA IN LOWEST DISTANCE ORDER:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">{inptype}(X)</th>\
                                <th scope="col">{forectype}(Y)</th>\
                                <th scope="col">Distance Between X and Input</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(inp=float(inp), inptype=inptype, forectype=forectype, n=len(distances))
    for i in range(len(distances)):
        insight += '<tr>\
                <td>₱{inp:,.2f}</td>\
                <td>₱{fore:,.2f}</td>\
                <td>{dist:,.2f}</td>\
            </tr>'.format(inp=distances[i][0][0], fore=distances[i][0][1], dist=distances[i][1])
    insight += '</tbody>\
                    </table></br>\
                    <h6>OPTIMAL NEIGHBORS: {n}</h6><br>\
                    <h6>NEAREST NEIGHBORS FOUND:</h6>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">{inptype}(X)</th>\
                                <th scope="col">{forectype}(Y)</th>\
                                <th scope="col">Distance Between X and Input</th>\
                            </tr>\
                        </thead>'.format(n=len(dict_neigh[inptype]), inp=float(inp), inptype=inptype, forectype=forectype,)
    for i in range(len(dict_neigh[inptype])):
        insight += '<tr>\
                <td>₱{inp:,.2f}</td>\
                <td>₱{fore:,.2f}</td>\
                <td>{dist:,.2f}</td>\
            </tr>'.format(inp=dict_neigh[inptype][i], fore=dict_neigh[forectype][i], dist=distances[i][1])
    insight += '</tbody>\
                    </table></br><div class="container-fluid">\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>Input Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(X) for the forecasting by getting the nearest neighbors using euclidean distance.</li>\
                            <li><strong>Forecast Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(Y) for the forecasting by averaging the nearest neighbors.</li>\
                            <li><strong>Input</strong> - the pivotal variable to start the forecasting process and it is only defined by prompting the user\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>Euclidean Distance</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h6 class="mb-2">PURPOSES:</h6>\
                        <p class="pl-2">The data above shows all of the existing neighbors and all of the nearest neighbors found using the Optimal K.\
                        The graph can be used to show the distances between the points using the Euclidean distance formula. The distance will be calculated using the x and the input only since the y is the missing data that the algorithm has to predict. </p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'
    return insight


def get_insightgeneral():
    insight = '<div class="modal fade" id="generalinsight" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">KNN Regression</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h6 class="mb-2">PROCEDURE:</h6>\
                        <ol><li>User enters an input along with its input type(X) and the forecast type(Y) to fit in the algorithm</li>\
                            <li>The input type(X) and the forecast type(Y) will be used to get the corresponding types of the existing data from the spreadsheets as training data set for getting the prediction</li>\
                            <li>The training data set will now get the list of the RMSE of different K values through the iteration of KNN Regression </li>\
                            <ol><li>Split the training data set with the ratio of 80:20 as train:test data</li>\
                                <li>Iterate through the different K values and compute the RMSE of the predicted values and test values on each iteration</li></ol>\
                                <li>Get the smallest RMSE value of that K value for the Optimal K</li>\
                                <li>Get the nearest neighbors of the input type(X) using the Euclidean distance</li>\
                                <li>Average the forecast type(Y) of the nearest neighbors of the input type(X)</li>\
                            </ol>\
                        <br>\
                        <h6 class="mb-2">DEFINITIONS:</h6>\
                        <ul class="list-unstyled">\
                            <li><strong>KNN Regression</strong> - is a non-parametric method that, in an intuitive manner, approximates the association between independent variables and the continuous outcome by averaging the observations in the same neighbourhood.</li>\
                            <li><strong>Input Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(X) for the forecasting by getting the nearest neighbors using euclidean distance.</li>\
                            <li><strong>Forecast Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(Y) for the forecasting by averaging the nearest neighbors.</li>\
                            <li><strong>Input</strong> - the pivotal variable to start the forecasting process and it is only defined by prompting the user\
                            <li><strong>Output</strong> - the result variable of the implementation of the KNN Regression process\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Training Set</strong> - is usally split from the input type(X) and forecast type(Y) that will fit from KNN Regression Model will be used for the prediction\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set.\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                            <li><strong>Euclidean Distance</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
        <div class="modal-footer">\
                    <button id="generalhelp" class="insightbtn modalbtns" data-bs-target="" data-bs-toggle="modal">Back</button>\
                </div>\
         </div></div></div>'
    return insight
