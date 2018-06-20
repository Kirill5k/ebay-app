from clients.webhooks.webhooks_client import WebhooksClient
from domain.ebay import EbayPhone


class NotificationService:
    webhooks_client = WebhooksClient()

    @classmethod
    def send_notification(cls, ebay_phone: EbayPhone, cex_price: str):
        title = f'{ebay_phone.title}<br>{ebay_phone.details}<br>'
        price = f'Ebay price: {ebay_phone.price} / Cex price: {cex_price}'
        url = ebay_phone.url
        cls.webhooks_client.send_notification(title, price, url)