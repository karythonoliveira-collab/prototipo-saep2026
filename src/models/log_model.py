import enum

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship

from database import Base

class LogTypes(enum.Enum):
    entry = "entry"
    exit = "exit"



class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(LogTypes), nullable=False)
    quantity = Column(Integer, nullable=False)
    datetime = Column(DateTime, server_default=func.now())

    user_id = Column(ForeignKey("users.id", ondelete="cascade"))
    product_id = Column(ForeignKey("products.id", ondelete="cascade"))

    user = relationship("User", back_populates="logs")
    product = relationship("Product", back_populates="logs")

