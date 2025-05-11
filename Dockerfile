FROM python:3.12.9-slim

ARG VERSION=unknown
ARG MODE="DEV"

ENV VERSION=${VERSION%%-*}
ENV MODE=${MODE}

# Install dependencies
RUN apt-get update && apt-get install -y git wget unzip\ 
        && rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Set up service
COPY requirements.txt .
COPY src src

# Make entrypoint executable
RUN chmod +x src/entry.sh

# Set up model(s)
RUN mkdir /root/output

RUN wget https://github.com/remla25-team13/model-training/releases/download/${VERSION}/sentiment_model.pk1 \
        -O /root/output/sentiment_model.pkl

RUN wget https://github.com/remla25-team13/model-training/releases/download/${VERSION}/bow_vectorizer.pkl \
        -O /root/output/bow_vectorizer.pkl

# Install python deps
RUN python -m pip install --upgrade pip &&\
        pip install -r requirements.txt


EXPOSE 8081

ENTRYPOINT [ "/root/src/entry.sh" ]
