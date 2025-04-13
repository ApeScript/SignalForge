FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN pip install .

RUN mkdir -p logs signals reports

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["python3", "app/api/server.py"]
