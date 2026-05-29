# app/helpers/db_service.py
import os
import json
import psycopg
from flask import Response, current_app

class DatabaseService:
    def __init__(self):
        # Ініціалізуємо рядок підключення один раз для всього класу
        self.db_url = os.getenv("DATABASE_URL")

    def _get_connection(self):
        """Внутрішній помічник для швидкого створення з'єднання."""
        if not self.db_url:
            raise ValueError("DATABASE_URL variable is missing in environment!")
        return psycopg.connect(self.db_url)
    
    def create_tables_if_not_exists(self):
        """Автоматично створює таблицю для кліматичних даних, якщо її немає."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS climate_data (
                            key_name TEXT PRIMARY KEY,
                            payload JSONB NOT NULL,
                            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                        """
                    )
            print("💾 Перевірка бази даних: таблиця 'climate_data' готова до роботи.")
            return True
        except Exception as e:
            print(f"❌ Помилка ініціалізації таблиць у базі: {e}")
            return False

    def get_metric(self, key_name: str):
        """Читає JSON-метрику з бази даних та повертає Flask Response."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT payload FROM climate_data WHERE key_name = %s;", (key_name,))
                    row = cur.fetchone()
                    
                    if row and row[0]:
                        payload = row[0]
                        # Якщо з бази повернувся рядок, віддаємо як є
                        if isinstance(payload, str):
                            return Response(payload, mimetype="application/json")
                        # Якщо база повернула словник/список, серіалізуємо в текст
                        return Response(json.dumps(payload), mimetype="application/json")
                        
                    return {"error": f"Data for '{key_name}' not synced yet"}, 404
                    
        except Exception as e:
            # Перевіряємо наявність контексту Flask для безпечного логування
            if current_app:
                current_app.logger.error(f"Database read error for '{key_name}': {e}")
            else:
                print(f"❌ Помилка читання БД для '{key_name}': {e}")
            return {"error": "Internal database error"}, 500

    def save_metric(self, key_name: str, raw_payload):
        """Універсальний метод для збереження або оновлення метрики в базі."""
        try:
            # Витягуємо чистий JSON-рядок з будь-якого формату відповіді
            if hasattr(raw_payload, 'get_data'):
                json_string = raw_payload.get_data(as_text=True)
            elif isinstance(raw_payload, (dict, list)):
                json_string = json.dumps(raw_payload)
            else:
                json_string = str(raw_payload)

            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO climate_data (key_name, payload, updated_at)
                        VALUES (%s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (key_name) 
                        DO UPDATE SET payload = EXCLUDED.payload, updated_at = CURRENT_TIMESTAMP;
                        """,
                        (key_name, json_string)
                    )
            print(f"🔹 Метрика '{key_name}' успішно синхронізована.")
            return True
        except Exception as e:
            print(f"❌ Помилка запису в БД для '{key_name}': {e}")
            return False
