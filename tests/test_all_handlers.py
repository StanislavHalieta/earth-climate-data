# tests/test_all_handlers.py
import pytest
import json
from flask import Response
from app.services import DatabaseService


@pytest.fixture
def client():
    """Фікстура для створення тестового клієнта Flask."""
    from main import app

    app.config["TESTING"] = True
    app.url_map.strict_slashes = False
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_supabase_read(monkeypatch):
    """Глобальна фікстура, яка підміняє базу даних."""

    def mock_get_metric(self, key_name: str):
        fake_climate_data = [{"date": "2026-01-01", "value": 42.0}]
        return Response(json.dumps(fake_climate_data), mimetype="application/json")

    monkeypatch.setattr(DatabaseService, "get_metric", mock_get_metric)


def test_every_endpoint_status_200(client):
    """Тест динамічно збирає роути та послідовно їх перевіряє."""
    from app.constants import FULL_ROUTES_FOR_README

    url_list = list(set([path for _, path in FULL_ROUTES_FOR_README]))

    if not url_list:
        url_list = ["/api/nasa/gmsl"]

    print(f"\n🚀 Запуск перевірки для {len(url_list)} ендпоінтів...")

    for url in url_list:
        if url.count("/api") > 1:
            url = "/" + url.lstrip("/").replace("api/", "", 1)

        if url in ["/api/nasa", "/api/noaa", "/api/peltier", "/api/noaa/vostok"]:
            if not url.endswith("/"):
                url += "/"

        response = client.get(url)
        assert (
            response.status_code == 200
        ), f"🚨 Помилка на роуті '{url}': статус {response.status_code}"
