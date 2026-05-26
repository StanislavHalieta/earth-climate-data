import pytest
from unittest.mock import patch, MagicMock
from app.helpers.http_request import HTTPRequest


def test_http_request_init_type_error():
    """1. Перевіряємо, чи працює захист від неправильного типу base_url"""
    with pytest.raises(TypeError):
        HTTPRequest(base_url=123)  # Передаємо число замість рядка


@patch("app.helpers.http_request.requests.Session.request")
def test_http_request_get_json_success(mock_request):
    """2. Тест успішного GET запиту, який повертає JSON"""
    # Створюємо фейкову відповідь від сервера NASA
    fake_response = MagicMock()
    fake_response.headers = {"Content-Type": "application/json"}
    fake_response.json.return_value = {"status": "ok", "data": "nasa_climate_metrics"}
    
    # Підсовуємо фейкову відповідь нашому моку
    mock_request.return_value = fake_response

    # Ініціалізуємо ваш клас
    client = HTTPRequest(base_url="https://nasa.gov")
    
    # Викликаємо ваш метод get
    result = client.get("v1/gmsl")

    # Перевіряємо, чи повернувся очікуваний словник
    assert result == {"status": "ok", "data": "nasa_climate_metrics"}
    
    # Перевіряємо, чи правильний URL змонтував ваш клас всередині
    mock_request.assert_called_once()
    called_kwargs = mock_request.call_args.kwargs
    assert called_kwargs["url"] == "https://nasa.gov/v1/gmsl"


@patch("app.helpers.http_request.requests.Session.request")
def test_http_request_get_netcdf_bytes(mock_request):
    """3. Тест завантаження бінарного файлу NetCDF (.nc)"""
    fake_response = MagicMock()
    fake_response.headers = {"Content-Type": "application/octet-stream"}
    fake_response.content = b"fake_binary_netcdf_bytes"
    
    mock_request.return_value = fake_response

    client = HTTPRequest(base_url="https://nasa.gov")
    
    # Викликаємо endpoint, який закінчується на .nc
    result = client.get("data_measures.nc")

    # Ваш клас має розпізнати розширення .nc і повернути байтову строку content
    assert result == b"fake_binary_netcdf_bytes"


@patch("app.helpers.http_request.requests.Session.request")
def test_http_request_exception_handling(mock_request):
    """4. Тест обробки критичних помилок мережі (блок except Exception)"""
    # Імітуємо, що під час запиту зник інтернет або впав сервер
    mock_request.side_effect = Exception("Connection timed out")

    client = HTTPRequest(base_url="https://nasa.gov")
    result = client.get("v1/gmsl")

    # Ваш код у блоці 'except Exception as err' має перехопити це 
    # і повернути словник із повідомленням про помилку
    assert result["error"] == "Request failed"
    assert "Connection timed out" in result["message"]