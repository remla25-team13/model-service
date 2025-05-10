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

@app.route('/predict', methods=['POST'])
def predict():
  """
  Predict whether an SMS is Spam.
  ---
  consumes:
    - application/json
  parameters:
      - name: input_data
        in: body
        description: message to be classified.
        required: True
        schema:
          type: object
          required: sms
          properties:
              sms:
                  type: string
                  example: This is an example of an SMS.
  responses:
    200:
      description: "The result of the classification: 'spam' or 'ham'."
  """
  input_data = request.get_json()
  sms = input_data.get('sms')
  
  vectorizer = joblib.load("output/bow_vectorizer.pkl")
  model = joblib.load('output/sentiment_model.pkl')
  
  processed_sms = preprocessor.preprocess(sms) 
  vectorized = vectorizer.transform([processed_sms]).toarray()
  
  prediction = model.predict(vectorized)[0]
  prediction = 'Spam'
  
  res = {
      "result": prediction,
      "sms": sms
  }
  print(res)
  return jsonify(res)

@app.route('/dumbpredict', methods=['POST'])
def dumb_predict():
  """
  Predict whether a given SMS is Spam or Ham (dumb model: always predicts 'ham').
  ---
  consumes:
    - application/json
  parameters:
      - name: input_data
        in: body
        description: message to be classified.
        required: True
        schema:
          type: object
          required: sms
          properties:
              sms:
                  type: string
                  example: This is an example of an SMS.
  responses:
    200:
      description: "The result of the classification: 'spam' or 'ham'."
  """
  input_data = request.get_json()
  sms = input_data.get('sms')
  
  return jsonify({
      "result": "Spam",
      "classifier": "decision tree",
      "sms": sms
  })

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
  app.run(host="0.0.0.0", port=8080, debug=True)
    