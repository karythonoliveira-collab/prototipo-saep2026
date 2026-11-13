import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from database import Base

class UserRoles(enum.Enum):
    operator = "operator"
    admin = "admin"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRoles), nullable=False)

    logs = relationship("Log", back_populates="user")


