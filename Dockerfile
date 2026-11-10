
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY config_check/ config_check/
COPY rules.yaml .
COPY examples/ examples/

ENTRYPOINT ["python", "-m", "config_check"]
