from urllib.parse import urlparse


def validate_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])

    except AttributeError:
        return False
