FROM python:3.9.5

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update -y \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && apt-get clean

CMD ['uvicorn', 'main:app', '--reload']