FROM python:3.12.9-slim

ARG VERSION=unknown

ENV VERSION=$VERSION

RUN apt-get update && apt-get install -y git \ 
        && rm -rf /var/lib/apt/lists/*

WORKDIR /root
COPY requirements.txt .

RUN python -m pip install --upgrade pip &&\
        pip install -r requirements.txt

COPY src src

EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD [ "src/app.py" ]
