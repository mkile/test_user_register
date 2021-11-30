from requests import get, post


# Api для сервиса Mailsac
class MailsacApi:
    email_service_domain = 'mailsac.com'
    prefix = 'https://'

    def __init__(self, user_name: str, api_key: str):
        self.user_name = user_name
        self.request_headers = {'Mailsac-Key': api_key, 'content-type': 'application/json'}
        self.process_messages = f'{self.prefix}{self.email_service_domain}/api/' \
                                f'addresses/{user_name}@{self.email_service_domain}/messages'
        self.get_message = f'{self.prefix}{self.email_service_domain}/api/dirty/{user_name}@{self.email_service_domain}/'
        # работает только с платной учеткой
        self.reserve_inbox = f'{self.prefix}{self.email_service_domain}/api/' \
                             f'addresses/{user_name}@{self.email_service_domain}'

    def reserve_inbox(self):
        result = get(url=self.reserve_inbox, headers=self.request_headers)
        return {'status_code': result.status_code, 'description': result.text}

    def get_messages(self):
        result = get(url=self.process_messages, headers=self.request_headers)
        if result.status_code != 200:
            return {'status_code': result.status_code, 'description': result.text}
        return {'status_code': result.status_code, 'description': result.text, 'result': result.json()}

    def get_message(self, message_id: str):
        result = get(url=self.get_message + str(message_id), headers=self.request_headers)
        if result.status_code != 200:
            return {'status_code': result.status_code, 'description': result.text}
        return {'status_code': result.status_code, 'description': result.text, 'result': result.json()}

    def __repr__(self):
        return f'MailsacAPI for user:"{self.user_name}"'


# Константы для сервиса MAilinator недописаны, так как пока нет доступа
class MailinatorApi:
    email_service_domain = 'mailinator.com'
    # request_headers = {'': API_KEY}
    get_messages = ''
    delete_messages = ''
    get_message = ''
