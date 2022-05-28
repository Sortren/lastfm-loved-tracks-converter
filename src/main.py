from flask import Flask
from api.api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api/v1")


@app.route("/")
def home():
    return "home page"


if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)
