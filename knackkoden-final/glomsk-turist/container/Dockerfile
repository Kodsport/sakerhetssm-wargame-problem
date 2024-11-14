FROM python:3.11.4-slim-bullseye

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install flask gunicorn

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]