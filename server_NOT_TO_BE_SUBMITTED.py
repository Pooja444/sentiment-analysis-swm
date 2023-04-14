#!./venv/bin/python3

from flask import Flask, request
from flask_cors import CORS

TWEET1 = "Just had the best day ever at the beach! Sun, sand, and waves. Can't wait to go back! #summerfun #beachday"
TWEET2 = "Feeling so frustrated with this never-ending traffic. Why does it always have to be this way? #trafficwoes #ugh"
TWEET3 = "Just got my dream job offer! So excited to start this new chapter in my life. #dreamjob #careermove"
TWEET4 = "The film does a good job of balancing this large cast and it’s just a fun superhero movie with a lot of heart."
TWEET5 = "So disappointed with the customer service at this store. They were rude and unhelpful. #customerservicefail #disappointed"

MODEL_SVM = "SVM"
MODEL_RNN = "RNN"
MODEL_NAIVE_BAYES = "Naive Bayes"
MODEL_BERT = "Bert BiLSTM"

OUTPUTS_DICT = {
    MODEL_SVM: {
        TWEET1: {"label": "POSITIVE", "score": "0.6136981900168118"},
        TWEET2: {"label": "NEGATIVE", "score": "0.06964910343834048"},
        TWEET3: {"label": "POSITIVE", "score": "0.7847887549257667"},
        TWEET4: {"label": "POSITIVE", "score": "0.7873562540387439"},
        TWEET5: {"label": "NEGATIVE", "score": "0.03726305645904526"},
    },
    MODEL_BERT: {
        TWEET1: {"label": "POSITIVE", "score": "0.9870897531509399"},
        TWEET2: {"label": "NEGATIVE", "score": "0.003583848476409912"},
        TWEET3: {"label": "POSITIVE", "score": "0.9832967519760132"},
        TWEET4: {"label": "POSITIVE", "score": "0.9945693016052246"},
        TWEET5: {"label": "NEGATIVE", "score": "0.0036315321922302246"},
    },
}

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route("/predict", methods=["POST"])
def predict_tweet():
    print(request.form.to_dict(flat=False))
    json_data = request.get_json(force=True)
    model = json_data["model"]
    tweet = json_data["tweet"]
    return {
        "sentiment": OUTPUTS_DICT[model][tweet]["label"],
        "confidence_score": OUTPUTS_DICT[model][tweet]["score"],
    }


app.run(port=5000)
