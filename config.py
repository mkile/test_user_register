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

API_KEY = os.environ.get('API_KEY', '')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASS', '12345678')


# Константы для сервиса Mailsac
class MailsacApi:
    email_service_domain = 'mailsac.com'
    prefix = 'https://'

    def __init__(self, user_name, api_key):
        self.user_name = user_name
        self.process_messages = f'{self.prefix}{self.email_service_domain}/api/' \
                                f'addresses/{user_name}@{self.email_service_domain}/messages'
        self.get_message = f'{self.prefix}{self.email_service_domain}/api/dirty/{user_name}@self.email_service_domain/'
        self.request_headers = {'Mailsac-Key': api_key, 'content-type': 'application/json'}
        # работает только с платной учеткой
        self.reserve_inbox = f'{self.prefix}{self.email_service_domain}/api/' \
                             f'addresses/{user_name}@{self.email_service_domain}'


# Константы для сервиса MAilinator недописаны, так как пока нет доступа
class MailinatorApi:
    email_service_domain = 'mailinator.com'
    request_headers = {'': API_KEY}
    get_messages = ''
    delete_messages = ''
    get_message = ''
