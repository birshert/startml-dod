FROM python:3.10-slim

ARG OPENAI_KEY

WORKDIR /app

RUN pip install openai flask --no-cache-dir

COPY . /app

EXPOSE 55555

ENV OPENAI_KEY=$OPENAI_KEY

CMD python server.py