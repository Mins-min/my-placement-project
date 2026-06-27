from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Initialize FastAPI App
app = FastAPI(
    title="Placement Probability Predictor API",
    description="Backend API tailored for fastapi dev execution with fixed CORS mechanics.",
    version="1.0.0"
)

# -------------------------------------------------------------------------
# 💻 FIXED CORS MIDDLEWARE SETUP
# -------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# -------------------------------------------------------------------------
# 📋 DATA SCHEMAS (Pydantic Models)
# -------------------------------------------------------------------------
class StudentData(BaseModel):
    age: int = Field(..., ge=15, le=40)
    gender: str
    cgpa: float = Field(..., ge=0.0, le=10.0)
    branch: str
    college_tier: str
    internships_count: int = Field(..., ge=0)
    projects_count: int = Field(..., ge=0)
    certifications_count: int = Field(..., ge=0)
    coding_skill_score: int = Field(..., ge=0, le=100)

# -------------------------------------------------------------------------
# 🚀 API ENDPOINTS
# -------------------------------------------------------------------------

@app.get("/")
def read_root():
    """
    Root Endpoint: Confirms server state.
    """
    return {"message": "ATS API Running"}


@app.post("/predict")
def predict_placement(student: StudentData):
    """
    Predict Endpoint: Computes placement probability percentages.
    """
    # 🌟 Weighted Evaluation Matrix
    cgpa_score = min(student.cgpa * 4.0, 40.0)                                 # Max 40 points
    coding_score = (student.coding_skill_score / 100.0) * 25.0                 # Max 25 points
    experience_score = min(
        (student.internships_count * 8.0) + (student.projects_count * 4.0), 20.0
    )                                                                          # Max 20 points
    
    cert_score = min(student.certifications_count * 3.0, 9.0)                  # Max 9 points
    tier_bonus = 6.0 if student.college_tier == "Tier 1" else (4.0 if student.college_tier == "Tier 2" else 2.0)
    
    # Calculate base probability and clamp safely between 5.0% and 100.0%
    raw_probability = cgpa_score + coding_score + experience_score + cert_score + tier_bonus
    employability_percentage = round(max(min(raw_probability, 100.0), 5.0), 1)

    return {
        "status": "success",
        "employability": employability_percentage,
        "input_profile": {
            "branch": student.branch,
            "cgpa": student.cgpa,
            "coding_score": student.coding_skill_score
        }
    }