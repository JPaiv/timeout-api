import csv
import boto3
import json
import logging
import requests
import datetime
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
        AWS Lambda handler to get events for verification.
    """
    logger.info(json.dumps(event))
    s3_client = boto3.client('s3')
    bucket_name, file_key = _get_bucket_and_file_names(event)
    logger.info(f'Reading {file_key} from {bucket_name}')

    local_file_name = _create_local_file_location_and_name(file_key)
    s3_client.download_file(bucket_name, file_key, local_file_name)
    transactions = _read_source_csv_for_financial_transactions(local_file_name)

    sorted_transactions = _sort_by_amount(transactions)
    succesful_verifications = []
    start_time = datetime.datetime.now()
    for index, transaction in enumerate(sorted_transactions):
        verified_transaction = _verify_transaction(transaction)
        logger.info("Verified transaction:")
        logger.info(verified_transaction)
        content = verified_transaction["content"]
        content = json.loads(content)
        if content["verified"] == "true":
            succesful_verifications.append(content)
            del sorted_transactions[index]

        time_check = datetime.datetime.now()
        time_difference = start_time - time_check
        if time_difference.microseconds >= 1000:
            sorted_transactions = sorted_transactions[:5]
            break

    _send_unused_entries_to_sqs(transactions)(sorted_transactions)

    logging.info(succesful_verifications)


def _get_bucket_and_file_names(event: dict):
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


def _verify_transaction(transaction: dict) -> dict:
    """
        Verify transaction validity from an api with latency to stimulate actual production.
    """
    response = requests.get(
        url="https://8xq34nc1h9.execute-api.eu-west-1.amazonaws.com/verifyTransaction", params=transaction)
    logger.info(response.json())
    response = response.content
    response = json.loads(response)
    return response


def _send_unused_entries_to_sqs(transactions):
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(
        QueueName=os.environ("timeoutTransactionsQueue"))
    response = queue.send_messages(Entries=transactions)
    logger.info(response)
