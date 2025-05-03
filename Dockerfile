FROM python:3.12.9-slim

WORKDIR /root
COPY requirements.txt .

RUN python -m pip install --upgrade pip &&\
        pip install -r requirements.txt

COPY src src

EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD [ "src/app.py" ]