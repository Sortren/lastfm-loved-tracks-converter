from flask_restx import reqparse

authorize_callback_args = reqparse.RequestParser()

authorize_callback_args.add_argument(
    "code",
    required=True,
    type=str
)
