import logging


logger = logging.getLogger('ebay-app')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def log(message=''):
    logger.info(f'> {message}')


def log_error(error):
    logger.error(f'> {error}')