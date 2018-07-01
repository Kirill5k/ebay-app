from services.ebay_service import EbayService
from services.notification_service import NotificationService
from services.cex_service import CexService
from utils.logging import Logger
from utils.cex_utils import average_cash_price
from domain.ebay import EbayPhone


class PhoneService:
    logger = Logger.of('PhoneService')

    PRICE_THRESHOLD = 0.9

    ebay_service = EbayService()
    cex_service = CexService()
    notification_service = NotificationService()

    @classmethod
    def fetch_latest_phones(cls):
        phones = cls.ebay_service.get_latest_phones()
        cls.logger.info(f'found {len(phones)} phones')
        for phone in phones:
            cls.check_price(phone)

    @classmethod
    def check_price(cls, ebay_phone: EbayPhone):
        cls.logger.info(f'{ebay_phone.title} (£{ebay_phone.price})')
        cls.logger.info(f' |--> {ebay_phone.formatted_title}')
        if ebay_phone.is_recognized and ebay_phone.has_trusted_seller:
            cex_phones = cls.cex_service.find_match(ebay_phone.formatted_title)
            cex_price = average_cash_price(cex_phones)
            if cex_price > 0 and cex_price * cls.PRICE_THRESHOLD >= ebay_phone.price:
                cls.notification_service.send_notification(ebay_phone, cex_price)

