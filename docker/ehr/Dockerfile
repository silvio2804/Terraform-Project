# ====== Backend EHR ======
FROM python:3.12-slim

# Imposta la working directory
WORKDIR /app

# Copia requirements e installa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice
COPY ehr_backend.py .

# Variabili d'ambiente default (modificabili in K8s)
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=ehr
ENV DB_USER=postgres
ENV DB_PASSWORD=secret

# Espone la porta FastAPI
EXPOSE 8000

# Comando di avvio
CMD ["uvicorn", "ehr_backend:app", "--host", "0.0.0.0", "--port", "8000"]
