'''
    Nick Weatherburn
    Jobcoin - Gemini
    11/18/2017

    Models for ORM
'''

from sqlalchemy import Column, String
from extensions import db


class ProcessedTransaction(db.Model):
    '''
        Transactions that have already been processed and added to the Creditor table
    '''
    __tablename__ = 'processed_transactions'

    to_address = Column(String, primary_key=True)
    from_address = Column(String)
    amount = Column(String, primary_key=True)
    timestamp = Column(String, primary_key=True)


class Creditor(db.Model):
    '''
        The creditors table represents addresses that have paid money to the mixer.
    '''
    __tablename__ = 'creditors'

    creditor_deposit_address = Column(String, primary_key=True)
    amount = Column(String)


class CreditorDepositToPaymentAddress(db.Model):
    '''
        The creditor to payment addresses table acts as a join table.
        This table will join a creditor_deposit_address (i.e. the address the mixer owns that a creditor will pay into)
        to a creditor_payment_address (i.e. the address the mixer will repay the credited funds to)

        | creditor_deposit_address | creditor_payment_address |
        | a                        | b                        |
        | a                        | c                        |    
    '''
    __tablename__ = 'creditor_deposit_to_payment_addresses'
    creditor_deposit_address = Column(String)
    creditor_payment_address = Column(String, primary_key=True)

