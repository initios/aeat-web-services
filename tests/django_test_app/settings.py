import os

'''Django test settings'''

INSTALLED_APPS = ['tests.django_test_app']

SECRET_KEY = 'testing.'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

AEAT_CERT_PATH = os.path.join(PROJECT_DIR, 'aduanet', 'tests', 'resources', 'certificate', 'cert.pem')  # NOQA
AEAT_KEY_PATH = os.path.join(PROJECT_DIR, 'aduanet', 'tests', 'resources', 'certificate', 'key.pem')  # NOQA
AEAT_VAT_NUMBER = 'X12345678'
AEAT_LEGAL_NAME = 'Test Legal Name'
AEAT_TEST_MODE = True
