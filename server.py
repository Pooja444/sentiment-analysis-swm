#!./venv/bin/python3

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route("/predict", methods=["POST"])
def predict_tweet():
    print(request.form.to_dict(flat=False))
    json_data = request.get_json(force=True)
    print(json_data)
    return {"sentiment": "POSITIVE"}


app.run(port=5000)
