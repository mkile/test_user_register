import pytest
import settings
from requests import get, post
from time import sleep
from logging import getLogger


def report_error(logger, error_msg):
    logger.error(error_msg)
    raise ValueError(error_msg)


# Написано под сервис Mailsac, а Mailinator так и не подтвердил триальный доступ
@pytest.mark.parametrize('attempt', range(settings.TESTS_COUNT))
def test_user_register(attempt, api):
    """Тест регистрирует пользователя, проверяет наличие письма для подтверждения регистрации и подтверждает ее"""
    logger = getLogger('Testlogger')
    logger.info(f'*** Starting new test for user: {api.user_name}, test number {attempt} ***')
    register_data = {'user_login': api.user_name, 'user_email': f'{api.user_name}@{api.email_service_domain}',
                     'password': settings.DEFAULT_PASSWORD, 'count-send': '0', 'captcha-checked': '0',
                     'action': 'register', 'nonce': 'c431dbdf8f', 'agree': 'on'}
    logger.info(f'Sending registration request.')
    result = post(settings.REGISTER_LINK, headers=settings.REGISTER_HEADERS, data=register_data)
    if result.status_code != 200:
        report_error(logger, f'Registration Failure, for user name {api.user_name} return code {result.status_code}')
    logger.info(f'Registration successful.')
    # Если сервер ответил кодом 200, пытаемся получить по API с почтового сервера список сообщений
    logger.info(f'Attempting email check')
    for attempt in range(settings.RETRIES_COUNT):
        logger.info(f'Attempt {attempt} of {settings.RETRIES_COUNT}')
        logger.info(f'Waiting {settings.TIMEOUT} seconds...')
        sleep(settings.TIMEOUT)
        logger.info('Getting messages from server')
        result = api.get_messages()
        if result['status_code'] != 200:
            report_error(logger, f'Failed to retrieve messages for account {api.user_name}, '
                                 f'return code {result["status_code"]}')
        logger.info('Messages received successfully.')
        # Получим первую ссылку из первого сообщения в ящике
        if len(result['result']) > 0:
            if len(result['result'][0]['links']) > 0:
                url_from_email = result['result'][0]['links'][0]
                logger.info(f'Received confirmation link {url_from_email}')
                # Отправим запрос на подтверждение регистрации
                result = get(url=url_from_email)
                logger.info(f'Going to confirmation link...')
                assert result.status_code == 200
                return
            else:
                logger.warning(f'Could not get link. Message has {len(result.json()[0]["links"])}')
        else:
            logger.warning(f'Could not get Message. Inbox has {len(result.json())} messages')
    report_error(logger, f'No messages received for account {api.user_name} for {settings.RETRIES_COUNT} attempts.')
