FROM python:3.9

RUN apt-get update && apt-get install -y \
    python3-tk \
    && apt-get clean

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "data.py"]
