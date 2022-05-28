from flask import Blueprint, make_response, request
from flask.views import MethodView
import requests as req
from misc.config import Config


lastfm_controller = Blueprint("lastfm_controller", __name__)


class LovedTrack(MethodView):
    def get(self):
        username = request.args.get("username")
        format = request.args.get("format")

        loved_tracks = req.get(
            f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={Config.API_KEY}&format={format}"

        )

        return make_response(loved_tracks.content, loved_tracks.status_code)


lastfm_controller.add_url_rule(
    "/lovedTrack", view_func=LovedTrack.as_view("LovedTrack"))
