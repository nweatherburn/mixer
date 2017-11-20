from models import Creditor, CreditorDepositToPaymentAddress, ProcessedTransaction
from extensions import db
from settings import ADDRESS_LENGTH, MIXER_ADDRESS, JOBCOIN_ADDRESSES, JOBCOIN_TRANSACTIONS

import random
import requests
import string
import sqlite3
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError


def get_new_deposit_address():
    '''Creates a random string to act as a deposit address'''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=ADDRESS_LENGTH))


def create_new_deposit_address_for_addresses(addresses):
    '''
        Given a list of addresses 
        Assign these addresses to be the payment addresses for a creditor
        and return a deposit address for that creditor.
    '''
    deposit_address = get_new_deposit_address()
    for address in addresses:
        db.session.add(CreditorDepositToPaymentAddress( \
                            creditor_deposit_address=deposit_address, \
                            creditor_payment_address=address))

    try:
        db.session.commit()
    except IntegrityError:
        raise ValueError('Creditor Payment Address already in use.')

    return deposit_address


def transfer_funds(from_address, to_address, amount):
    '''
        Transfers amount from from_address to to_address.
    '''
    toSend = {
        'fromAddress' : from_address,
        'toAddress' : to_address,
        'amount' : str(amount)
    }
    r = requests.post(JOBCOIN_TRANSACTIONS, json=toSend)
    r.raise_for_status()


def transfer_to_mixer_account(from_address, amount):
    '''
        Transfers amount from from_address to the MIXER_ADDRESS.
    '''
    transfer_funds(from_address, MIXER_ADDRESS, amount)


def transfer_from_mixer_account(to_address, amount):
    '''
        Transfers amount from the MIXER_ADDRESS to to_address.
    '''
    transfer_funds(MIXER_ADDRESS, to_address, amount)


def is_new_transaction(transaction):
    ''' Returns whether this is the first time this transaction has been seen'''
    return not db.session.query( \
                    exists() \
                        .where( \
                            (ProcessedTransaction.to_address == transaction.to_address) \
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


def extract_fee(amount):
    ''' 
        Calculates the fee to apply to a given transaction amount.
        Returns the amount minus the fee.
    '''
    return amount  # We are a generous mixer


def process_new_transaction(transaction):
    ''' 
        Process a new transaction. 
        Adds the transaction to processed transactions.
        Increments the creditors credit amount (the amount we need to repay them)
    '''
    if is_mixers_address(transaction.to_address):
        transfer_to_mixer_account(transaction.to_address, transaction.amount)

        amount_post_fee = extract_fee(transaction.amount)
        creditor = Creditor.query.filter_by(creditor_deposit_address=transaction.to_address).first()
        if creditor:
            creditor.amount = creditor.amount + amount_post_fee
        else:
            creditor = Creditor(creditor_deposit_address=transaction.to_address, amount=transaction.amount)
            db.session.add(creditor)

    db.session.add(transaction)
    db.session.commit()


def process_transaction(to_address, from_address, amount, timestamp):
    transaction = ProcessedTransaction(to_address=to_address, from_address=from_address, amount=amount, timestamp=timestamp)

    if is_new_transaction(transaction):
        process_new_transaction(transaction)


def amount_to_pay(amount):
    '''
        Takes the amount owing to a creditor 
        and decides how much to pay them this payment round.
    '''
    if amount <= 1:
        return amount
    
    # Pay between 10% and 30% of the remaining balance.
    # Round payments to two decimal places.
    # Assuming there are 21million potential job coins 
    #  and a payment round happens every 30 seconds then this mixer will
    #  take at most 80 minutes to pay back.
    #  Definitely not a productionizable algorithm but it introduces enough
    #  randomness for this.
    
    payment_percent = round(random.uniform(0.1, 0.3), 2)
    to_pay = min(1, round(amount * payment_percent, 2))
    return to_pay



def repay_creditors():
    creditors = db.session.query(Creditor).all()
    for creditor in creditors:
        to_pay = amount_to_pay(creditor.amount)
        creditor.amount = creditor.amount - to_pay

        deposit_addresses = CreditorDepositToPaymentAddress.query.all()
        payment_address = random.choice(deposit_addresses).creditor_payment_address

        transfer_from_mixer_account(payment_address, to_pay)

    db.session.commit()

