# Heart Disease Prediction — FastAPI + Docker

This is a **ready-to-run** template for your assignment. It includes:
- FastAPI app with `/health`, `/info`, `/predict`
- Prebuilt demo model at `model/heart_model.joblib` (trained on synthetic data so API runs out-of-the-box)
- `train.py` to retrain on the real Kaggle dataset
- Dockerfile and docker-compose for local run
- Clear steps for cloud deployment

> **NOTE:** Replace the demo model with the **real Kaggle Heart Disease dataset** to meet course expectations.

## 1) Project structure
```
app/
  main.py
  schema.py
  model_utils.py
data/
  heart.csv                # (optional – put Kaggle CSV here to retrain)
model/
  heart_model.joblib       # prebuilt demo model
Dockerfile
docker-compose.yaml
requirements.txt
train.py
README.md
```

## 2) Local run (Docker)
```bash
docker-compose build
docker-compose up
# Swagger UI: http://localhost:8000/docs
```

### Example predict (curl)
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "age": 56, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250, "fbs": 0,
  "restecg": 1, "thalach": 150, "exang": 0, "oldpeak": 1.0, "slope": 1,
  "ca": 0, "thal": 2
}'
```

## 3) Retrain with real data
1. Download the Kaggle dataset CSV (e.g., `heart.csv`) and place it at `data/heart.csv`.
2. Run:
```bash
# inside project root
python train.py   # saves to model/heart_model.joblib
```
3. Rebuild the container to pick up the new model:
```bash
docker-compose build --no-cache
docker-compose up -d
```

If your Kaggle file uses a different target column name, `train.py` will look for one of:
`target`, `num`, `presence`, `outcome`.

## 4) Deploy to Cloud (general Docker flow)
- Push this repo to GitHub
- On your cloud (Render/Railway/AWS ECS/Google Cloud Run/Heroku container):
  - Choose **Docker** as environment
  - Point build context to repository root
  - Expose port **8000**
  - Start command is already in the Dockerfile (`uvicorn app.main:app --host 0.0.0.0 --port 8000`)

## 5) Endpoints
- `GET /health` → `{"status": "ok"}`
- `GET /info` → model name + feature list
- `POST /predict` → `{ "heart_disease": true/false, "probability": float }`

## 6) Notes
- Feature schema follows common Heart dataset columns: `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal`.
- The demo model is **only for running the API**. For grading, **retrain with Kaggle data** and commit `model/heart_model.joblib`.
