from models import Creditor, CreditorDepositToPaymentAddress, ProcessedTransaction
from extensions import db
from settings import ADDRESS_LENGTH, MIXER_ADDRESS, JOBCOIN_ADDRESSES, JOBCOIN_TRANSACTIONS

import random
import requests
import string
from sqlalchemy.sql import exists


def get_new_deposit_address():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=ADDRESS_LENGTH))


def transfer_funds(from_address, to_address, amount):
    # TODO (nweatherburn): do transfer
    '''toSend = {
        'fromAddress' : from_address,
        'toAddress' : to_address,
        'amount' : str(amount)
    }
    r = requests.post(JOBCOIN_TRANSACTIONS, json=toSend)
    r.raise_for_status()'''
    print('\ntransfer_funds({fa}, {ta}, {a})'.format(fa=from_address, ta=to_address, a=amount))


def transfer_to_mixer_account(address, amount):
    transfer_funds(address, MIXER_ADDRESS, amount)


def is_new_transaction(transaction):
    ''' Returns whether this is the first time this transaction has been seen'''
    return not db.session.query( \
                    exists() \
                        .where( \
                            (ProcessedTransaction.from_address == transaction.to_address) \
                            & (ProcessedTransaction.from_address == transaction.from_address) \
                            & (ProcessedTransaction.amount == transaction.amount) \
                            & (ProcessedTransaction.timestamp == transaction.timestamp) \
                        ) \
                    ).scalar()


def is_mixers_address(address):
    ''' Returns whether the given address is owned by the mixer. '''
    return db.session.query(exists() \
                        .where(CreditorDepositToPaymentAddress.creditor_deposit_address == address) \
                    ).scalar()


def amount_post_fee(amount):
    ''' Calculates the fee to apply to a given transaction amount'''
    return amount  # We are a generous mixer


def process_new_transaction(transaction):
    ''' 
        Process a new transaction. 
        Adds the transaction to processed transactions.
        Increments the creditors credit amount (the amount we need to repay them)
    '''
    if is_mixers_address(transaction.to_address):
        transfer_to_mixer_account(transaction.to_address, transaction.amount)

        amount_post_fee = amount_post_fee(transaction.amount)
        creditor = db.session.query(Creditor.creditor_deposit_address == transaction.to_address)
        creditor.amount += transaction.amount_post_fee
    else:
        print('\n')
        print('process_new_transaction(transaction) false')
        print('to: ', transaction.to_address)
        print('from_address: ', transaction.from_address)
        print('amount: ', transaction.amount)
        print('timestamp: ', transaction.timestamp)

    db.session.add(transaction)
    db.session.commit()


def process_transaction(to_address, from_address, amount, timestamp):
    processed_transaction = ProcessedTransaction(to_address=to_address, from_address=from_address, amount=amount, timestamp=timestamp)

    if is_new_transaction(processed_transaction):
        process_new_transaction(processed_transaction)