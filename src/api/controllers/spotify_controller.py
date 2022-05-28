from flask import Blueprint, make_response, request
from flask.views import MethodView
import requests as req
from misc.config import Config


spotify_controller = Blueprint("spotify_controller", __name__)


class Login(MethodView):
    def get(self):
        scopes = 'user-library-read'

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

        response = req.post("https://accounts.spotify.com/api/token", data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Config.SPOTIFY_REDIRECT_URI,
            'client_id': Config.SPOTIFY_CLIENT_ID,
            'client_secret': Config.SPOTIFY_CLIENT_SECRET
        }).json()

        return make_response(response, 200)


class TemporarySpotifyRedirectEndpoint(MethodView):
    def get(self):
        return "temporary redirect endpoint after authorize"


spotify_controller.add_url_rule(
    "/login", view_func=Login.as_view("login"))


spotify_controller.add_url_rule(
    "/authorizeCallback", view_func=AuthorizeCallback.as_view("authorizeCallback"))

spotify_controller.add_url_rule(
    "/temporary", view_func=TemporarySpotifyRedirectEndpoint.as_view("temporary"))
