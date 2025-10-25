# FastAPI + Uvicorn + Scikit-learn
FROM python:3.11-slim

# System deps (optional but useful)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Env
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH="model/heart_model.joblib"

EXPOSE 8000

# Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
