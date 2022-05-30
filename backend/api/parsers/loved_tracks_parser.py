from flask_restx import reqparse

parser = reqparse.RequestParser()

parser.add_argument(
    "username",
    required=True,
    location='args',
    type=str
)

parser.add_argument(
    "format",
    required=True,
    location='args',
    type=str,
    choices=("json", "xml")
)
