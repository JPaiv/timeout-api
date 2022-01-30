import os
import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(json.dumps(event))
    event = event["body"]
