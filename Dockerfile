# FROM python:3.6
# ADD . /app
# WORKDIR /app
# RUN pip install -r requirements.txt

FROM ubuntu:16.04
FROM python:3.6
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app