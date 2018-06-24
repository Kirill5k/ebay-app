from clients.webhooks.webhooks_client import WebhooksClient
from domain.ebay import EbayPhone
from utils.logging import Logger


class NotificationService:
    logger = Logger.of('NotificationService')
    webhooks_client = WebhooksClient()

    @classmethod
    def send_notification(cls, ebay_phone: EbayPhone, cex_price: str):
        title = f'{ebay_phone.title}<br>{ebay_phone.formatted_title}<br>'
        price = f'Ebay price: {ebay_phone.price} / Cex price: {cex_price}'
        url = ebay_phone.url
        cls.logger.info('Sending event')
        cls.logger.info(f'|--> {title}')
        cls.logger.info(f'|--> {price}')
        cls.logger.info(f'|--> {url}')
        cls.webhooks_client.send_notification(title, price, url)