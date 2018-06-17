from time import sleep
from utils.logging import log
from services.phone_service import PhoneService


def fetch_phone_listings():
    while True:
        PhoneService.fetch_latest_phones()
        log()
        sleep(850)


fetch_phone_listings()