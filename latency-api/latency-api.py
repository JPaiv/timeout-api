from urllib import response
import boto3
import json
import logging
import os
import time
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
    queryStringParameters = event["queryStringParameters"]
    logging.info(queryStringParameters)
    return queryStringParameters


def _query_dynamo_by_id(body: dict) -> dict:
    """
        Query DynamoDb table by id and parse the result.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["latencyTable"])
    query_response = table.query(
        KeyConditionExpression=Key('id').eq(body["bank_country_code"])
    )
    logger.info(response)
    item_retrieved_from_db = _get_result_from_dynamo_query(query_response)
    item_retrieved_from_db = _convert_decimal_to_int(item_retrieved_from_db)
    logging.info(item_retrieved_from_db)
    if item_retrieved_from_db:
        body["verified"] = "true"
        time.sleep(item_retrieved_from_db["latency"])
    else:
        body["verified"] = "false"
    return body


def _get_result_from_dynamo_query(response: dict) -> dict:
    """
        Dynamo returns list of db items in the table. Query returns only 1 items to take the first item from the list.
    """
    item_retrieved_from_db = response["Items"]
    item_retrieved_from_db = item_retrieved_from_db[0]
    return item_retrieved_from_db


def _convert_decimal_to_int(item_retrieved_from_db: dict) -> dict:
    """
        Dynamo returns int as decimal: change it back to int.
    """
    item_retrieved_from_db = dict(map(lambda x: (x[0], int(x[1])) if isinstance(
        x[1], Decimal) else x, item_retrieved_from_db.items()))

    return item_retrieved_from_db


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
