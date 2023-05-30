import os
from typing import Annotated

from db.models import User
from db.schemas import UserCreate, UserEdit, UserLogin
from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

app = FastAPI()


class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET_KEY", 'insecure_secret_key')
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: Annotated[UserCreate, Body(embed=False)]):
    try:
        User.create(user_data.username, user_data.email, user_data.password)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with given username/email already exists'
        )


@app.post('/login', status_code=status.HTTP_204_NO_CONTENT)
async def login(
    user_data: Annotated[UserLogin, Body(embed=False)], auth: AuthJWT = Depends()
):
    if not User.login(user_data.username, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    access_token = auth.create_access_token(subject=user_data.username)
    refresh_token = auth.create_refresh_token(subject=user_data.username)
    auth.set_access_cookies(access_token)
    auth.set_refresh_cookies(refresh_token)


@app.post('/refresh', status_code=status.HTTP_204_NO_CONTENT)
async def refresh(auth: AuthJWT = Depends()):
    auth.jwt_refresh_token_required()
    current_user = auth.get_jwt_subject()
    new_access_token = auth.create_access_token(subject=current_user)
    auth.set_access_cookies(new_access_token)


@app.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(auth: AuthJWT = Depends()):
    auth.jwt_required()
    auth.unset_jwt_cookies()


@app.get('/user', status_code=status.HTTP_200_OK)
async def view_user(auth: AuthJWT = Depends()):
    auth.jwt_required()
    username = auth.get_jwt_subject()
    user = User.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


@app.patch('/user', status_code=status.HTTP_204_NO_CONTENT)
async def edit_user(
    user_data: Annotated[UserEdit, Body(embed=False)], auth: AuthJWT = Depends()
):
    auth.jwt_required()
    username = auth.get_jwt_subject()
    is_updated = User.update(username, **user_data.dict())
    if is_updated is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot update user'
        )


@app.delete('/user', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(auth: AuthJWT = Depends()):
    auth.jwt_required()
    username = auth.get_jwt_subject()
    is_deleted = User.delete(username)
    if is_deleted is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete user'
        )
    auth.unset_jwt_cookies()
