from flask_restx import reqparse

parser = reqparse.RequestParser()

parser.add_argument(
    "code",
    required=True,
    location='args',
    help="Code that has been received from OAuth authorization in spotify after login using /authorize endpoint",
    type=str
)
