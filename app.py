from flask import Flask
from routes.expenses import expenses_bp

app = Flask(__name__)

app.register_blueprint(expenses_bp)

if __name__ == "__main__":
    app.run(debug=True)