import csv
import boto3
import json
import logging
import requests
import time
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(json.dumps(event))
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    local_file_name = '/tmp/' + file_key
    s3_client.download_file(bucket_name, file_key, local_file_name)
    transactions = _read_source_csv_for_financial_transactions(local_file_name)
    sorted_transactions = _sort_by_amount(transactions)
    start_time = time.time()
    succesful_verifications = []
    for transaction in sorted_transactions:
        verified_transaction = _verify_transaction(transaction)
        if verified_transaction["verified"]:
            succesful_verifications.append(verified_transaction)


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


def _verify_transaction(transaction: dict) -> dict:
    response = requests.request(
        "GET", "https://a6z1z5aa46.execute-api.eu-west-1.amazonaws.com/verifyTransaction", data=json.dumps(transaction), timeout=60)
    logger.info(type(response.json()))
    return json.loads(transaction)
