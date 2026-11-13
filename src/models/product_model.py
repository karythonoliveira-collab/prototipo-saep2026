from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    description = Column(String(120), nullable=False)
    quantity = Column(Integer, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    logs = relationship("Log", back_populates="product")

