
# Dockerfile pentru aplicația Flask
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
