#!./venv/bin/python3

import pandas as pd

import string
import re
import nltk
from nltk.corpus import stopwords

import getopt, sys

options = "hf:"
long_options = ["help", "datafile"]

file_path = ""

try:
    args, values = getopt.getopt(sys.argv[1:], options, long_options)
    for arg, value in args:
        if arg in ("-h", "--help"):
            print("File path for the input dataset\n")
            sys.exit(0)
        elif arg in ("-f", "--datafile"):
            file_path = value
        else:
            print("Invalid argument: ", arg)
except getopt.error as err:
    print(str(err))
    sys.exit(1)

if file_path == None or file_path == "":
    print("Please provide a file path for the input dataset\n")
    sys.exit(1)

nltk.download("stopwords")
stopWords = set(stopwords.words("english"))

DATASET_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]
DATASET_ENCODING = "ISO-8859-1"

POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

KERAS_MODEL = "model.h5"

df = pd.read_csv(
    file_path,
    encoding=DATASET_ENCODING,
    names=DATASET_COLUMNS,
)

print("\nData before preprocessing...")

print(df.head())


def removeStopwords(text):
    tokens = []
    for token in text.split():
        if token not in stopWords:
            tokens.append(token)
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


df["preprocessed_text"] = df["text"].apply(lambda x: removeStopwords(x))
df["preprocessed_text"] = df["preprocessed_text"].apply(lambda x: removeURL(x))
df["preprocessed_text"] = df["preprocessed_text"].apply(lambda x: removeHTML(x))
df["preprocessed_text"] = df["preprocessed_text"].apply(lambda x: removeSymbols(x))

df["text"] = df["preprocessed_text"]
df.drop(columns=["preprocessed_text"], axis=1, inplace=True)

print("\nData after preprocessing...")

print(df.head())

df.to_csv("preprocessed_dataset.csv", index=False)
