# -*- coding: utf-8 -*-
"""picklefile.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rJ2bwKMdSMrJwD5fXFIf8Gp2kpnXmdeU
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

df=pd.read_csv("tweets.csv")

# function to Vectorize the text using TFIDF
tfidf = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1, 2))
train_tf = tfidf.fit_transform(df['tweet'])
test_tf = tfidf.transform(df["tweet"])

X_train_tf, X_test_tf, y_train_tf, y_test_tf =train_test_split(train_tf,df.target,test_size=0.2,random_state=2020)

model=LogisticRegression(C=1.0)
model.fit(X_train_tf,y_train_tf)

pred=model.predict(X_test_tf)
print(pred)

filename='disaster_prediction'
pickle.dump(model,open(filename,'wb'))

pickle.load(open(filename,'rb'))