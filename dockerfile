FROM python:3.11-slim

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip setuptools==57.5.0
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]