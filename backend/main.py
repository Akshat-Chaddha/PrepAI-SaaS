from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pdfplumber
import random
import models
from database import engine




app = FastAPI()
models.Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message": "PrepAI Backend is Live 🚀"}
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        return {"error": "Invalid credentials"}
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    from ats_engine import calculate_ats_score

score, strengths, weaknesses = calculate_ats_score(
    resume_text,
    job_description
)

new_resume = models.Resume(
    user_id=current_user.id,
    ats_score=score,
    strengths=",".join(strengths),
    weaknesses=",".join(weaknesses),
    job_description=job_description,
    resume_text=resume_text
)

db.add(new_resume)
db.commit()

return {
    "ats_score": score,
    "strengths": strengths,
    "weaknesses": weaknesses
}
@app.get("/dashboard")
def get_dashboard(current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    resumes = db.query(models.Resume).filter(
        models.Resume.user_id == current_user.id
    ).all()

    history = [r.ats_score for r in resumes]
    latest = history[-1] if history else None

    return {
        "latest_score": latest,
        "history": history
    }