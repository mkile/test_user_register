import pytest
import requests

@pytest.fixture(scope="function")
def api():
    # Сгенерируем случайного пользователя
    user_name = random_username()
    if config.API_KEY == '':
        raise ValueError('Can not initalize fixture! API_KEY environment variable not set.')
    return config.MailsacApi(user_name, config.API_KEY)

@pytest.fixture(scope="function")
def prepaired_inbox_session(api):
    """"Фикстура для подготовки ящика, пользователя и API, а также освобождения ящика после теста"""
    # Получим доступ к ящику
    if requests.get(api.reserve_inbox, headers=api.headers).status_code != 200:
        raise ValueError(f'Selected mailbox {api.user_name} is owned by another account')
    # На всякий случай очистим почтовый ящик
    if requests.delete(api.process_messages, headers=api.request_headers) != 204:
        raise ValueError(f'Failed to clear mailbox {user_name}, returned code {result.status_code}')
    yield
    # На всякий случай очистим почтовый ящик
    print('deleted')
    requests.delete(api.process_messages, headers=api.request_headers)
    # Освободим почтовый ящик
    requests.delete(api.reserve_inbox, headers=api.headers).status_code
