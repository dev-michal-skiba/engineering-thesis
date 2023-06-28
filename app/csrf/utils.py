from secrets import choice

from csrf.constants import (CSRF_TOKEN_ALLOWED_CHARS, CSRF_TOKEN_LENGTH,
                            CSRF_TOKEN_NAME, SAFE_METHODS)
from fastapi import Request
from starlette.responses import Response


def is_safe_http_method(request: Request) -> bool:
    return request.method in SAFE_METHODS


def get_new_csrf_token() -> str:
    return "".join(choice(CSRF_TOKEN_ALLOWED_CHARS) for i in range(CSRF_TOKEN_LENGTH))


def set_csrf_token_on_cookie(response: Response, csrf_token: str) -> None:
    response.set_cookie(
        key=CSRF_TOKEN_NAME,
        value=csrf_token,
        httponly=False,
        samesite="none",
    )


def get_csrf_token_from_cookie(request: Request) -> str:
    csrf_token = request.cookies.get(CSRF_TOKEN_NAME, '') or ''
    return str(csrf_token)


async def get_csrf_token_from_body(request: Request) -> str:
    body = await request.json()
    csrf_token = body.get(CSRF_TOKEN_NAME, '') or ''
    return str(csrf_token)
