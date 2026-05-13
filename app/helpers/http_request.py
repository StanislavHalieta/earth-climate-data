from typing import Any, Optional

import requests
from requests.auth import HTTPBasicAuth

class HTTPRequest:
    def __init__(
        self,
        base_url: str,
        username: str | int | None = None,
        password: str | int | None = None,
        auth_token: str | int | None = None
        ):
        
        if not isinstance(base_url, str):
            raise TypeError(f"Expected str for base_url, got {type(base_url).__name__}")
        
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        
        if username and password:
            self.session.auth = (username, password)
            
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
            
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "ClimateDataCollector/1.0"
        })

    def _make_request(self, method, endpoint, data=None, params=None, auth_required=False):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        auth = HTTPBasicAuth(self.username, self.password) if self.username and self.password else None

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                auth=auth,
                allow_redirects=True
            )

            if "text/html" in response.headers.get("Content-Type", "").lower():
                response = self.session.request(
                    method=method,
                    url=url,
                    allow_redirects=True
                )

            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return response.json()

            if endpoint.endswith('.nc'):
                return response.content

            return response.text
        except Exception as err:
            return {"error": "Request failed", "message": str(err)}
    # Методи get, post і т.д.
    def get(self, endpoint, params=None, auth_required=False):
        return self._make_request("GET", endpoint, params=params, auth_required=auth_required)
    
    def post(
        self, 
        endpoint: str, 
        data: Optional[dict | list] = None, 
        params: Optional[dict] = None
    ) -> Any:
        if not isinstance(endpoint, str):
            raise TypeError(f"Endpoint must be str, got {type(endpoint).__name__}")
            
        return self._make_request(
            method="POST", 
            endpoint=endpoint, 
            data=data, 
            params=params
        )

    # Для повної картини додамо ще PUT та DELETE в такому ж стилі
    def put(self, endpoint: str, data: Optional[dict] = None) -> Any:
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Any:
        return self._make_request("DELETE", endpoint)
    
    def authorize(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})