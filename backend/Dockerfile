FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    terraform \
    unzip \
    curl \
    && curl "https://releases.hashicorp.com/terraform/1.14.7/terraform_1.14.7_linux_amd64.zip" -o /tmp/tf.zip \
    && unzip /tmp/tf.zip -d /usr/local/bin/ \
    && rm /tmp/tf.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
