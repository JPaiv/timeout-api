import os
import boto3
import json
import logging
import os

# Initialize you log configuration using the base class
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(json.dumps(event))

    s3 = boto3.resource('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    # s3.get_object(Bucket=bucket_name, Key=file_key)
    s3.Bucket(bucket_name).download_file(
        file_key, "latencies.json")
    with open("latencies.json") as source_file:
        source_file = json.loads(source_file)
        for key, value in source_file.items():
            latency_data = {}
            latency_data["id"] = key
            latency_data["latency"] = value
            _write_to_dynamo(latency_data)


# def _create_dynamo_latency_object(source_data: dict) -> dict:
#     latency_data = {}
#     for key, value in source_data.items():
#         latency_data["id"] = key
#         latency_data["latency"] = value
#     return latency_data


def _write_to_dynamo(latency_data: dict):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName=os.environ["latencyTable"], Item=latency_data)
