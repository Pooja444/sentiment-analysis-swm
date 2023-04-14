#!./venv/bin/python3

import pickle
import pandas as pd

from flask import Flask, request
from flask_cors import CORS

import tensorflow as tf
from transformers import BertTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

import string
import re
import nltk
from nltk.corpus import stopwords
import numpy as np

from sklearn.metrics import f1_score

nltk.download("stopwords")
stopWords = set(stopwords.words("english"))

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

POSITIVE = "POSITIVE"
NEUTRAL = "NEUTRAL"
NEGATIVE = "NEGATIVE"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

MODEL_SVM = "SVM"
MODEL_RNN = "RNN"
MODEL_NAIVE_BAYES = "Naive Bayes"
MODEL_BERT = "Bert BiLSTM"


@app.route("/predict", methods=["POST"])
def predict_tweet():
    print(request.form.to_dict(flat=False))
    json_data = request.get_json(force=True)
    model = json_data["model"]
    tweet = json_data["tweet"]
    result = predict(model, tweet)
    return {
        "sentiment": result["label"],
        "confidence_score": result["score"],
    }


def preprocess_input_tweet(text):
    def removeStopwords(text):
        tokens = []
        for token in text.split():
            if token.lower() not in stopWords:
                tokens.append(token.lower())
        return " ".join(tokens)

    def removeURL(text):
        url = re.compile(r"https?://\S+|www\.\S+")
        return url.sub(r"", text)

    def removeHTML(text):
        html = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        return re.sub(html, "", text)

    def removeSymbols(text):
        table = str.maketrans("", "", string.punctuation)
        return text.translate(table)

    preprocessed_text = removeStopwords(text)
    preprocessed_text = removeURL(preprocessed_text)
    preprocessed_text = removeHTML(preprocessed_text)
    preprocessed_text = removeSymbols(preprocessed_text)

    return preprocessed_text


def decode_sentiment(score, include_neutral=False):
    if include_neutral:
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE


def encode(data):
    max_length = 140
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    tokens = tokenizer.batch_encode_plus(
        data, max_length=max_length, padding="max_length", truncation=True
    )

    return tf.constant(tokens["input_ids"])


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def predict(text, model, include_neutral=False):
    pickled_model = pickle.load(open(f"./models/pickle-files/{model}.pkl", "rb"))
    score = ""
    label = ""
    preprocessed_text = preprocess_input_tweet(text)
    if model == MODEL_BERT:
        x_encoded = encode([preprocessed_text])
        score = str(pickled_model.predict([x_encoded])[0])
        label = decode_sentiment(score, include_neutral=include_neutral)
    elif model == MODEL_SVM:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
        text_vect = vectorizer.transform([preprocessed_text])
        label = pickled_model.predict([text_vect])[0]
        raw_score = model.decision_function(text_vect)[0]
        score = str(sigmoid(raw_score))
    elif model == MODEL_NAIVE_BAYES:
        prediction = pickled_model.predict([preprocessed_text])
        df = pd.read_csv(
            "preprocessed_dataset.csv",
            encoding="latin",
            names=["target", "id", "date", "flag", "user", "text"],
        )
        df.drop(columns=["id", "date", "user", "flag"], inplace=True)
        df = df[["text", "target"]]
        _, X_test, _, y_test = train_test_split(
            df["text"], df["target"], test_size=0.2, random_state=42
        )
        label = prediction[0]
        y_pred_cnb = pickled_model.predict(X_test)
        score = "F1 score: " + str(f1_score(y_test, y_pred_cnb, average="macro"))
    elif model == MODEL_RNN:
        label = "Uncertain - RNN is not a good model for sentiment analysis"
        score = "0"

    return {"label": label, "score": score}


app.run(port=5000)
