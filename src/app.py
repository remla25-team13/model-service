"""
Flask API for the Restaurant sentiment analysis model(s).
"""

import os
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger

# from lib_ml import prepare, _extract_message_len, _text_process TODO temp

app = Flask(__name__)
swagger = Swagger(app)

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
    
    # TODO uncomment once lib-ml and the model setup is fully clarified
    #processed_sms = prepare(sms) 
    #model = joblib.load('output/model.joblib')
    #prediction = model.predict(processed_sms)[0]
    prediction = 'Spam'
    
    res = {
        "result": prediction,
        "classifier": "decision tree",
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
    
    version = version.split('-')[0] # git describe --tags returns in the format TAG-COMMIT INFO, but we want just the tag
    
    return jsonify({
      "version": version
    })

if __name__ == '__main__':
    # clf = joblib.load('output/model.joblib') TODO insert actual model here
    app.run(host="0.0.0.0", port=8080, debug=True)