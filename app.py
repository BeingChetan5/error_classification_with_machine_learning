import numpy as np
import pandas as pd
import uvicorn  # For asynchronous server gateway interface which id multi-thread. Where flask uses WSGI which is single thread.
from data.get_data_from_jira import get_df
from fastapi import FastAPI
from predictdata import PredictData
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from fastapi.encoders import jsonable_encoder


app = FastAPI()


@app.get('/')
def index():
    return {'welcome_msg': 'Welcome to "Test case Error Classifier" application.'}

@app.post('/train')
def train_model():
    try:
        df = get_df()
        data = df[['error_msg', 'category']]
        encoder = LabelEncoder()
        df['category'] = encoder.fit_transform(df['category'])
        X = data['error_msg']
        y = data['category']

        sgd_clf = SGDClassifier()
        pipeline = Pipeline([('vectorizer', TfidfVectorizer()), ('classifier', sgd_clf)])
        pipeline.fit(X, y)
        joblib.dump(pipeline, 'sgd_clssifier.pkl')
    except Exception as err:
        return {'Training Model': f"Failed with error: {err}"}

    return {'Training Model': "Success"}

@app.get('/predict/')
def predict_category(data:PredictData):
    data = data.dict()
    error_msg = data['error_msg']

    sgd_load_model = open('sgd_clssifier.pkl', 'rb')
    sgd_classifier = joblib.load(sgd_load_model)
    predicted_category = sgd_classifier.predict([error_msg])

    return {'Predicted Category:': predicted_category.tolist()}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
