import os
from flask.cli import load_dotenv
from app.services import HTTPRequest

load_dotenv()


def create_nasa_session(base_url=None) -> HTTPRequest:
    auth_token = os.getenv("NASA_TOKEN")
    nasa_user = os.getenv("NASA_USER")
    nasa_pass = os.getenv("NASA_PASS")
    raw_base_url = base_url or os.getenv("NASA_ARCHIVE_PODAAC_URL")

    session = HTTPRequest(
        base_url=raw_base_url,
        auth_token=auth_token,
        username=nasa_pass,
        password=nasa_user,
    )
    return session
