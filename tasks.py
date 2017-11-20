from extensions import db
from models import ProcessedTransaction
from mixer import process_transaction
from settings import JOBCOIN_TRANSACTIONS

import requests


def update_transactions():
    ''' Get all transactions and process them'''
    r = requests.get(JOBCOIN_TRANSACTIONS)
    transactions = r.json()

    for t in transactions:
        to_address = t['toAddress']
        from_address = t['fromAddress'] if 'fromAddress' in t else None
        amount = t['amount']
        timestamp = t['timestamp']

        process_transaction(to_address, from_address, amount, timestamp)


def make_payments():
    ''' Make payments to current creditors'''
    '''print(db.transaction_is_processed('a', 'b', 'c'))'''
    '''address = ''.join(random.choices(string.ascii_letters + string.digits, k=1))
    amount = '5'
    timestamp = 'a'
    pt = db.session.query( \
                        exists() \
                            .where( \
                                (ProcessedTransaction.address == address) \
                                & (ProcessedTransaction.amount == amount) \
                                & (ProcessedTransaction.timestamp == timestamp) \
                            ) \
                        ).scalar()

    print(pt)'''
    pass