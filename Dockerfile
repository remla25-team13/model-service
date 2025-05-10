FROM python:3.12.9-slim

ARG VERSION=unknown

RUN version="${VERSION}" && \ 
        clean="${version%%-*}" && \
        echo "$clean" && \
        echo "VERSION=$clean" >> /root/.env

ENV VERSION=$VERSION

RUN apt-get update && apt-get install -y git wget unzip\ 
        && rm -rf /var/lib/apt/lists/*

WORKDIR /root
COPY requirements.txt .
COPY src src

RUN mkdir /root/output

RUN wget https://github.com/remla25-team13/model-training/releases/download/${VERSION}/sentiment_model.pk1 \
        -O /root/output/sentiment_model.pkl

RUN wget https://github.com/remla25-team13/model-training/releases/download/${VERSION}/bow_vectorizer.pkl \
        -O /root/output/bow_vectorizer.pkl

RUN python -m pip install --upgrade pip &&\
        pip install -r requirements.txt


EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD [ "src/app.py" ]
