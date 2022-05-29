from flask_restx import reqparse

auth_args = reqparse.RequestParser()

auth_args.add_argument(
    "Authorization",
    location="headers",
    required=True,
    type=str,
)
