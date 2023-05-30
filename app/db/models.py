from __future__ import annotations

import bcrypt
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError

from .database import Base, Session, engine
from .schemas import UserInfo


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    @staticmethod
    def create(username: str, email: str, password: str) -> None:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        user = User(username=username, email=email, hashed_password=hashed_password)
        session = Session()
        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise

    @staticmethod
    def login(username: str, password: str) -> bool:
        session = Session()
        try:
            user = session\
                .query(User)\
                .filter(User.username == username)\
                .filter(User.is_active == True)\
                .one()
            is_password_correct = bcrypt.checkpw(
                password=password.encode('utf-8'),
                hashed_password=user.hashed_password.encode('utf-8')
            )
            if is_password_correct:
                return True
            return False
        except SQLAlchemyError:
            return False

    @staticmethod
    def get(username: str) -> UserInfo | None:
        session = Session()
        try:
            user = session\
                .query(User)\
                .filter(User.username == username)\
                .filter(User.is_active == True)\
                .one()
        except SQLAlchemyError:
            return None
        return UserInfo(username=user.username, email=user.email)

    @staticmethod
    def update(username: str, **kwargs) -> bool:
        kwargs = dict(filter(lambda item: item[1] is not None, kwargs.items()))
        if 'password' in kwargs:
            password = kwargs.pop('password')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            kwargs['hashed_password'] = hashed_password
        session = Session()
        try:
            session \
                .query(User) \
                .filter(User.username == username) \
                .update(kwargs)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return False
        return True

    @staticmethod
    def delete(username: str) -> bool:
        session = Session()
        try:
            session\
                .query(User)\
                .filter(User.username == username)\
                .update({User.is_active: False})
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            return False
        return True


Base.metadata.create_all(engine)
