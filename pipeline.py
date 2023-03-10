## imports necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sklearn.preprocessing as sk
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression as logistic
import statsmodels.api as sm

## set working directory to be the folder holding the data
os.chdir(r"C:\Users\ETHAN\Desktop\Humi")

## instantiate each csv as a dataframe (FinalResult1 was empty, so it is skipped)
data = pd.read_csv("data.csv")
dataset1 = pd.read_csv("dataset1.csv")
dataset2 = pd.read_csv("dataset2.csv")
dataset3 = pd.read_csv("dataset3.csv")
dataset4 = pd.read_csv("dataset4.csv")
dataset5 = pd.read_csv("dataset5.csv")

## union the datasets to make one complete table
dataset = pd.concat([dataset1,dataset2,dataset3,dataset4,dataset5])
dataset = dataset.drop(columns=["Unnamed: 0"])
dataset = pd.concat([data,dataset])
dataset = dataset[dataset.tenure != 0]

## create dataframe containing only churned customers from the complete table
churned = dataset.loc[dataset["Churn"] == "Yes"]

## create dataframe containing only non-churned customers from the complete table
current = dataset.loc[dataset["Churn"] == "No"]

## identify average spending across both churned and current customers
avg_churned_spending = churned["TotalCharges"].mean()
avg_current_spending = current["TotalCharges"].mean()

## convert boolean values into integers for regression
regression = dataset
regression["Churn"] = regression["Churn"].map({"Yes":1, "No":0})
regression["gender"] = regression["gender"].map({"Male":1, "Female":0})
regression["Partner"] = regression["Partner"].map({"Yes":1, "No":0})
regression["Dependents"] = regression["Dependents"].map({"Yes":1, "No":0})
regression["PhoneService"] = regression["PhoneService"].map({"Yes":1, "No":0})
regression["MultipleLines"] = regression["MultipleLines"].map({"Yes":1, "No":0, "No phone service":0})
regression["InternetService"] = regression["InternetService"].map({"DSL":1, "Fiber optic":1, "No":0})
regression["OnlineSecurity"] = regression["OnlineSecurity"].map({"Yes":1, "No":0, "No internet service":0})
regression["OnlineBackup"] = regression["OnlineBackup"].map({"Yes":1, "No":0, "No internet service":0})
regression["DeviceProtection"] = regression["DeviceProtection"].map({"Yes":1, "No":0, "No internet service":0})
regression["TechSupport"] = regression["TechSupport"].map({"Yes":1, "No":0, "No internet service":0})
regression["StreamingTV"] = regression["StreamingTV"].map({"Yes":1, "No":0, "No internet service":0})
regression["StreamingMovies"] = regression["StreamingMovies"].map({"Yes":1, "No":0, "No internet service":0})
regression["Contract"] = regression["Contract"].map({"Two year":1, "One year":1, "Month-to-month":0})
regression["PaperlessBilling"] = regression["PaperlessBilling"].map({"Yes":1, "No":0})
regression["PaymentMethod"] = regression["PaymentMethod"].map({"Bank transfer (automatic)":1,
                                                               "Credit card (automatic)":1, "Mailed check":0,
                                                               "Electronic check":0})

## standardize tenure, monthly costs, and total costs for regression
scaler = sk.StandardScaler()
#scaler = sk.MinMaxScaler()
regression[["tenure","MonthlyCharges","TotalCharges"]] = scaler.fit_transform(regression[["tenure","MonthlyCharges","TotalCharges"]])

## adjust the Churn columns for prediction model
y = regression["Churn"]
regression.drop(columns=["Churn"], inplace=True)

## create training and test sets (70% train, 30% test)
x_train, x_test, y_train, y_test = tts(regression, y, test_size=0.3, random_state=0)

## use statsmodel library for a prediction model creation function
def sm_model(y_train, x_train, x_test):
    x_train = sm.add_constant(x_train)
    x_test = sm.add_constant(x_test)
    logit = sm.Logit(y_train,x_train)
    model = logit.fit()
    print(model.summary())
    y_hat = list(map(round, model.predict(x_test)))
    array = np.c_[y_hat, y_test]
    print("Predicted and actual values: \n", array)
    print("Confusion Matrix: \n", metrics.confusion_matrix(y_test, y_hat))
    print("Accuracy score: ", metrics.accuracy_score(y_test, y_hat))
    return model, array

## use sklearn library for a prediction model creation function
def sk_model(y_train, x_train, x_test):
    model = logistic(max_iter=100000000)
    model.fit(x_train, y_train)
    array = np.c_[x_train.columns.tolist(), model.coef_[0]]
    intercept = model.intercept_[0]
    print('\nPrinting model coefficients and intercept summary for sklearn model:\n', array, model.intercept_)
    y_pred = model.predict(x_test)
    print('\nPrinting predicted and actual values from sklearn:\n', np.c_[y_pred, y_test])
    print('Confusion Matrix from sklearn\n', metrics.confusion_matrix(y_test, y_pred))
    plt.matshow(metrics.confusion_matrix(y_test, y_pred))
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.grid(visible=None)
    plt.show()
    print('Accuracy Scores from sklearn:\n', metrics.accuracy_score(y_test, y_pred))
    print('Classification Report from sklearn:\n', metrics.classification_report(y_test, y_pred))
    return model, array, intercept

def roc(model, x_test, y_test):
    probs = model.predict_proba(x_test)
    fpr, tpr, _ = metrics.roc_curve(y_test, probs[:, 1])
    plt.plot(fpr, tpr, marker='.')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.show()
    print('AUC: %.3f' % metrics.roc_auc_score(y_test, probs[:, 1]))

## runs the statsmodel prediction
sm_model(y_train, x_train, x_test)

## runs the sklearn prediction model
model, array, intercept = sk_model(y_train,x_train, x_test)

# Run AUC to validate the success of the sklearn model
roc(model, x_test, y_test)

## creates a subset of the regression dataframe that consists only of statistically significant variables
## in this case, statistical significance is defined by a p-value of less than 0.25 (p-value being from the logit test)
sig_regression = regression[["SeniorCitizen", "Dependents", "tenure", "PhoneService", "MultipleLines", "OnlineSecurity",
                             "OnlineBackup", "TechSupport", "Contract", "PaperlessBilling", "PaymentMethod",
                             "MonthlyCharges", "TotalCharges"]]

## redefine training and test sets for usage with the statistically significant set
x_train, x_test, y_train, y_test = tts(sig_regression, y, test_size=0.3, random_state=0)

## runs the statsmodel prediction
sm_model(y_train, x_train, x_test)

## runs the sklearn prediction model
model, array, intercept = sk_model(y_train,x_train, x_test)

# Run AUC to validate the success of the sklearn model
roc(model, x_test, y_test)

# Function to calculate the reduction percentage in odds ratio
def result(coeff, field,x, categorical=False):
    if categorical:
        exp = np.exp(x*coeff)
        print ( field, ': Odds Ratio Reduction : '+str(round((1 - exp)*100,2 ))+'%')
    else:
        exp1 = np.exp(x*coeff/regression["tenure"].std())
        exp2 = np.exp(-1*x*coeff/regression["tenure"].std())
        print ( field, ': Odds Ratio Reduction with unit increase: '+str(round((1 - exp1)*100,2 ))+'%',
                'Odds Ratio Reduction with unit decrease: '+str(round((1 - exp2)*100,2 ))+'%')

result(0.37, 'SeniorCitizen', 1, True)
result(-0.22, 'Dependents', 1, True)
result(-1.38, 'tenure', 1)
result(-1.06, 'PhoneService', 1, True)
result(0.16, 'MultipleLines', 1, True)
result(-0.48, 'OnlineSecurity', 1, True)
result(-0.37, 'OnlineBackup', 1, True)
result(-0.57, 'TechSupport', 1, True)
result(-0.91, 'Contract', 1, True)
result(0.50, 'PaperlessBilling', 1, True)
result(-0.34, 'PaymentMethod', 1, True)
result(0.87, 'MonthlyCharges', 1)
result(0.55, 'TotalCharges', 1)

