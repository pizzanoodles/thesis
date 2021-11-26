from initialize import get_actualbel, get_definition, initialize_dir_region, initialize_dir_year
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
                    <h5>CURRENT INPUT: ₱{inp:,.2f} on {year}</h5>\
                    <br><h5>DATA:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>{label1}</strong> - {def1}</li>\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                            <li><strong>Training Set</strong> - is usally split from the input type(X) and forecast type(Y) that will fit from KNN Regression Model will be used for the prediction\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set.\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5><p></p>\
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


def get_insightacc(k, acc, predmods, y_tst):
    insight = '<div class="modal fade" id="insightacc" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Accuracy Score from the model</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <br><h5>DATA:</h5>\
                    <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">K</th>\
                                <th scope="col">Predictions</th>\
                                <th scope="col">Test Set</th>\
                                <th scope="col">Accuracy Score</th>\
                            </tr>\
                        </thead>\
                        <tbody>'
    for i in range(len(acc)):
        insight += '<tr>\
                <td>{k}</td>\
                <td>{pred}</td>\
                <td>{test}</td>\
                <td>{amount:0.2f}%</td>\
            </tr>'.format(k=k[i], amount=acc[i], pred=predmods[i], test=y_tst)
    insight += '</tbody>\
                    </table></br>\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Accuracy Score</strong> - the number of correctly classified data instances over the total number of data instances</li>\
                            <li><strong>Predictions</strong> - the value computed using the KNN with the corresponding K-value\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5><p></p>\
                        <p class="pl-2">The data above was created when getting the Optimal K. The Accuracy Score was computed by comparing each of the predictions and the test set in % and finally, by averaging all of the scores percentages in % also</p>\
                    </div>\
                </div>\
                    <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'
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
                    <h5>CURRENT PREDICTION: ₱{opt:,.2f} on {year}</h5>\
                    <br><h5>DATA:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>{label1}</strong> - {def1}</li>\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                            <li><strong>Training Set</strong> - is usally split from the input type(X) and forecast type(Y) that will fit from KNN Regression Model will be used for the prediction\
                            <li><strong>Test Set</strong> - is a data set used to provide an unbiased evaluation of a final model fit on the training data set.\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5>\
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
                    <h5>OPTIMAL PREDICTION: ₱{opt:,.2f} on K={optm_k}</h5>\
                    <br><h5>DATA:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5>\
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
                    <h5>LOWEST RMSE: {rmse:,.2f} on K={optm_k}</h5>\
                    <br><h5>DATA:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>RMSE(Root-Mean-Squared-Error)</strong> - is the standard deviation of the residuals (prediction errors)\
                            <li><strong>Optimal K</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5>\
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
                    <h5>INPUT: ₱{inp:,.2f}</h5><br>\
                    <h5>NEIGHBORS: {n}</h5><br>\
                    <h5>DATA IN LOWEST DISTANCE ORDER:</h5>\
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
                    <h5>OPTIMAL NEIGHBORS: {n}</h5><br>\
                    <h5>NEAREST NEIGHBORS FOUND:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Input Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(X) for the forecasting by getting the nearest neighbors using euclidean distance.</li>\
                            <li><strong>Forecast Type</strong> - is a dictionary variable containing (name,list of values) to be used as a training data set(Y) for the forecasting by averaging the nearest neighbors.</li>\
                            <li><strong>Input</strong> - the pivotal variable to start the forecasting process and it is only defined by prompting the user\
                            <li><strong>K(Neighbors)</strong> - the number of the nearest neighbors to get in the model based in the input\
                            <li><strong>Euclidean Distance</strong> - the optimal number of the nearest neighbors with the lowest rmse value\
                        </ul>\
                        <br>\
                        <h5 class="mb-2">PURPOSES:</h5>\
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
                        <h5 class="mb-2">PROCEDURE:</h5>\
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
                        <h5 class="mb-2">DEFINITIONS:</h5>\
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
# DATAVIS


def get_insightdefsurplus(surplusperyear, percents, years):
    insight = '<div class="modal fade" id="insightsurplus" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Surplus Values on each Year</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">Surplus Value</th>\
                                <th scope="col">Surplus Values Compared to Last Year</th>\
                                <th scope="col">Surplus Compared to Last Year in %</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(surplusperyear)):
        insight += '<tr>\
                <th scope="row">{year}</th>\
                <td>₱{amount:,.2f}</td>'.format(year=years[i], amount=surplusperyear[i])
        if(i == 0):
            amount2 = 0
        else:
            amount2 = surplusperyear[i]-surplusperyear[i-1]
        if(amount2 < 0):
            insight += '<td>-₱{amount2:,.2f}</td>\
                <td>-{percents}%</td>'.format(amount2=abs(amount2), percents=percents[i])
        else:
            insight += '<td>₱{amount2:,.2f}</td>\
                <td>{percents}%</td>'.format(amount2=amount2, percents=percents[i])
        insight += '</tr>'
    insight += '</tbody>\
                    </table></br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Surplus</strong> - an amount of something left over when requirements have been met; an excess of production or supply over demand. In this case the surplus is calculated by the difference of the total appropriations and revenues.</li>\
                            <li><strong>Total Appropriations</strong> - {app}</li>\
                            <li><strong>Total Revenues</strong> - {rev}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(app=get_definition("Total Appropriations"), rev=get_definition("Total Revenues"))
    return insight


def get_insightdeflinerevapp(totaldicts):
    insight = '<div class="modal fade" id="linerevapp" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Total Revenues and Appropriations of all LGUs on each Year </h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                        <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">Total Revenues</th>\
                                <th scope="col">Total Appropriations</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(totaldicts["Years"])):
        insight += '<tr>\
                <th scope="row">{year}</th>\
                <td>₱{rev:,.2f}</td>\
                <td>₱{app:,.2f}</td></tr>'.format(year=totaldicts["Years"][i], app=totaldicts["Appropriations"][i], rev=totaldicts["Revenues"][i])
    insight += '</tbody>\
                    </table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Total Revenues</strong> - {rev}</li>\
                            <li><strong>Total Appropriations</strong> - {app}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(rev=get_definition("Total Revenues"), app=get_definition("Total Appropriations"))
    return insight


def get_insightdefgauge(lat, prev, years, diff):
    insight = '<div class="modal fade" id="insightgauge" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Latest Surplus Difference from Previous Year</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                            <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Latest Surplus ({latyr})</th>\
                                <th scope="col">Previous Surplus ({prevyr})</th>\
                                <th scope="col">Difference in %</th>\
                            </tr>\
                        </thead><tbody>\
                            <tr>\
                            <td>₱{lat:,.2f}</td>\
                            <td>₱{prev:,.2f}</td>\
                            <td>{diff:.2f}%</td>\
                            </tbody></table>\
                        <br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Surplus</strong> - an amount of something left over when requirements have been met; an excess of production or supply over demand. In this case the surplus is calculated by the difference of the total appropriations and revenues.</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(lat=lat, prev=prev, diff=diff, latyr=years[-1], prevyr=years[-2])
    return insight


def get_insightdefanimch(df, year):
    region = initialize_dir_region()
    reg_lst = region["value"]
    insight = '<div class="modal fade" id="insightanim" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Total Revenues and Appropriations by Region</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">Total Revenues:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Region</th>'
    for y in year:
        insight += '<th scope="col">{yr}</th>'.format(yr=y)
    insight += '</tr>\
                        </thead><tbody>'
    for r in reg_lst:
        insight += '<tr><td>{r}</td>'.format(r=r)
        lst = list(df["Revenue"].loc[df["Region"] == r])
        for y in year:
            insight += '<td>₱{am:,.2f}</td>'.format(am=lst[year.index(y)])
        insight += '</tr>'
    insight += '</tbody></table><br>\
        <h5 class="mb-2">Total Appropriations:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Region</th>'
    for y in year:
        insight += '<th scope="col">{yr}</th>'.format(yr=y)
    insight += '</tr>\
                        </thead><tbody>'
    for r in reg_lst:
        insight += '<tr><td>{r}</td>'.format(r=r)
        lst = list(df["Appropriations"].loc[df["Region"] == r])
        for y in year:
            insight += '<td>₱{am:,.2f}</td>'.format(am=lst[year.index(y)])
        insight += '</tr>'
    insight += '         </tbody></table>\
                        <br><h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Total Revenues</strong> - {rev}</li>\
                            <li><strong>Total Appropriations</strong> - {app}</li>\
                            <li><strong>NCR</strong> - National Capital Region</li>\
                            <li><strong>CAR</strong> - Cordillera Administrative Region</li>\
                            <li><strong>BARMM</strong> - Bangsamoro Autonomous Region in Muslim Mindanao</li>\
                            <li><strong>NIR</strong> - Negros Island Region</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(rev=get_definition("Total Revenues"), app=get_definition("Total Appropriations"))
    return insight
# DATAVIS GENERATEFIGURE
# REVENUE


def get_insightlclsrces(dict):
    insight = '<div class="modal fade" id="insightlclsrc" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Tax Revenues</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Tax Revenues</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Local Sources</strong> - {def1}</li>\
                            <li><strong>Tax Revenues</strong> - {def5}</li>\
                            <li><strong>Tax Revenue - Property</strong> - {def2}</li>\
                            <li><strong>Tax Revenue - Goods and Services</strong> - {def3}</li>\
                            <li><strong>Other Local Taxes</strong> - {def4}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def1=get_definition("Local Sources"), def5=get_definition("Tax Revenues"), def2=get_definition("Tax Revenue - Property"), def3=get_definition("Tax Revenue - Goods and Services"), def4=get_definition("Other Local Taxes"))
    return insight


def get_insightntr(dict):
    insight = '<div class="modal fade" id="insightntr" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Non-Tax Revenues</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Non-Tax Revenues</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Local Sources</strong> - {def0}</li>\
                            <li><strong>Non-Tax Revenues</strong> - {def1}</li>\
                            <li><strong>Business Income</strong> - {def2}</li>\
                            <li><strong>Service Income</strong> - {def3}</li>\
                            <li><strong>Other Income and Receipts</strong> - {def4}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Local Sources"), def1=get_definition("Non-Tax Revenues"), def2=get_definition("Business Income"), def3=get_definition("Service Income"), def4=get_definition("Other Income and Receipts"))
    return insight


def get_insightext(dict):
    insight = '<div class="modal fade" id="insightext" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">External Sources</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">External Sources</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>External Sources</strong> - {def0}</li>\
                            <li><strong>Share from the National Internal Revenue Taxes (IRA)</strong> - {def1}</li>\
                            <li><strong>Share from GOCCs</strong> - {def2}</li>\
                            <li><strong>Other Shares from National Tax Collections</strong> - {def3}</li>\
                            <li><strong>Other Receipts</strong> - {def4}</li>\
                            <li><strong>Inter-local Transfer</strong> - {def5}</li>\
                            <li><strong>Capital/Investment Receipts</strong> - {def6}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("External Sources"), def1=get_definition("Share from the National Internal Revenue Taxes (IRA)"),
                                    def2=get_definition("Share from GOCCs"), def3=get_definition("Other Shares from National Tax Collections"),
                                    def4=get_definition("Other Receipts"), def5=get_definition("Inter-local Transfer"),
                                    def6=get_definition("Capital/Investment Receipts"))
    return insight


def get_insightextntc(dict):
    insight = '<div class="modal fade" id="insightextntc" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Shares from National Tax Collections</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Shares from National Tax Collections</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Other Shares from National Tax Collections</strong> - {def0}</li>\
                            <li><strong>Share from Ecozone</strong> - {def1}</li>\
                            <li><strong>Share from EVAT</strong> - {def2}</li>\
                            <li><strong>Share from National Wealth</strong> - {def3}</li>\
                            <li><strong>Share from Tobacco Excise Tax</strong> - {def4}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Other Shares from National Tax Collections"), def1=get_definition("Share from Ecozone"),
                                    def2=get_definition("Share from EVAT"), def3=get_definition("Share from National Wealth"),
                                    def4=get_definition("Share from Tobacco Excise Tax"))
    return insight


def get_insightextor(dict):
    insight = '<div class="modal fade" id="insightextor" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Other Receipts</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Other Receipts</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Other Receipts</strong> - {def0}</li>\
                            <li><strong>Grants and Donations</strong> - {def1}</li>\
                            <li><strong>Other Subsidy Income</strong> - {def2}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Other Receipts"), def1=get_definition("Grants and Donations"),
                                    def2=get_definition("Other Subsidy Income"))
    return insight


def get_insightextcir(dict):
    insight = '<div class="modal fade" id="insightextcir" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Capital/Investment Receipts</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Capital/Investment Receipts</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{lbl}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(lbl=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Capital/Investment Receipts</strong> - {def0}</li>\
                            <li><strong>Sale of Capital Assets</strong> - {def1}</li>\
                            <li><strong>Sale of Investments</strong> - {def2}</li>\
                            <li><strong>Proceeds from Collections of Loans Receivable</strong> - {def3}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Capital/Investment Receipts"), def1=get_definition("Sale of Capital Assets"),
                                    def2=get_definition("Sale of Investments"), def3=get_definition("Proceeds from Collections of Loans Receivable"))
    return insight


def get_insightrec(dict):
    insight = '<div class="modal fade" id="insightrec" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Receipts from Borrowings on all Years</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">Receipts from Borrowings</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Receipts'])):
        insight += '<tr>\
            <td>{yr}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(yr=dict["Year"][i], amount=dict["Receipts"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Receipts from Borrowings</strong> - {def0}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Receipts from Borrowings"))
    return insight


def get_insightrevgauge(lat, prev, year, diff):
    insight = '<div class="modal fade" id="insightrevgauge" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Current Revenue Difference from Previous Year</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                            <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Current Revenue ({latyr})</th>\
                                <th scope="col">Previous Revenue ({prevyr})</th>\
                                <th scope="col">Difference in %</th>\
                            </tr>\
                        </thead><tbody>\
                            <tr>\
                            <td>₱{lat:,.2f}</td>\
                            <td>₱{prev:,.2f}</td>\
                            <td>{diff:.2f}%</td>\
                            </tbody></table>\
                        <br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Revenues</strong> - the money generated from normal business operations, calculated as the average sales price times the number of units sold</li>\
                            <li><strong>Total Revenues</strong> - {def0}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(lat=lat, prev=prev, diff=diff, latyr=year, prevyr=year-1, def0=get_definition("Total Revenues"))
    return insight


def get_insightforegauge(lat, prev, year, diff, forec):
    insight = '<div class="modal fade" id="insightforegauge" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Current {forec} Difference from Previous Year</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                            <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Current {forec} ({latyr})</th>\
                                <th scope="col">Previous {forec} ({prevyr})</th>\
                                <th scope="col">Difference in %</th>\
                            </tr>\
                        </thead><tbody>\
                            <tr>\
                            <td>₱{lat:,.2f}</td>\
                            <td>₱{prev:,.2f}</td>\
                            <td>{diff:.2f}%</td>\
                            </tbody></table>\
                        <br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>{forec}</strong> - {def0}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
            <div class="modal-footer">\
                    <button class="insightbtn modalbtns" data-bs-target="#generalinsight" data-bs-toggle="modal">Help</button>\
                </div>\
         </div></div></div>'.format(forec=forec, lat=lat, prev=prev, diff=diff, latyr=year, prevyr=year-1, def0=get_definition(forec))
    return insight


def get_insightappgauge(lat, prev, year, diff):
    insight = '<div class="modal fade" id="insightappgauge" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Current Appropriation Difference from Previous Year</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                            <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Current Appropriation ({latyr})</th>\
                                <th scope="col">Previous Appropriation ({prevyr})</th>\
                                <th scope="col">Difference in %</th>\
                            </tr>\
                        </thead><tbody>\
                            <tr>\
                            <td>₱{lat:,.2f}</td>\
                            <td>₱{prev:,.2f}</td>\
                            <td>{diff:.2f}%</td>\
                            </tbody></table>\
                        <br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Appropriations</strong> - when money is set aside money for a specific and particular purpose or purposes</li>\
                            <li><strong>Total Appropriations</strong> - {def0}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(lat=lat, prev=prev, diff=diff, latyr=year, prevyr=year-1, def0=get_definition("Total Appropriations"))
    return insight


def get_insightcontapp(dict):
    insight = '<div class="modal fade" id="insightcontapp" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Continuing Appropriations</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Continuing Appropriations</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{label}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(label=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Continuing Appropriations</strong> - {def0}</li>\
                            <li><strong>General Public Services</strong> - {def1}</li>\
                            <li><strong>Education</strong> - {def2}</li>\
                            <li><strong>Health, Nutrition and Population Control</strong> - {def3}</li>\
                            <li><strong>Labor and Employment</strong> - {def4}</li>\
                            <li><strong>Housing and Community Development</strong> - {def5}</li>\
                            <li><strong>Social Services and Social Welfare</strong> - {def6}</li>\
                            <li><strong>Economic Services</strong> - {def7}</li>\
                            <li><strong>Other Purposes</strong> - {def8}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Continuing Appropriations"), def1=get_definition("General Public Services"),
                                    def2=get_definition("Education"), def3=get_definition("Health, Nutrition and Population Control"),
                                    def4=get_definition("Labor and Employment"), def5=get_definition("Housing and Community Development"),
                                    def6=get_definition("Social Services and Social Welfare"), def7=get_definition("Economic Services"),
                                    def8=get_definition("Other Purposes"))
    return insight


def get_insightothersoths(dict):
    insight = '<div class="modal fade" id="insightothersoths" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Other Purposes > Others</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Others</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{label}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(label=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Others</strong> - {def0}</li>\
                            <li><strong>Maintenance and Other Operating Expenses</strong> - {def1}</li>\
                            <li><strong>Personnel Services</strong> - {def2}</li>\
                            <li><strong>Capital Outlay</strong> - {def3}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Others"), def1=get_definition("Maintenance and Other Operating Expenses"),
                                    def2=get_definition("Personnel Services"), def3=get_definition("Capital Outlay"))
    return insight


def get_insightdebts(dict):
    insight = '<div class="modal fade" id="insightdebts" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Other Purposes > Debt Services</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Debt Services</th>\
                                <th scope="col">Amount</th>\
                            </tr>\
                        </thead><tbody>'
    for i in range(len(dict['Label'])):
        insight += '<tr>\
            <td>{label}</td>\
            <td>₱{amount:,.2f}</td></tr>'.format(label=dict["Label"][i], amount=dict["Amount"][i])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Debt Services</strong> - {def0}</li>\
                            <li><strong>Financial Expense</strong> - {def1}</li>\
                            <li><strong>Amortization</strong> - {def2}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("Debt Service"), def1=get_definition("Financial Expense"),
                                    def2=get_definition("Amortization"))
    return insight


def get_insightsocex(dict):
    insight = '<div class="modal fade" id="insightsocex" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Other Purposes > Social Expenditures</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Social Expenditures</th>\
                                <th scope="col">Maintenance and Other Operating Expenses</th>\
                                <th scope="col">Capital Outlay</th>\
                            </tr>\
                        </thead><tbody>'
    for i in dict:
        insight += '<tr>\
            <th scope="row">{label}</th>\
            <td>₱{amount:,.2f}</td>\
                <td>₱{amount2:,.2f}</td></tr>'.format(label=i, amount=dict[i][0], amount2=dict[i][1])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Social Expenditures</strong> - measure of the extent to which countries assume responsibility for supporting the standard of living of disadvantaged or vulnerable groups</li>\
                            <li><strong>LDRRMF(Local Disaster Risk Reduction and Management Fund)</strong> - {def0}</li>\
                            <li><strong>20% Development Fund</strong> - {def5}</li>\
                            <li><strong>Share from National Wealth</strong> - {def1}</li>\
                            <li><strong>Allocation for Senior Citizens and PWD</strong> - {def2}</li>\
                            <li><strong>Maintenance and Other Operating Expenses</strong> - {def3}</li>\
                            <li><strong>Capital Outlay</strong> - {def4}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("LDRRMF"), def1=get_definition("Share from National Wealth"),
                                    def2=get_definition("Allocation for Senior Citizens and PWD"), def3=get_definition("Maintenance and Other Operating Expenses"),
                                    def4=get_definition("Capital Outlay"), def5=get_definition("20% Development Fund"))
    return insight


def get_insightcurrapp(dict):
    insight = '<div class="modal fade" id="insightcurrapp" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Current Appropriations</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <div class="container-fluid">\
                        <h5 class="mb-2">DATA:</h5>\
                        <table class="table ml-2">\
                            <thead>\
                            <tr>\
                                <th scope="col">Current Appropriations</th>\
                                <th scope="col">Personnel Services</th>\
                                <th scope="col">Maintenance and Other Operating Expenses</th>\
                                <th scope="col">Capital Outlay</th>\
                            </tr>\
                        </thead><tbody>'
    for i in dict:
        insight += '<tr>\
            <th scope="row">{label}</th>\
            <td>₱{amount:,.2f}</td>\
                <td>₱{amount2:,.2f}</td>\
                    <td>₱{amount3:,.2f}</td></tr>'.format(label=i, amount=dict[i][0], amount2=dict[i][1], amount3=dict[i][2])
    insight += '</tbody></table><br>\
                        <h5 class="mb-2">DEFINITIONS:</h5>\
                        <ul class="list-unstyled">\
                            <li><strong>Social Expenditures</strong> - measure of the extent to which countries assume responsibility for supporting the standard of living of disadvantaged or vulnerable groups</li>\
                            <li><strong>LDRRMF(Local Disaster Risk Reduction and Management Fund)</strong> - {def0}</li>\
                            <li><strong>20% Development Fund</strong> - {def5}</li>\
                            <li><strong>Share from National Wealth</strong> - {def1}</li>\
                            <li><strong>Allocation for Senior Citizens and PWD</strong> - {def2}</li>\
                            <li><strong>Maintenance and Other Operating Expenses</strong> - {def3}</li>\
                            <li><strong>Capital Outlay</strong> - {def4}</li>\
                        </ul>\
                        <br>\
                    </div>\
        </div>\
         </div></div></div>'.format(def0=get_definition("LDRRMF"), def1=get_definition("Share from National Wealth"),
                                    def2=get_definition("Allocation for Senior Citizens and PWD"), def3=get_definition("Maintenance and Other Operating Expenses"),
                                    def4=get_definition("Capital Outlay"), def5=get_definition("20% Development Fund"))
    return insight
