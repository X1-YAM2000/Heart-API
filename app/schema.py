from pydantic import BaseModel, Field

class HeartInput(BaseModel):
    age: float = Field(..., ge=0, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="1=male, 0=female")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: float = Field(..., ge=0, description="Resting blood pressure")
    chol: float = Field(..., ge=0, description="Serum cholestoral in mg/dl")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (1=true; 0=false)")
    restecg: int = Field(..., ge=0, le=2, description="Resting electrocardiographic results (0-2)")
    thalach: float = Field(..., ge=0, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina (1=yes; 0=no)")
    oldpeak: float = Field(..., description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., ge=0, le=2, description="The slope of the peak exercise ST segment (0-2)")
    ca: int = Field(..., ge=0, le=4, description="Number of major vessels (0-4) colored by fluoroscopy")
    thal: int = Field(..., ge=0, le=3, description="Thalassemia (0=unknown/NA, 1=fixed defect, 2=normal, 3=reversible defect)")
