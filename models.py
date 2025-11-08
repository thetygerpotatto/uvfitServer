from sqlalchemy import Integer, CheckConstraint, Column, ForeignKey, Integer, String, Boolean, Time
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100), nullable=False)
    # Relaciones ORM
    data = relationship("UserData", back_populates="user")

class UserData(Base):
    __tablename__ = "user_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    height = Column(Integer)
    weight = Column(Integer)
    gender = Column(String(255), 
                    CheckConstraint("gender IN ('MALE', 'FEMALE', 'OTHER')"))
    activity = Column(String(255), 
                    CheckConstraint("activity IN ('LOW', 'MEDIUM', 'HIGH')"))
    laydowntime = Column(Time)
    isNew = Column(Boolean)


    #Relaciones
    user = relationship("Usuario", back_populates="data")

