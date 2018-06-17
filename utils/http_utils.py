from utils.logging import log_error, log
from time import sleep


def retry(times=5, wait=10):
    def decorator(http_call):
        def wrapper(*original_args, **original_kwargs):
            for count in range(times):
                try:
                    return http_call(*original_args, **original_kwargs)
                except Exception as error:
                    log_error(f'{error}, Retry {count+1}')
                    sleep(wait)
        return wrapper
    return decorator
