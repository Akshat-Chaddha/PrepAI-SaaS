from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pdfplumber
import models
import schemas
import auth
from database import engine, SessionLocal
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import auth
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
def upload_resume(
    file: UploadFile = File(...),
    job_description: str = "",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    with pdfplumber.open(file.file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                resume_text += extracted

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
# =========================
# DASHBOARD
# =========================
@app.get("/dashboard")
def get_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resumes = db.query(models.Resume).filter(
        models.Resume.user_id == current_user.id
    ).all()

    history = [r.ats_score for r in resumes]
    latest = history[-1] if history else None

    return {
        "latest_score": latest,
        "history": history
    }