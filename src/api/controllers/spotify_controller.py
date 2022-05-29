from flask import make_response, request
from flask_restx import Namespace, Resource
import requests as req
from misc.config import Config
from api.parsers import authorize_callback_args


spotify_controller = Namespace("SpotifyController",
                               description="Spotify integration logic")


@spotify_controller.route("/search")
class Search(Resource):
    @spotify_controller.doc("")
    def get(self):
        bearer_token = request.headers.get("Authorization")
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

        return make_response(
            {
                "found_tracks": found_tracks,
                "not_found_tracks": not_found_tracks
            }, 200)


@spotify_controller.route("/playlists/<string:user_id>")
class UserPlaylist(Resource):
    @spotify_controller.doc("")
    def post(self, user_id):
        bearer_token = request.headers.get("Authorization")
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

        return make_response(playlist_created_response.json(),
                             playlist_created_response.status_code)


@spotify_controller.route("/playlists/<string:playlist_id>/tracks")
class PlaylistTracks(Resource):
    @spotify_controller.doc("")
    def put(self, playlist_id):
        bearer_token: str = request.headers.get("Authorization")
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

        return make_response(tracks_added_response.json(),
                             tracks_added_response.status_code)


@spotify_controller.route("/userProfileData")
class UserProfileData(Resource):
    @spotify_controller.doc("")
    def get(self):
        bearer_token = request.headers.get("Authorization")

        profile_data = req.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": bearer_token}
        )

        return make_response(profile_data.json(),
                             profile_data.status_code)


@spotify_controller.route("/authorize")
class Authorize(Resource):
    @spotify_controller.doc("")
    def get(self):
        scopes = 'playlist-modify-public playlist-modify-private'

        url = req.Request('GET', "https://accounts.spotify.com/authorize", params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
            'client_id': Config.SPOTIFY_CLIENT_ID
        }).prepare().url

        return make_response({"url": url}, 200)


@spotify_controller.route("/authorizeCallback")
class AuthorizeCallback(Resource):
    @spotify_controller.expect(authorize_callback_args)
    @spotify_controller.doc("")
    def get(self):
        code = request.args.get("code")

        access_data = req.post("https://accounts.spotify.com/api/token", data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
            'client_id': Config.SPOTIFY_CLIENT_ID,
            'client_secret': Config.SPOTIFY_CLIENT_SECRET
        })

        return make_response(access_data.json(),
                             access_data.status_code)


@spotify_controller.route("/temporary")
class TemporarySpotifyRedirectEndpoint(Resource):
    @spotify_controller.doc("")
    def get(self):
        return "temporary redirect endpoint after authorize"
