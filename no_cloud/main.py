from __future__ import print_function
from pprint import pprint
import csv
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(max_latency):
    latency_data = _read_source_json_api_latency_data()
    financial_transactions = _read_source_csv_for_financial_transactions()

    transactions = _merge_source_file_data(financial_transactions,
                                           latency_data)
    transactions = _filter_by_latency(transactions, max_latency)
    transactions = _sort_by_amount(transactions)
    priority_transactions = _priority_transactions(transactions, max_latency)
    pprint(priority_transactions)
    amounts_sum = _sum_priority_transaction_values(priority_transactions)
    pprint(amounts_sum)


def _read_source_json_api_latency_data() -> dict:
    """
        Read json source data from root folder to get api altencies.
    """
    with open("/home/juho/timeout_api/no_cloud/api_latencies.json") as f_in:
        return json.load(f_in)


def _read_source_csv_for_financial_transactions() -> dict:
    """
        Get financial transactions from a source file.
    """
    a = csv.DictReader(open("/home/juho/timeout_api/no_cloud/transactions.csv"),
                       delimiter=',')
    transactions = [x for x in a]
    return transactions


def _merge_source_file_data(financial_transactions: list,
                            latency_data: dict) -> dict:
    """
        Add country api latency.
    """
    for transaction in financial_transactions:
        transaction.update(
            {"latency": latency_data[transaction["bank_country_code"]]})
    return financial_transactions


def _filter_by_latency(transactions: list, max_latency: int) -> list:
    transactions = [
        transaction for transaction in transactions
        if transaction["latency"] <= max_latency
    ]
    return transactions


def _sort_by_amount(transactions: list) -> list:
    """
        Sort transactions by amount of dollars.
    """
    sorted_transactions = sorted(transactions,
                                 key=lambda transaction: transaction["amount"],
                                 reverse=True)
    return sorted_transactions


def _priority_transactions(transactions: list, max_latency: int) -> list:
    priority_transactions = []
    suitable_indexes = []
    for index, transaction in enumerate(transactions):
        if sum(priority_transactions) + transaction["latency"] <= max_latency:
            priority_transactions.append(transaction["latency"])
            suitable_indexes.append(index)

    priority_transactions = [transactions[i] for i in suitable_indexes]
    return priority_transactions


def _sum_priority_transaction_values(priority_transactions) -> int:
    amounts = []
    for transaction in priority_transactions:
        amounts.append(float(transaction["amount"]))

    return sum(amounts)


if __name__ == "__main__":
    main(1000)
