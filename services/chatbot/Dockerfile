# #For normal service without using cuda 
ARG BASE_IMAGE=python:3.10.14-slim-bullseye

FROM ${BASE_IMAGE}

RUN useradd -ms /bin/bash celery_user

COPY requirements.txt /tmp/requirements.txt

WORKDIR /chatbot

ENV CUDA_DOCKER_ARCH=all

RUN mkdir -p /chatbot/logs

COPY ./src /chatbot/src

RUN apt-get update && apt-get install -y build-essential git
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN chown -R celery_user:celery_user /chatbot

USER celery_user



