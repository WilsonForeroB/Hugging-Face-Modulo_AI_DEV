FROM python:3.11-slim

# Opcional pero recomendable
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copiamos solo requirements primero para aprovechar mejor la cache
COPY requirements.txt .

# Instalamos dependencias de Python (sin nada de sistema)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:hf"]
