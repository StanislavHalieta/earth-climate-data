import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from app import create_app
from app.helpers import CustomJSONProvider

app = create_app()

app.json = CustomJSONProvider(app)

@app.route("/")
def get_home():
    return {
        "coords": "тестові координати", 
        "status": "працює"
    }


if __name__ == "__main__":
    # 1. Зчитуємо порт, який дає Render. Якщо його немає (локальний запуск) — беремо 5000
    port = int(os.getenv("PORT", 5000))
    
    # 2. Обов'язково ставимо host="0.0.0.0", щоб сервер відповідав на зовнішні запити хостингу
    # Також вимикаємо debug=True для продакшену (Render), щоб не навантажувати систему
    is_debug = os.getenv("FLASK_ENV") == "development"
    
    app.run(host="0.0.0.0", port=port, debug=is_debug)