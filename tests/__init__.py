import sys
import os
from .test_entry import *
from .test_assets import *
from .test_query import *
from .test_stack import *

sys.path.insert(0, os.path.abspath('..'))

logging.basicConfig(filename='reports.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)


def stack_keys():
    credentials = {
        'api_key': 'blt20962a819b57e233',
        'access_token': 'blt01638c90cc28fb6f',
        'environment': 'development',
        'environment_prod': 'production',
        'sync_api_key': 'blt477ba55f9a67bcdf',
        'sync_delivery__token': 'cs7731f03a2feef7713546fde5',
    }
    return credentials


def entry_keys():
    credentials = {
        'api_key': 'blt20962a819b57e233',
        'access_token': 'cs18efd90468f135a3a5eda3ba',
        'environment': 'production',
        'entry_uid': 'bltb0256a89e2225a39',
    }
    return credentials


def query_keys():
    credentials = {
        'api_key': 'blt20962a819b57e233',
        'access_token': 'blt01638c90cc28fb6f',
        'environment': 'production',
    }
    return credentials
