from multiprocessing.connection import wait
import os
from urllib import response
import boto3
import json
import logging
import os
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from requests.models import Response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: dict, context: dict) -> Response:
    logger.info(json.dumps(event))
    body: dict = _get_body_from_event(event)
    logger.info(json.dumps(body))
    body = _query_dynamo_by_id(body)
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
    logger.info(response)
    item_retrieved_from_db = response["Items"][0]
    item_retrieved_from_db = dict(map(lambda x: (x[0], int(x[1])) if isinstance(
        x[1], Decimal) else x, item_retrieved_from_db.items()))
    logging.info(item_retrieved_from_db)
    if item_retrieved_from_db:
        body["verified"] = True
        wait(int(item_retrieved_from_db["latency"]))
    else:
        body["verified"] = False
    return body


def _create_response(body: dict) -> response:
    if body["verified"]:
        return {
            "status": 200,
            "content": json.dumps(body)
        }
    else:
        return {
            "status": 404,
            "content": json.dumps(body)
        }
