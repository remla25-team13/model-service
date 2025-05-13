FROM python:3.12.9-slim

ARG ARTIFACT_VERSION="v0.0.8"
ARG MODE="DEV"
ARG PORT=8080
ARG HOST="0.0.0.0"

ENV ARTIFACT_VERSION=${ARTIFACT_VERSION%%-*}
ENV MODE=${MODE}
ENV PORT=${PORT}
ENV HOST=${HOST}

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

# Install python deps
RUN python -m pip install --upgrade pip &&\
        pip install -r requirements.txt


EXPOSE 8081

ENTRYPOINT [ "/root/src/entry.sh" ]
