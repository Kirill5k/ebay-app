import requests
from utils.logging import log
from utils.http_utils import retry
from config import Config


class WebhooksClient:
    def __init__(self):
        self.key = Config.webhooks['key']
        self.event = Config.webhooks['event']

    @retry(times=5, wait=10)
    def send_notification(self, title, price, ebay_url):
        log('Sending event')
        log(title)
        log(price)
        log(ebay_url)
        url = f'https://maker.ifttt.com/trigger/{self.event}/with/key/{self.key}'
        payload = {'value1': title, 'value2': price, 'value3': ebay_url}
        requests.post(url=url, data=payload)
