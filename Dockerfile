FROM python:3-slim

EXPOSE 8000

WORKDIR /

RUN apt-get update && apt-get install wget -y && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --reload
