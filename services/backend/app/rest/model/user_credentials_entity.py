from rest.model.database import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    password = Column(String(60), nullable=False)

    token = relationship("Token", uselist=False, back_populates="user", cascade="all, delete-orphan")