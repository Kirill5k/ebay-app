from time import sleep
from utils.logging import Logger
from services.phone_service import PhoneService


logger = Logger.of('MAIN')

if __name__ == '__main__':
    while True:
        PhoneService.fetch_latest_phones()
        logger.info()
        sleep(560)