"""
Flask API for the Restaurant sentiment analysis model(s).
"""

import os

import joblib
import requests
from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from lib_ml import Preprocessor
from tqdm import tqdm


def download_model(MODEL_VERSION: str, MODEL_TYPE):
    path = f"output/model_{MODEL_TYPE}_{MODEL_VERSION}.jbl"
    url = f"https://github.com/remla25-team13/model-training/releases/download/{MODEL_VERSION}/model-{MODEL_TYPE}.jbl"

    print(f"Downloading {MODEL_TYPE}@{MODEL_VERSION}")

    if not os.path.isfile(path):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)
        else:
            print("Could not find file.")
    else:
        print("Model file already exist.")


def download_vectorizer(MODEL_VERSION: str):
    path = f"output/vectorizer_{MODEL_VERSION}.pkl"
    url = f"https://github.com/remla25-team13/model-training/releases/download/{MODEL_VERSION}/vectorizer.pkl"

    if not os.path.isfile(path):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)
        else:
            print("Could not find file.")
    else:
        print("Vectorizer file already exists")


model_version = os.getenv("MODEL_VERSION", "v2.0.0")
mode = os.getenv("MODE", "DEV")
port = os.getenv("PORT", 8080)
host = os.getenv("HOST", "0.0.0.0")
service_version = os.getenv("ARTIFACT_VERSION", "v2.0.0")
model_type = os.getenv("MODEL_TYPE", "gauss")

debug = False if mode == "PROD" else True

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
preprocessor = Preprocessor()

print("Downloading model files")
download_model(model_version, model_type)
download_vectorizer(model_version)


@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint returning a greeting.
    ---
    responses:
      200:
        description: A greeting message
    """
    return "Hello, World! From model-service."


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict the sentiment of a review.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: review to be classified.
          required: True
          schema:
            type: object
            required: review
            properties:
                review:
                    type: string
                    example: This is an example of a review.
    responses:
      200:
        description:
          "The result of the classification: 'Positive' (1) or 'Negative' (0)."
        schema:
          type: object
          properties:
            result:
              type: number
              example: 1
            review:
              type: string
              example: This is an example of a review.
    """
    input_data = request.get_json()
    review = input_data.get("review")

    vectorizer = joblib.load(f"output/vectorizer_{model_version}.pkl")
    model = joblib.load(f"output/model_{model_type}_{model_version}.jbl")

    processed_sms = preprocessor.preprocess(review)
    vectorized = vectorizer.transform([processed_sms]).toarray()

    prediction = model.predict(vectorized)[0]

    res = {"result": str(prediction), "review": review}

    return jsonify(res)


@app.route("/version")
def version():
    """
    Show model service version
    ---
    consumes:
      - nothing
    responses:
      200:
        description: "The service version"
    """
    return jsonify({"version": service_version})


if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
