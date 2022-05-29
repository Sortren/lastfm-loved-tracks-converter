from flask import Blueprint
from flask_restx import Api

from .lastfm_controller import lastfm_controller
from .spotify_controller import spotify_controller


api_bp = Blueprint("/api/v1", __name__, url_prefix="/api/v1")

api_v1 = Api(api_bp,
             doc="/docs",
             title="Lastfm Loved Tracks to Spotify Playlist API",
             version='1.0')

api_v1.add_namespace(lastfm_controller)
api_v1.add_namespace(spotify_controller)
