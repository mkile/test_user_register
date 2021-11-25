import random
import string
import pytest
from config import MAX_NAME_LENGTH


@pytest.fixture
def random_username(prefix, max_length):
    symbol = string.ascii_letters
    return prefix + "".join([random.choice(symbol) for i in range(random.randrange(maxlen))])
