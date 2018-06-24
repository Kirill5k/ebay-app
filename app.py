from time import sleep
from utils.logging import Logger
from services.phone_service import PhoneService

logger = Logger.of('MAIN')


def fetch_phone_listings():
    while True:
        PhoneService.fetch_latest_phones()
        logger.info()
        sleep(850)


fetch_phone_listings()