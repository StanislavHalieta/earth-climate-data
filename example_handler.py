from flask import Blueprint

# Створюємо Blueprint
simple_bp = Blueprint("simple", __name__)

# Створюємо роут всередині Blueprint
@simple_bp.route("/hello")
def example_logic():
    return "Привіт! Це дані з окремого файлу."

@simple_bp.route("/hello2")
def example_logic2():
    return "Привіт! Це дані з окремого файлу 2."