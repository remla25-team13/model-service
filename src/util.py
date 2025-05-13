import os

import requests
from tqdm import tqdm


def download_model(MODEL_VERSION: str):
    path = "/root/output/sentiment_model.pkl"
    url = f"https://github.com/remla25-team13/model-training/releases/download/{MODEL_VERSION}/sentiment_model.pk1"

    if not os.path.isfile(path):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)
    else:
        print("Model file already exist.")


def download_vectorizer(MODEL_VERSION: str):
    path = "/root/output/bow_vectorizer.pkl"
    url = f"https://github.com/remla25-team13/model-training/releases/download/{MODEL_VERSION}/bow_vectorizer.pkl"

    if not os.path.isfile(path):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192)):
                    f.write(chunk)            
    else:
        print("Vectorizer file already exists")
