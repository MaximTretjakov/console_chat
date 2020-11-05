import sys
import logging
import traceback

import logs.server_log_config
import logs.client_log_config
import inspect
import datetime

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server_logger')
else:
    LOGGER = logging.getLogger('client_logger')


def log(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        LOGGER.debug(
            f'<{datetime.datetime.now():%Y-%m-%d %H:%M:%S}> '
            f'Функция {func.__name__}() '
            f'вызвана из функции {inspect.stack()[1][3]}.'
        )
        return ret
    return wrapper
