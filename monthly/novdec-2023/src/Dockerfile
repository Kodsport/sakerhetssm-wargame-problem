FROM mcr.microsoft.com/playwright/python:v1.39.0-jammy

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip3 install flask playwright waitress

EXPOSE 5000

CMD waitress-serve --port=5000 app:app