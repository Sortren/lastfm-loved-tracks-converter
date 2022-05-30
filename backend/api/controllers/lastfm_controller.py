from flask import request, current_app
from flask_restx import Resource, Namespace
import requests as req

import conf.settings as settings
from api.parsers import loved_tracks_parser

lastfm_controller = Namespace("lastfm-controller",
                              description="Lastfm integration logic")


@lastfm_controller.route("/loved-tracks")
class LovedTracks(Resource):

    @lastfm_controller.expect(loved_tracks_parser)
    @lastfm_controller.doc("")
    def get(self):
        loved_tracks_args = loved_tracks_parser.parse_args()
        username = loved_tracks_args.get("username")
        format = loved_tracks_args.get("format")


        loved_tracks = req.get(
            f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={settings.LASTFM_API_KEY}&format={format}"
        )
        
        current_app.logger.info(f"Provided payload ?username={username}&format={format} Has been sent to Lastfm API")
        current_app.logger.info(f"Lastfm API returned code {loved_tracks.status_code} and payload: {loved_tracks.json()}")
        
        
        return loved_tracks.json(), loved_tracks.status_code
