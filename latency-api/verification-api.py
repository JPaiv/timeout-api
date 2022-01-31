import csv
import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(json.dumps(event))

    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))

    s3_client.download_file(bucket_name, file_key, file_key)
    transactions = _read_source_csv_for_financial_transactions(file_key)
    logger.info(json.dumps(transactions))


def _read_source_csv_for_financial_transactions(file_key) -> dict:
    """
        Get financial transactions from a source file.
    """
    a = csv.DictReader(open(file_key),
                       delimiter=',')
    transactions = [x for x in a]
    return transactions
