import json
from requests import Response


def handler(event, context) -> Response:
    body = {"message": "Tervetuloa uuteenaikaan!",
            "content": "Parasta koodia!"}
    return {
        "status": 200,
        "content": json.dumps(body)
    }
