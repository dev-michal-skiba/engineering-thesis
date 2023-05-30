from typing import Annotated

from pydantic import BaseModel, Field

EMAIL_REGEX = r'^\S+@\S+\.\S+$'
EMAIL_DESCRIPTION = 'Email is expected to follow [username]@[domain] format, ' \
                    'where domain is split by dot'
PASSWORD_REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,}$'
PASSWORD_DESCRIPTION = 'Password is expected to be at least twelve characters long, ' \
                       'include at least one uppercase letter, one lowercase letter, ' \
                       'one digit and one special sign'


class UserCreate(BaseModel):
    username: Annotated[str, Field(max_length=64)] = ...
    email: Annotated[
        str, Field(max_length=64, regex=EMAIL_REGEX, description=EMAIL_DESCRIPTION)
    ] = ...
    password: Annotated[str, Field(regex=PASSWORD_REGEX, description=PASSWORD_DESCRIPTION)] = ...


class UserLogin(BaseModel):
    username: Annotated[str, Field()] = ...
    password: Annotated[str, Field()] = ...


class UserInfo(BaseModel):
    username: str
    email: str


class UserEdit(BaseModel):
    email: Annotated[
        str, Field(max_length=64, regex=EMAIL_REGEX, description=EMAIL_DESCRIPTION)
    ] = None
    password: Annotated[str, Field(regex=PASSWORD_REGEX, description=PASSWORD_DESCRIPTION)] = None
