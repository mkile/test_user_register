import pytest
import mailapi
import settings

from string import ascii_letters
from random import choice, randrange
from logging import basicConfig, getLogger, INFO


basicConfig(level=INFO, filename="test.log",  format='[%(asctime)s] %(message)s')


@pytest.fixture(scope="function")
def api():
    logger = getLogger('Testlogger')
    # Сгенерируем случайного пользователя
    symbol = ascii_letters
    user_name = settings.PREFIX + "".join([choice(symbol) for i in range(randrange(settings.MAX_NAME_LENGTH))])
    logger.info(f'Generated random user: {user_name}')
    if settings.API_KEY == '':
        logger.error('Can not initialize fixture! API_KEY environment variable not set.')
        raise ValueError('Can not initialize fixture! API_KEY environment variable not set.')
    return mailapi.MailsacApi(user_name, settings.API_KEY)
