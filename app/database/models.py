from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from ..database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(10), unique=True, nullable=False)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(Integer, unique=True, nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=1)
    role = relationship("Role", back_populates="users")



