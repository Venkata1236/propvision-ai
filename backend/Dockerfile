FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

COPY saved_models ./saved_models
COPY faiss_index ./faiss_index

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]