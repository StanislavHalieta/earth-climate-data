from typing import Any, Optional
import requests
from requests.auth import HTTPBasicAuth

class HTTPRequest:
    def __init__(
        self,
        base_url: str,
        username: str | int | None = None,
        password: str | int | None = None,
        auth_token: str | int | None = None,
    ):
        if not isinstance(base_url, str):
            raise TypeError(f"Expected str for base_url, got {type(base_url).__name__}")
        
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth_token = auth_token
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ClimateDataCollector/1.0"
        })
        
        if username and password:
            self.session.auth = HTTPBasicAuth(username, password)
        elif auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})

        original_rebuild_auth = self.session.rebuild_auth
        def custom_rebuild_auth(prepared_request, response):
            old_auth = response.request.headers.get('Authorization')
            original_rebuild_auth(prepared_request, response)
            if old_auth and 'Authorization' not in prepared_request.headers:
                prepared_request.headers['Authorization'] = old_auth

        self.session.rebuild_auth = custom_rebuild_auth

    # Змінюємо внутрішній метод: додаємо **kwargs, щоб ловити verify та інші параметри
    def _make_request(self, method, endpoint, data=None, params=None, **kwargs):
        if endpoint is None:
            endpoint = ""
            
        if endpoint.startswith(('http://', 'https://')):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        headers = {}
        if method in ["POST", "PUT"] and data is not None:
            headers["Content-Type"] = "application/json"

        # Витягуємо verify з kwargs, якщо його там немає — за замовчуванням True (для безпеки інших запитів)
        verify_ssl = kwargs.get('verify', True)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if method in ["POST", "PUT"] else None,
                params=params,
                headers=headers,
                allow_redirects=True,
                verify=verify_ssl  # Використовуємо гнучкий параметр
            )

            if response.status_code == 401 or "text/html" in response.headers.get("Content-Type", "").lower():
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if method in ["POST", "PUT"] else None,
                    params=params,
                    headers=headers,
                    allow_redirects=True,
                    verify=verify_ssl
                )

            response.raise_for_status()

            if any(ext in url.lower() for ext in ['.nc', '.zip', '.he5', '.csv', '.dap', '.gz']):
                return response.content
            
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return response.json()

            return response.text
        except Exception as err:
            return {"error": "Request failed", "message": str(err)}

    # Твій оригінальний get, але тепер він вміє приймати і прокидати будь-які інші параметри через **kwargs
    def get(self, endpoint: str = "", params=None, auth_required=False, **kwargs):
        return self._make_request("GET", endpoint, params=params, **kwargs)
    
    # Решту методів post, put, delete повертаємо до твого початкового вигляду, але додаємо **kwargs
    def post(self, endpoint: str = "", data: Optional[dict | list] = None, params: Optional[dict] = None, **kwargs) -> Any:
        return self._make_request(method="POST", endpoint=endpoint, data=data, params=params, **kwargs)

    def put(self, endpoint: str = "", data: Optional[dict] = None, **kwargs) -> Any:
        # Повертаємо твій оригінальний порядок аргументів
        return self._make_request("PUT", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str = "", **kwargs) -> Any:
        return self._make_request("DELETE", endpoint, **kwargs)
    
    def authorize(self, token: str):
        self.auth_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})