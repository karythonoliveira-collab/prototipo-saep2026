from sqlalchemy import create_engine, Base
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/empresa"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread=False"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()