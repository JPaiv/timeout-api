import os
import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(json.dumps(event))

    s3 = boto3.resource('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))

    content_object = s3.Object(bucket_name, file_key)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    logger.info(json.dumps(json_content))
    for key, value in json_content.items():
        latency_data = {}
        latency_data["id"] = key
        latency_data["latency"] = value
        logger.info(json.dumps(latency_data))
        _write_to_dynamo(latency_data)


def _write_to_dynamo(latency_data: dict):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["latencyTable"])
    table.put_item(Item=latency_data)
