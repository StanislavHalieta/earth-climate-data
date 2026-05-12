from typing import Any, Optional

import requests

class HTTPRequest:
    def __init__(
        self,
        base_url: str,
        username: str | int | None = None,
        password: str | int | None = None,
        auth_token: str | int | None = None
        ):
        
        # Гвардіан-клінінг: перевіряємо, чи base_url це дійсно рядок
        if not isinstance(base_url, str):
            raise TypeError(f"Expected str for base_url, got {type(base_url).__name__}")
        
        self.base_url = base_url.rstrip('/')
        
        # Створюємо сесію. Сесія в requests — це як браузер: 
        # вона пам'ятає куки та краще обробляє редиректи.
        self.session = requests.Session()
        
        # Якщо є логін/пароль (як для NASA Earthdata), додаємо їх у сесію
        if username and password:
            self.session.auth = (username, password)
            
        # Якщо є Bearer токен (для інших API)
        if auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
            
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "ClimateDataCollector/1.0"
        })

    def _make_request(self, method, endpoint, data=None, params=None, auth_required=False):
        """
        auth_required: якщо True, ми можемо додати специфічну логіку 
        для перевірки авторизації перед відправкою.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            # Використовуємо self.session замість requests
            # handle_redirects=True дозволяє requests слідувати за посиланнями
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                allow_redirects=True  # Важливо для NASA
            )
            
            # Якщо NASA вимагає підтвердження авторизації при редиректі
            # requests зазвичай робить це автоматично, якщо сесія має .auth
            
            response.raise_for_status()
            
            try:
                return response.json()
            except ValueError:
                return response.text
                
        except requests.exceptions.HTTPError as err:
            # Якщо отримали 401 Unauthorized — значить авторизація не спрацювала
            if err.response.status_code == 401:
                return {"error": "Auth Failed", "message": "Check your credentials"}
            return {"error": f"HTTP {err.response.status_code}", "message": str(err)}
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
        """
        Метод для відправки POST запитів.
        :param endpoint: Шлях до ресурсу (наприклад, '/products/add')
        :param data: Тіло запиту (словник або список), яке конвертується в JSON
        :param params: URL параметри (те, що йде після ?)
        """
        # Додаємо перевірку типів "на льоту" (Runtime check)
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