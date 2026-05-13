import os
from flask import Flask
from dotenv import load_dotenv

from app.nasa.gmsl_indicator.handler import format_gmsl_indicator_data
from app.helpers import HTTPRequest
from app.nasa import nasa_bp


# 1. Завантажуємо змінні з .env файлу в пам'ять
load_dotenv()

app = Flask(__name__)

app.register_blueprint(nasa_bp, url_prefix="/api/nasa")

@app.route("/api/dummy_data")
def get_dummy_data():
    new_request = HTTPRequest(
    base_url="https://dummyjson.com",
)

    data = new_request.get(endpoint="/products")
     
    return data        

@app.route("/api/test", methods=["GET ", "POST"])
def dummy_auth():
    new_request = HTTPRequest(
    base_url=os.getenv("ARCHIVE_PODAAC_URL"),
    username=os.getenv("NASA_USER"),
    password=os.getenv("NASA_PASS")
)

    data = new_request.get(endpoint=os.getenv("NASA_SSH_GMSL_INDICATOR_URL").lstrip('/'))
    token = data.get("accessToken")
    
    if token:
        # 2. "Вшиваємо" токен у заголовки сесії
        new_request.authorize(token=token)
        
        # 3. ВИКОРИСТАННЯ: Тепер просто робимо запит до захищеного роуту
        # Сесія сама додасть заголовок Authorization: Bearer <token>
        user_profile = new_request.get(endpoint="/auth/me")
        
        return {
            "auth_status": "Success",
            "profile": user_profile  # Поверне дані про Emily
        }
    
    return {"error": "Auth failed"}, 401

@app.route("/api/dummy_post", methods=["GET", "POST"])
def dummy_post():
    new_request = HTTPRequest(base_url="https://dummyjson.com")
    
    new_item = {
    "username": "emilys",
    "password": "emilyspass",
    "expiresInMins": 30,
    }
    
    data = new_request.post(
        endpoint="/auth/login",
        data=new_item,
        params={"credentials": "include"}
        )
    new_request.session.tokens = data.get("accessToken")  # Зберігаємо токен в сесії для подальших запитів 
    print("Received token:", new_request.session.tokens)  # Виводимо токен для перевірки
    return data

if __name__ == "__main__":
    app.run(debug=True)