## imports necessary libraries
import pandas as pd
import numpy as np
import os
import sklearn.preprocessing as sk

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
regression["PaymentMethod"] = regression["PaymentMethod"].map({"Bank transfer (automatic)":1, "Credit card (automatic)":1, "Mailed check":0, "Electronic check":0})

## normalize monthly and total cost for regression
scaler = sk.MinMaxScaler()
regression[["tenure","MonthlyCharges","TotalCharges"]] = scaler.fit_transform(regression[["tenure","MonthlyCharges","TotalCharges"]])


regression.to_csv("regression_dataset.csv",",")
