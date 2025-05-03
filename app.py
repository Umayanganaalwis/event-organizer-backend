from flask import Flask
from routes.auth import auth_bp
from routes.events import events_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(events_bp)

if __name__ == "__main__":
    app.run(debug=True)