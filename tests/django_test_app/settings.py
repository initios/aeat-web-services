import os

'''Django test settings'''

INSTALLED_APPS = ['django_test_app']

SECRET_KEY = 'testing.'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

USE_TZ = True
TIME_ZONE = 'UTC'

TEST_CERT_PATH = os.path.join(PROJECT_DIR, 'aduanet', 'tests', 'resources', 'certificate', 'cert.pem')  # NOQA
TEST_KEY_PATH = os.path.join(PROJECT_DIR, 'aduanet', 'tests', 'resources', 'certificate', 'key.pem')  # NOQA

AEAT_CERT_PATH = os.environ.get('AEAT_CERT_PATH', TEST_CERT_PATH)
AEAT_KEY_PATH = os.environ.get('AEAT_KEY_PATH', TEST_KEY_PATH)
AEAT_VAT_NUMBER = os.environ.get('AEAT_VAT_NUMBER', 'X12345678')
AEAT_LEGAL_NAME = os.environ.get('AEAT_LEGAL_NAME', 'Test Legal Name')
AEAT_TEST_MODE = True
