import os

from csrf import double_submit_cookie as dsc
from csrf import synchronizer_token_pattern as stp
from csrf.constants import (DOUBLE_SUBMIT_COOKIE_CSRF_PROTECTION_METHOD,
                            SYNCHRONIZER_TOKEN_PATTERN_CSRF_PROTECTION_METHOD)
from csrf.utils import is_safe_http_method
from fastapi import Request, Response

CSRF_PROTECTION_METHOD = os.getenv('CSRF_PROTECTION_METHOD')


async def apply_csrf_protection(request: Request) -> None:
    if is_safe_http_method(request):
        return
    if CSRF_PROTECTION_METHOD == DOUBLE_SUBMIT_COOKIE_CSRF_PROTECTION_METHOD:
        await dsc.apply_csrf_protection(request)
    if CSRF_PROTECTION_METHOD == SYNCHRONIZER_TOKEN_PATTERN_CSRF_PROTECTION_METHOD:
        await stp.apply_csrf_protection(request)


def update_csrf_cookie(response: Response) -> None:
    if CSRF_PROTECTION_METHOD == DOUBLE_SUBMIT_COOKIE_CSRF_PROTECTION_METHOD:
        dsc.update_csrf_cookie(response)
    if CSRF_PROTECTION_METHOD == SYNCHRONIZER_TOKEN_PATTERN_CSRF_PROTECTION_METHOD:
        stp.update_csrf_cookie(response)
