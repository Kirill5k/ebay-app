import logging


class Logger:
    def __init__(self, logger):
        self.__logger = logger

    @classmethod
    def of(cls, name, debug=False):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG if debug is True else logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug is False else logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return Logger(logger)

    def info(self, message=''):
        self.__logger.info(f'> {message}')

    def error(self, error):
        self.__logger.error(f'> {error}')

    def debug(self, message):
        self.__logger.debug(f'> {message}')
