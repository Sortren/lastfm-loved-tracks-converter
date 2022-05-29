from flask import Flask
from api.controllers import api_bp
from misc.config import Config

app = Flask(__name__)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run("127.0.0.1", debug=Config.DEBUG)
