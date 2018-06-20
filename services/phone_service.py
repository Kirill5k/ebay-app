from services.ebay_service import EbayService
from services.notification_service import NotificationService
from services.cex_service import CexService
from utils.logging import log_error, log
from utils.cex_utils import average_cash_price
from domain.ebay import EbayPhone


class PhoneService:
    ebay_service = EbayService()
    cex_service = CexService()
    notification_service = NotificationService()

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
            cex_price = average_cash_price(cex_phones)
            if cex_price >= ebay_phone.price:
                cls.notification_service.send_notification(ebay_phone, cex_price)
