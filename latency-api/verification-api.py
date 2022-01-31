import csv
import boto3
import json
import logging
import requests
import time
from typing import Union
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
        AWS Lambda handler to get events for verification.
    """
    logger.info(json.dumps(event))
    s3_client = boto3.client('s3')
    bucket_name, file_key = _get_bucket_and_file_names(event)
    logger.info('Reading {} from {}'.format(file_key, bucket_name))

    local_file_name = _create_local_file_location_and_name(file_key)
    s3_client.download_file(bucket_name, file_key, local_file_name)
    transactions = _read_source_csv_for_financial_transactions(local_file_name)

    sorted_transactions = _sort_by_amount(transactions)
    succesful_verifications = []
    for transaction in sorted_transactions:
        verified_transaction = _verify_transaction(transaction)
        if verified_transaction["verified"]:
            succesful_verifications.append(verified_transaction)


def _get_bucket_and_file_names(event: dict) -> Union(str, str):
    """
        Get bucket and file name from s3 trigger event to download transaction source data file.
    """
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    return bucket_name, file_key


def _create_local_file_location_and_name(file_key: str) -> str:
    """
        Lambda only accepts tmp file location for a file download.
    """
    return '/tmp/' + file_key


def _read_source_csv_for_financial_transactions(file_key) -> list:
    """
        Get financial transactions from a source file.
    """
    a = csv.DictReader(open(file_key),
                       delimiter=',')
    transactions = [x for x in a]
    return transactions


def _sort_by_amount(transactions: list) -> list:
    """
        Sort transactions by amount of dollars.
    """
    sorted_transactions = sorted(transactions,
                                 key=lambda transaction: transaction["amount"],
                                 reverse=True)
    return sorted_transactions


def _verify_transaction(transaction: dict, timeout: int) -> dict:
    """
        Verify transaction validity from an api with latency to stimulate actual production.
    """
    response = requests.request(
        "GET", "https://a6z1z5aa46.execute-api.eu-west-1.amazonaws.com/verifyTransaction", data=json.dumps(transaction), timeout=timeout)
    logger.info(type(response.json()))
    return json.loads(transaction)
