from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pdfplumber
import random

import models, schemas, auth
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

    ats_score = random.randint(60, 95)

    resume = models.Resume(
        filename=file.filename,
        content=text,
        ats_score=ats_score,
        user_id=1
    )
    db.add(resume)
    db.commit()

    return {"filename": file.filename, "ats_score": ats_score}