import random
import string
import pytest
import config
import logging


logging.basicConfig(level=logging.INFO, filename="test.log",  format='[%(asctime)s] %(message)s')


@pytest.fixture(scope="function")
def api():
    logger = logging.getLogger('Testlogger')
    # Сгенерируем случайного пользователя
    symbol = string.ascii_letters
    user_name = config.PREFIX + "".join([random.choice(symbol) for i
                                         in range(random.randrange(config.MAX_NAME_LENGTH))])
    logger.info(f'Generated random user: {user_name}')
    if config.API_KEY == '':
        logger.error('Can not initialize fixture! API_KEY environment variable not set.')
        raise ValueError('Can not initialize fixture! API_KEY environment variable not set.')
    return config.MailsacApi(user_name, config.API_KEY)
