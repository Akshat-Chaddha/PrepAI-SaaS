from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pdfplumber
import models
import schemas
import auth
from database import engine, SessionLocal

# =========================
# APP INIT
# =========================
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "PrepAI Backend is Live 🚀"}


# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# REGISTER
# =========================
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = auth.hash_password(user.password)

    db_user = models.User(
        email=user.email,
        password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully"}


# =========================
# LOGIN
# =========================
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# UPLOAD RESUME
# =========================
@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Extract text from PDF
    with pdfplumber.open(file.file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                resume_text += extracted

    # Import ATS engine
    from ats_engine import calculate_ats_score

    # For now using dummy job description
    job_description = "Software Developer Python FastAPI SQL"

    score, strengths, weaknesses = calculate_ats_score(
        resume_text,
        job_description
    )

    # Save resume record (no auth user yet — simple version)
    new_resume = models.Resume(
        user_id=1,  # temporary (replace with real auth later)
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


# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    resumes = db.query(models.Resume).filter(
        models.Resume.user_id == 1  # temporary user
    ).all()

    history = [r.ats_score for r in resumes]
    latest = history[-1] if history else None

    return {
        "latest_score": latest,
        "history": history
    }