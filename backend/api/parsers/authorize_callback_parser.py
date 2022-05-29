from flask_restx import reqparse

authorize_callback_args = reqparse.RequestParser()

authorize_callback_args.add_argument(
    "code",
    required=True,
    help="Code that has been received from OAuth authorization in spotify after login using /authorize endpoint",
    type=str
)
