from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from ..config import DB_RUL

engine = create_engine(DB_RUL) 

Base = declarative_base()

Session = sessionmaker(bind=engine)

def get_sesion():
    session = Session()
    try:
        yield session
    finally:
        session.close()