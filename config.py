import configparser
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class Config:
    config = configparser.ConfigParser()
    config.read(os.path.join(PROJECT_ROOT, 'config.ini'))
    mongo = config['mongo']
    ebay = config['ebay']

    @classmethod
    def get_filepath(cls, file):
        return os.path.join(PROJECT_ROOT, 'data', cls.config['files'][file])