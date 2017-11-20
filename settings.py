from urllib.parse import urljoin

ADDRESS_LENGTH = 10
MIXER_ADDRESS = 'mixer_address'


# Jobcoin Endpoints
_JOBCOIN_ROOT = 'http://jobcoin.gemini.com/tremble/api/'

JOBCOIN_ADDRESSES = urljoin(_JOBCOIN_ROOT, 'addresses/{addresses}')
JOBCOIN_TRANSACTIONS = urljoin(_JOBCOIN_ROOT, 'transactions')


class FlaskConfig(object):
    """Configuration."""
    DEBUG = False
    JOBS = [
        {
            'id': 'update_transactions',
            'func': 'tasks:update_transactions',
            'trigger': 'interval',
            'seconds': 5
        },
        {
            'id': 'make_payments',
            'func': 'tasks:make_payments',
            'trigger': 'interval',
            'seconds': 30
        }
    ]
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mixer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False