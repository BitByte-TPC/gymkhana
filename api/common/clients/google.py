from typing import Any, Mapping

from google.auth.transport import requests
from google.oauth2 import id_token

from api import settings


class GoogleClient:
    """Client to connect to google APIs."""

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    def verify_id_token(self, google_id_token: str) -> Mapping[str, Any]:
        """Returns verified data in `google_id_token` JWT.
        Throws:
            `ValueError` if `google_id_token` verification fails.
            `GoogleAuthError` if issuer is invalid.
        """
        return id_token.verify_oauth2_token(google_id_token, requests.Request())


google_client = GoogleClient(settings.GOOGLE_OAUTH2_KEY, settings.GOOGLE_OAUTH2_SECRET)

__all__ = ['google_client']
