from csrf.constants import CSRF_TOKEN_ALLOWED_CHARS, CSRF_TOKEN_LENGTH
from csrf.utils import (get_csrf_token_from_body, get_csrf_token_from_cookie,
                        get_new_csrf_token, set_csrf_token_on_cookie)
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

async def apply_csrf_protection(request: Request) -> None:
    cookie_csrf_token = get_csrf_token_from_cookie(request)
    body_csrf_token = await get_csrf_token_from_body(request)
    if (
        not cookie_csrf_token
        or len(cookie_csrf_token) != CSRF_TOKEN_LENGTH
        or not all(char in CSRF_TOKEN_ALLOWED_CHARS for char in cookie_csrf_token)
        or cookie_csrf_token != body_csrf_token
    ):
        _raise_csrf_http_error()


def _raise_csrf_http_error() -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="CSRF validation failed"
    )


def update_csrf_cookie(response: Response) -> None:
    csrf_token = get_new_csrf_token()
    set_csrf_token_on_cookie(response, csrf_token)
