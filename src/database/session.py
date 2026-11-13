from sqlalchemy.orm import sessionmaker

from database.engine import engine

Session = sessionmaker(
    bind=engine,
    autoflush=True
)

