from flask import Flask
from example_handler import simple_bp 

app = Flask(__name__)

# Реєструємо Blueprint і даємо йому префікс
app.register_blueprint(simple_bp, url_prefix="/api")

@app.route("/")
def index():
    return "Головна сторінка (працює)"

if __name__ == "__main__":
    app.run(debug=True)