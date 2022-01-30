import os
from urllib import response
import boto3
import json
import logging
import os
from requests.models import Response
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: dict, context: dict) -> Response:
    logger.info(json.dumps(event))
    body: dict = _get_body_from_event(event)
    logger.info(json.dumps(body))
    body, item = _query_dynamo_by_id(body)
    response = _create_response(body)
    return response


def _get_body_from_event(event: dict):
    body: dict = event["body"]
    body: dict = json.loads(body)
    logging.info(body)
    return body


def _query_dynamo_by_id(body: dict) -> dict:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["latencyTable"])
    response = table.query(
        KeyConditionExpression=Key('id').eq(body["bank_country_code"])
    )
    item = response["Items"][0]
    logging.info(json.dumps(item))
    # if item:
    #     body["verified"] = True

    # else:
    #     body["verified"] = False
    return body, item


def _create_response(body: dict) -> response:
    if body["approved"]:
        return {
            "status": 200,
            "content": json.dumps(body)
        }
    else:
        return {
            "status": 240,
            "content": json.dumps(body)
        }
