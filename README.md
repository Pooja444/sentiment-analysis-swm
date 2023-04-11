# Sentiment Analysis

An academic project - detects the sentiment of a tweet

## Follow the below steps for running this project

### Data preprocessing

```
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

### Follow the below steps for generating CSV out of the preprocessed data -

* Install the Sentiment140 data set from - [Kaggle](https://www.kaggle.com/datasets/kazanova/sentiment140)
* Run the command with the input CSV as file path `./data_preprocessing.py -f "path/to/file"`

This creates a file called 'preprocessed_dataset.csv' that contains the preprocessed data
