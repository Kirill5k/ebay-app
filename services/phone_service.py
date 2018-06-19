from services.ebay_service import EbayService
from services.cex_service import CexService
from utils.logging import log_error, log
from domain.ebay import EbayPhone


class PhoneService:
    ebay_service = EbayService()
    cex_service = CexService()

    @classmethod
    def fetch_latest_phones(cls):
        phones = cls.ebay_service.get_latest_phones()
        log(f'found {len(phones)} phones')
        for phone in phones:
            cls.check_price(phone)

    @classmethod
    def check_price(cls, ebay_phone: EbayPhone):
        cex_phones = cls.cex_service.find_match(ebay_phone.details)
        if len(cex_phones) > 0:
            log(f'EBAY ORIGINAL ({ebay_phone.price}): {ebay_phone.title}')
            log(f'EBAY PREDICTED: {ebay_phone.details}')
            for cex_phone in cex_phones:
                log(f'CEX ({cex_phone.price.cash}): {cex_phone.name}')