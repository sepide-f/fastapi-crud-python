from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel


class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    role = Column(String, index=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str

