from os import getenv

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    url=getenv("DATABASE_URL"),
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=0,
    echo=True,
)