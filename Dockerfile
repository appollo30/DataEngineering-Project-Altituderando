FROM python:3.8

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY src/. ./src
COPY data/. ./data

CMD ["python", "./src/insertion.py"]
