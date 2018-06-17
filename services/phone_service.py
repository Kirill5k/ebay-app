from services.ebay_service import EbayService
from utils.logging import log_error


class PhoneService:
    ebay_service = EbayService()

    @classmethod
    def fetch_latest_phones(cls):
        phones = cls.ebay_service.get_latest_phones()
        for phone in phones:
            cls.__save(phone)

    @classmethod
    def __save(cls, phone):
        try:
            phone.save()
        except Exception as error:
            log_error(f'Unable to save phone: {error}')

