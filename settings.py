import os

TIMEOUT = 1
RETRIES_COUNT = 5
MAX_NAME_LENGTH = 10
PREFIX = 'user_'
TESTS_COUNT = 1
REGISTER_LINK = 'https://stavkinasport.com/wp-admin/admin-ajax.php'
REGISTER_HEADERS = {
    'cache-control': "no-cache, must-revalidate, max-age=0",
    'access-control-allow-credentials': 'true'
}

API_KEY = os.environ.get('API_KEY', '12345678')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASS', '12345678')
