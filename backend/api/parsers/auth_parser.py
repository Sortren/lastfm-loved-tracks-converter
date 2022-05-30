from flask_restx import reqparse

parser = reqparse.RequestParser()

parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    type=str,
)
