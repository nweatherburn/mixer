from extensions import db
from models import ProcessedTransaction
from mixer import process_transaction, repay_creditors
from settings import JOBCOIN_TRANSACTIONS

from decimal import Decimal
import requests


def update_transactions():
    ''' Get all transactions and processes them'''
    r = requests.get(JOBCOIN_TRANSACTIONS)
    transactions = r.json()
    for t in transactions:
        to_address = t['toAddress']
        from_address = t['fromAddress'] if 'fromAddress' in t else None
        timestamp = t['timestamp']
        amount = t['amount']

        process_transaction(to_address, from_address, amount, timestamp)


def make_payments():
    ''' Make payments to current creditors'''
    repay_creditors()

