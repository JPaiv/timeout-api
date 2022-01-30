import os
import boto3
import json
import logging
import os
from requests.models import Response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: dict, context: dict) -> Response:
    body: dict = _get_body_from_event(event)
    logger.info(json.dumps(body))


def _get_body_from_event(event: dict):
    body: dict = event["body"]
    body: dict = json.loads(body)
    logging.info(body)
    return body


def _create_response(body):
    if "email_status" in body:
        return {
            "status": 400,
            "content": json.dumps(body)
        }
    else:
        return {
            "status": 200,
            "content": json.dumps(body)
        }
