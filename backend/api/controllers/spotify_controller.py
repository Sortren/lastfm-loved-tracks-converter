from flask import request
from flask_restx import Namespace, Resource, fields
import requests as req

import conf.settings as settings
from api.parsers import auth_parser, authorize_callback_parser


spotify_controller = Namespace("spotify-controller",
                               description="Spotify integration logic")


@spotify_controller.route("/search")
class Search(Resource):
    track_model = spotify_controller.model("Track to search", {
        "track_name": fields.String("Name of the track"),
        "artist_name": fields.String("Name of the artist")
    })

    tracks_to_search_model = spotify_controller.model("Tracks to search", {
        "tracks": fields.List(fields.Nested(track_model))
    })

    @spotify_controller.doc("")
    @spotify_controller.expect(auth_parser, tracks_to_search_model)
    def get(self):
        auth_args = auth_parser.parse_args()
        bearer_token = auth_args.get("Authorization")
        
        request_body_payload = request.get_json().get("tracks")

        found_tracks = []
        not_found_tracks = []

        for track in request_body_payload:
            track_name = track.get("track_name")
            artist_name = track.get("artist_name")

            track_searched_response = req.get(
                "https://api.spotify.com/v1/search",
                params={
                    "q": track_name,
                    "type": "track",
                    "limit": 20
                },
                headers={
                    "Authorization": bearer_token
                })

            is_found = False

            for searched_track in track_searched_response.json().get("tracks").get("items"):
                if artist_name in searched_track.get("artists")[0].get("name"):
                    found_tracks.append(searched_track.get("uri"))
                    is_found = True
                    break

            if is_found is False:
                not_found_tracks.append(f"{track_name}, {artist_name}")

        return {
            "found_tracks": found_tracks,
            "not_found_tracks": not_found_tracks
        }, 200


@spotify_controller.route("/playlists/<string:user_id>")
class UserPlaylist(Resource):
    playlist_model = spotify_controller.model("Playlist", {
        "name": fields.String("Spotify username for whom the playlist will be added"),
        "description": fields.String("Description of a playlist"),
        "public": fields.Boolean("Should playlist be public")
    })

    @spotify_controller.doc("")
    @spotify_controller.expect(auth_parser, playlist_model)
    def post(self, user_id):
        auth_args = auth_parser.parse_args()
        bearer_token = auth_args.get("Authorization")

        request_body_payload = request.get_json()

        playlist_created_response = req.post(
            f"https://api.spotify.com/v1/users/{user_id}/playlists",
            json={
                "name": request_body_payload.get("name"),
                "description": request_body_payload.get("description"),
                "public": request_body_payload.get("public")
            },
            headers={
                "Authorization": bearer_token
            }
        )

        return playlist_created_response.json(), playlist_created_response.status_code


@spotify_controller.route("/playlists/<string:playlist_id>/tracks")
class PlaylistTracks(Resource):
    tracks_model = spotify_controller.model("Tracks", {
        "tracks": fields.List(fields.String("List of tracks URIs"))
    })

    @spotify_controller.expect(auth_parser, tracks_model)
    @spotify_controller.doc("")
    def put(self, playlist_id):
        auth_args = auth_parser.parse_args()
        bearer_token = auth_args.get("Authorization")
        
        tracks_payload: list[str] = request.get_json().get("tracks")
        tracks: str = ",".join(tracks_payload)

        tracks_added_response = req.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            params={
                "uris": tracks,
            },
            headers={
                "Authorization": bearer_token
            }
        )

        return tracks_added_response.json(), tracks_added_response.status_code


@spotify_controller.route("/user-profile-data")
class UserProfileData(Resource):
    @spotify_controller.expect(auth_parser)
    @spotify_controller.doc("")
    def get(self):
        auth_args = auth_parser.parse_args()
        bearer_token = auth_args.get("Authorization")

        profile_data = req.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": bearer_token}
        )

        return profile_data.json(), profile_data.status_code


@spotify_controller.route("/authorize")
class Authorize(Resource):
    @spotify_controller.doc("")
    def get(self):
        scopes = 'playlist-modify-public playlist-modify-private'

        url = req.Request('GET', "https://accounts.spotify.com/authorize", params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID
        }).prepare().url

        return {"url": url}, 200


@spotify_controller.route("/authorize-callback")
class AuthorizeCallback(Resource):
    @spotify_controller.expect(authorize_callback_parser)
    @spotify_controller.doc("")
    def get(self):
        authorize_callback_args = authorize_callback_parser.parse_args()
        code = authorize_callback_args.get("code")

        access_data = req.post("https://accounts.spotify.com/api/token", data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET
        })

        return access_data.json(), access_data.status_code


@spotify_controller.route("/temporary")
class TemporarySpotifyRedirectEndpoint(Resource):
    @spotify_controller.doc("")
    def get(self):
        return "temporary redirect endpoint after authorize"
