"""
Flask API for the Restaurant sentiment analysis model(s).
"""

import os
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger

from lib_ml import Preprocessor

app = Flask(__name__)
swagger = Swagger(app)
preprocessor = Preprocessor()

@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint returning a greeting.
    ---
    responses:
      200:
        description: A greeting message
    """
    return "Hello, World! From app-service."

@app.route('/predict', methods=['POST'])
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
      description: "The result of the classification: 'spam' or 'ham'."
  """
  input_data = request.get_json()
  review = input_data.get('review')
  
  vectorizer = joblib.load("output/bow_vectorizer.pkl")
  model = joblib.load('output/sentiment_model.pkl')
  
  processed_sms = preprocessor.preprocess(review) 
  vectorized = vectorizer.transform([processed_sms]).toarray()
  
  prediction = model.predict(vectorized)[0]
  prediction = "Positive" if prediction == 1 else "Negative"

  res = {
      "result": prediction,
      "sms": review
  }
  
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
  version = os.getenv("VERSION", "unknown")

  return jsonify({
    "version": version
  })

if __name__ == '__main__':
  mode = os.getenv("MODE", "DEV")
  debug = False if mode == 'PROD' else True
  
  app.run(host="0.0.0.0", port=8081, debug=debug)
    