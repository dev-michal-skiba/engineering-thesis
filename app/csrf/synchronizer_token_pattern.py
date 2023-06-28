from fastapi import Request, Response

async def apply_csrf_protection(request: Request) -> None:
    raise NotImplementedError('Synchronizer Token Pattern is not enabled yet')


def update_csrf_cookie(response: Response) -> None:
    raise NotImplementedError('Synchronizer Token Pattern is not enabled yet')
