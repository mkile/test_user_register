import pytest
import config
import requests
import time
import logging


# Написано под сервис Mailsac, а Mailinator так и не подтвердил триальный доступ
@pytest.mark.parametrize('attempt', range(config.TESTS_COUNT))
def test_user_register(attempt, api):
    """Тест регистрирует пользователя, проверяет наличие письма для подтверждения регистрации и подтверждает ее"""
    logger = logging.getLogger('Testlogger')
    logger.info(f'*** Starting new test for user: {api.user_name}, test number {attempt} ***')
    register_data = {'user_login': api.user_name, 'user_email': f'{api.user_name}@{api.email_service_domain}',
                     'password': config.DEFAULT_PASSWORD, 'count-send': '0', 'captcha-checked': '0',
                     'action': 'register', 'nonce': 'c431dbdf8f', 'agree': 'on'}
    logger.info(f'Sending registration request.')
    result = requests.post(config.REGISTER_LINK, headers=config.REGISTER_HEADERS, data=register_data)
    if result.status_code == 200:
        logger.info(f'Registration successful.')
        # Если сервер ответил кодом 200, пытаемся получить по API с почтового сервера список сообщений
        logger.info(f'Attempting email check')
        for attempt in range(config.RETRIES_COUNT):
            logger.info(f'Attempt {attempt} of {config.RETRIES_COUNT}')
            logger.info(f'Waiting {config.TIMEOUT} seconds...')
            time.sleep(config.TIMEOUT)
            logger.info('Getting messages from server')
            result = requests.get(api.process_messages, headers=api.request_headers)
            if result.status_code == 200:
                logger.info('Request successful.')
                # Получим первую ссылку из первого сообщения в ящике
                if len(result.json()) > 0:
                    if len(result.json()[0]['links']) > 0:
                        url_from_email = result.json()[0]['links'][0]
                        logger.info(f'Recieved confirmation link {url_from_email}')
                        # Отправим запрос на подтверждение регистрации
                        result = requests.get(url=url_from_email)
                        logger.info(f'Going to confirmation link...')
                        assert result.status_code == 200
                        return
                    else:
                        logger.warning(f'Could not get link. Message has {len(result.json()[0]["links"])}')
                else:
                    logger.warning(f'Could not get Message. Inbox has {len(result.json())} messages')
            else:
                raise ValueError(f'Failed to retrieve messages for account {api.user_name}, '
                                 f'return code {result.status_code}')
    else:
        raise ValueError(f'Registration Failure, for user name {api.user_name} return code {result.status_code}')
