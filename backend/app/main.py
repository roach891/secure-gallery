from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from auth import auth_bp
from image import image_bp

app = Flask(__name__)

CORS(app)

load_dotenv()

app.config.from_envvar('FLASK_CONFIG',silent=True)

init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(image_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
