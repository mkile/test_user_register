import pytest
import config
import requests
import time


@pytest.mark.parametrize("user_data", config.USERS_DATA)
def test_user_register(user_data):
    register_data = {'username': user_data['name'], 'password': user_data['password'], 'email': user_data['email']}
    result = requests.post(config.REGISTER_LINK, headers=config.REGISTER_HEADERS, data=register_data)
    if result.status_code == 200:
        for attempt in range(config.RETRIES_COUNT):
            time.sleep(config.TIMEOUT)
            result = requests.get(config.EMAIL_URL)
            if result.status_code == 200:
                # Обработка ответа зависит от реализации способа получения почты...
                # Обработка полученного списка писем, получение ссылки из текста письма
                url_from_email = ''
                result = requests.get(url=url_from_email)
                assert result.status_code == 200
    else:
        raise ValueError('Registration Failure, return code not 200')
