from flask import Blueprint
from api.controllers import lastfm_controller, spotify_controller

api = Blueprint("api", __name__)

api.register_blueprint(lastfm_controller, url_prefix="/LastfmController")
api.register_blueprint(spotify_controller, url_prefix="/SpotifyController")
