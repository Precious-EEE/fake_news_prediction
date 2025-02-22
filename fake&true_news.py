# -*- coding: utf-8 -*-
"""Fake&True_News.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QZ4Mz8-jak2vKeqt9HBRHYWJCSzJjOoV
"""

# Step 1: Install Kaggle API
!pip install kaggle

# Step 2: Upload kaggle.json file
from google.colab import files
files.upload()

# Step 3: Move kaggle.json to the correct location
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Step 4: Download the dataset (replace 'dataset-owner/dataset-name' with the actual dataset)
!kaggle datasets download -d jainpooja/fake-news-detection

# Step 5: Unzip the dataset
import zipfile
import os

with zipfile.ZipFile("fake-news-detection.zip", 'r') as zip_ref:
    zip_ref.extractall(".")

# List the files in the current directory
os.listdir('.')

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string

fake = pd.read_csv("/content/Fake.csv")
true = pd.read_csv("/content/True.csv")

fake.head()

true.head()

fake["class"] = 0
true["class"] = 1

fake.shape, true.shape

# Removing last 10 rows for manual testing
fake_manual_testing = fake.tail(10)
for i in range(23480,23470,-1):
    fake.drop([i], axis = 0, inplace = True)


true_manual_testing = true.tail(10)
for i in range(21416,21406,-1):
    true.drop([i], axis = 0, inplace = True)

fake.shape, true.shape

fake_manual_testing["class"] = 0
true_manual_testing["class"] = 1

fake_manual_testing.head(10)

true_manual_testing.head(10)

manual_testing = pd.concat([fake_manual_testing,true_manual_testing], axis = 0)
manual_testing.to_csv("manual_testing.csv")

df = pd.concat([fake, true], axis =0 )
df.head(10)

df.columns

df_1 = df.drop(["title", "subject","date"], axis = 1)

df_1.isnull().sum()

df_1 = df_1.sample(frac = 1)

df_1.head()

df_1.reset_index(inplace = True)
df_1.drop(["index"], axis = 1, inplace = True)

df_1.columns

df_1.head()

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

df_1["text"] = df_1["text"].apply(wordopt)

x = df_1["text"]
y = df_1["class"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

from sklearn.linear_model import LogisticRegression

LR = LogisticRegression()
LR.fit(xv_train,y_train)

pred_lr=LR.predict(xv_test)

LR.score(xv_test, y_test)

print(classification_report(y_test, pred_lr))

from sklearn.tree import DecisionTreeClassifier

DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)

pred_dt = DT.predict(xv_test)

DT.score(xv_test, y_test)

print(classification_report(y_test, pred_dt))

from sklearn.ensemble import GradientBoostingClassifier

GBC = GradientBoostingClassifier(random_state=0)
GBC.fit(xv_train, y_train)

pred_gbc = GBC.predict(xv_test)

GBC.score(xv_test, y_test)

print(classification_report(y_test, pred_gbc))

from sklearn.ensemble import RandomForestClassifier

RFC = RandomForestClassifier(random_state=0)
RFC.fit(xv_train, y_train)

pred_rfc = RFC.predict(xv_test)

RFC.score(xv_test, y_test)

print(classification_report(y_test, pred_rfc))

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = GBC.predict(new_xv_test)
    pred_RFC = RFC.predict(new_xv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nGBC Prediction: {} \nRFC Prediction: {}".format(output_lable(pred_LR[0]),                                                                                                       output_lable(pred_DT[0]),
                                                                                                              output_lable(pred_GBC[0]),
                                                                                                              output_lable(pred_RFC[0])))

news = str(input())
manual_testing(news)

news = str(input())
manual_testing(news)

news = str(input())
manual_testing(news)

import pickle

pickle.dump(GBC,open("GBC.pkl",'wb'))

pickled_model = pickle.load(open("GBC.pkl",'rb'))

def output_lable(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_GBC = pickled_model.predict(new_xv_test)
    return print("\n\nGBC Prediction: {}".format(output_lable(pred_GBC[0])))

news = str(input())
manual_testing(news)