from sqlalchemy import Column, Integer, NotNullable, String
from database import Base

class usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100), nullable=False)
