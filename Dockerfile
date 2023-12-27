FROM python:3.10.11-slim

WORKDIR /code

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["python", "main.py"]
