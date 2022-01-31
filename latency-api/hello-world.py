import json
from requests import Response


def handler(event, context) -> Response:
    body = {"message": "Welcome to the new age!",
            "content": "Best possible code!"}
    return {
        "status": 200,
        "content": json.dumps(body)
    }
