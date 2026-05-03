from secrets import token_urlsafe


def generate_token() -> str:
    return token_urlsafe(8)
