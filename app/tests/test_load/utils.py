import string
from secrets import choice
from uuid import uuid4

PASSWORD_ALLOWED_CHARS = string.ascii_letters + string.digits


def generate_user_info() -> dict[str, str]:
    username = str(uuid4())
    email = f"{username}@example.com"
    password = "LoadTest1234!" + "".join(choice(PASSWORD_ALLOWED_CHARS) for _ in range(8))
    new_password = "LoadTest1234!" + "".join(choice(PASSWORD_ALLOWED_CHARS) for _ in range(8))
    return {
        "username": username,
        "email": email,
        "password": password,
        "new_password": new_password
    }
