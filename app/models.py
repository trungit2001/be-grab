from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from passlib.hash import bcrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement="auto", primary_key=True, nullable=False)
    username = Column(String(32), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False, unique=True)
    created_date = Column(DateTime, server_default=func.now())
    full_name = Column(String(64))
    address = Column(String(128))
    phone_number = Column(String(12))
    gender = Column(Boolean, default=False)

    post = relationship("Post", back_populates="author")

    def __init__(
        self,
        username: str,
        hashed_password: str,
        created_date: DateTime,
        full_name: str,
        address: str,
        phone_number: str,
        gender: bool = False
    ):
        self.username = username
        self.hashed_password = hashed_password
        self.created_date = created_date
        self.full_name = full_name
        self.address = address
        self.phone_number = phone_number
        self.gender = gender

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def __repr__(self) -> str:
        return "<User(username='%s', hashed_password='%s', created_date='%s' \
            full_name='%s', address='%s', phone_number='%s', gender='%s')>" % (
                self.username,
                self.hashed_password,
                self.created_date,
                self.full_name,
                self.address,
                self.phone_number,
                self.gender
        )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement="auto", primary_key=True, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(4096), nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    last_modified_date = Column(DateTime, onupdate=func.now())
    status = Column(Boolean, default=False)

    author = relationship("User", back_populates="posts")

    def __init__(
        self,
        author_id: int,
        title: str,
        created_date: DateTime = func.now(),
        last_modified_date: DateTime = func.now(),
        status: bool = False,
    ):
        self.author_id = author_id
        self.title = title
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.status = status

    def __repr__(self):
        return "Post<(user_id='%s', title='%s', created_date='%s', last_modified_date='%s', status='%s')>" % (
            self.user_id,
            self.title,
            self.created_date,
            self.last_modified_date,
            self.status
        )