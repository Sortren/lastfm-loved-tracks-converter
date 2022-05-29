from flask_restx import reqparse

loved_tracks_args = reqparse.RequestParser()

loved_tracks_args.add_argument(
    "username",
    required=True,
    type=str
)

loved_tracks_args.add_argument(
    "format",
    required=True,
    type=str,
    choices=("json", "xml")
)
