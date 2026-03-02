import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("postgresql://prepai_db_wn2m_user:wS9FCPQHg1vCLsyJWRcRNAZfDtT0gGD5@dpg-d6in0aruibrs73ae8mag-a.singapore-postgres.render.com/prepai_db_wn2m")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()