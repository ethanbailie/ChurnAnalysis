## imports necessary libraries
import pandas as pd
import numpy as np
import os

## set working directory to be the folder holding the data
os.chdir(r"C:\Users\ETHAN\Desktop\Humi")

## instantiate each csv as a dataframe (FinalResult1 was empty so it is skipped)
d = pd.read_csv("d.csv")
data = pd.read_csv("data.csv")
dataset1 = pd.read_csv("dataset1.csv")
dataset2 = pd.read_csv("dataset2.csv")
dataset3 = pd.read_csv("dataset3.csv")
dataset4 = pd.read_csv("dataset4.csv")
dataset5 = pd.read_csv("dataset5.csv")
FinalResult = pd.read_csv("FinalResult.csv")
FinalResult2 = pd.read_csv("FinalResult2.csv")
test_churn = pd.read_csv("test_churn.csv")

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

dataset.to_csv("dataset.csv",",")
