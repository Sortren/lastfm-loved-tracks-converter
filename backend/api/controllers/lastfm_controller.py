from flask import make_response, request
from flask_restx import Resource, Namespace
import requests as req

from misc.config import Config
from api.parsers import loved_tracks_args

lastfm_controller = Namespace("lastfm-controller",
                              description="Lastfm integration logic")


@lastfm_controller.route("/loved-tracks")
class LovedTracks(Resource):

    @lastfm_controller.expect(loved_tracks_args)
    @lastfm_controller.doc("")
    def get(self):
        username = request.args.get("username")
        format = request.args.get("format")

        loved_tracks = req.get(
            f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={Config.API_KEY}&format={format}"

        )

        return loved_tracks.content, loved_tracks.status_code
