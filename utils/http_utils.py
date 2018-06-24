from utils.logging import Logger
from time import sleep


logger = Logger.of('Retry')


def retry(times=5, wait=10, default_response=None):
    def decorator(http_call):
        def wrapper(*original_args, **original_kwargs):
            for count in range(times):
                try:
                    return http_call(*original_args, **original_kwargs)
                except Exception as error:
                    logger.error(f'{error}, Retry {count+1}')
                    sleep(wait)
            return default_response if default_response is not None else {}
        return wrapper
    return decorator
