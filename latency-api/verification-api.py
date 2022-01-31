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
    sorted_transactions = _sort_by_amount(transactions)
    logger.info(json.dumps(sorted_transactions))


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


def _verify_transaction(transactiond: dict) -> dict:
    pass
