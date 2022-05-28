from flask import Blueprint, make_response, request
from flask.views import MethodView
import requests as req
from misc.config import Config


spotify_controller = Blueprint("spotify_controller", __name__)


class Playlist(MethodView):
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


class UserProfileData(MethodView):
    def get(self):
        bearer_token = request.headers.get("Authorization")

        profile_data = req.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": bearer_token}
        )

        return make_response(profile_data.json(), profile_data.status_code)


class Authorize(MethodView):
    def get(self):
        scopes = 'playlist-modify-public playlist-modify-private'

        url = req.Request('GET', "https://accounts.spotify.com/authorize", params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
            'client_id': Config.SPOTIFY_CLIENT_ID
        }).prepare().url

        return make_response({"url": url}, 200)


class AuthorizeCallback(MethodView):
    def get(self):
        code = request.args.get("code")

        access_data = req.post("https://accounts.spotify.com/api/token", data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
            'client_id': Config.SPOTIFY_CLIENT_ID,
            'client_secret': Config.SPOTIFY_CLIENT_SECRET
        })

        return make_response(access_data.json, access_data.status_code)


class TemporarySpotifyRedirectEndpoint(MethodView):
    def get(self):
        return "temporary redirect endpoint after authorize"


spotify_controller.add_url_rule(
    "/authorize", view_func=Authorize.as_view("authorize"))

spotify_controller.add_url_rule(
    "/authorizeCallback", view_func=AuthorizeCallback.as_view("authorizeCallback"))

spotify_controller.add_url_rule(
    "/userProfileData", view_func=UserProfileData.as_view("userProfileData"))

spotify_controller.add_url_rule(
    "/playlist/<user_id>", view_func=Playlist.as_view("playlist"))

spotify_controller.add_url_rule(
    "/temporary", view_func=TemporarySpotifyRedirectEndpoint.as_view("temporary"))
