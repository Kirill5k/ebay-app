import requests
from requests.auth import HTTPBasicAuth
from utils.date_utils import Date
from clients.ebay.domain.token import AccessToken
from clients.ebay.mapper.phone_mapper import EbayPhoneMapper
from utils.logging import log
from utils.http_utils import retry
from config import Config


class EbayClient:
    client_id: str
    client_secret: str
    access_token: AccessToken = None

    def __init__(self):
        self.client_id = Config.ebay['client_id']
        self.client_secret = Config.ebay['client_secret']

    @retry(times=5, wait=10)
    def __get_access_token(self) -> dict:
        url = 'https://api.ebay.com/identity/v1/oauth2/token'
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'client_credentials', 'scope': 'https://api.ebay.com/oauth/api_scope'}
        response = requests.post(url=url, auth=auth, headers=headers, data=payload)
        return response.json()['access_token']

    def __update_token(self) -> None:
        if self.access_token is None or self.access_token.is_expired():
            log('updating token')
            token = self.__get_access_token()
            self.access_token = AccessToken(token)

    @retry(times=5, wait=10)
    def __search(self, query, start_time) -> dict:
        filters = 'conditionIds:{1000|1500|2000|2500|3000|4000|5000}'
        filters += ',buyingOptions:{FIXED_PRICE}'
        filters += ',deliveryCountry:GB'
        filters += ',itemStartDate:[{}]'.format(start_time)
        filters += ',price:[10..350]'
        filters += ',priceCurrency:GBP'
        filters += ',itemLocationCountry:GB'

        url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
        headers = {
            'authorization': f'Bearer {self.access_token.token}',
            'x-ebay-c-marketplace-id': 'EBAY_GB'
        }
        params = {'q': query, 'category_ids': '9355', 'filter': filters}

        result = requests.get(url=url, params=params, headers=headers)
        return result.json().get('itemSummaries', [])

    def get_latest_phones(self, minutes=15) -> list:
        self.__update_token()
        phones = self.__search(query='phone', start_time=Date().minus_minutes(minutes).as_iso())
        return list(map(EbayPhoneMapper.map, phones))