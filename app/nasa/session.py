import os
from flask.cli import load_dotenv
from app.helpers import HTTPRequest

load_dotenv()

def create_nasa_session() -> HTTPRequest:
    user = os.getenv("NASA_USER")
    password = os.getenv("NASA_PASS")
    raw_base_url = os.getenv("ARCHIVE_PODAAC_URL")
    
    session = HTTPRequest(
        base_url=raw_base_url,
        username=user,
        password=password
    )

    return session