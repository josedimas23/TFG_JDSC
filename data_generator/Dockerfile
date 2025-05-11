FROM python:3.11-slim
WORKDIR /app

COPY data_generator/requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY data_generator/ ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "data.py"]