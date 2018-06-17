from utils.http_utils import retry
from clients.cex.mapper.phone_mapper import CexPhoneMapper
import requests


class CexClient:
    @retry(times=5, wait=10)
    def __search(self, query) -> dict:
        url = f'https://wss2.cex.uk.webuy.io/v3/boxes/predictivesearch?'
        params = {'q': query}
        result = requests.get(url=url,params=params)
        response = result.json().get('response', {'akc': 'Failure'})
        assert response['ack'] == 'Success', 'Failed to make get request to CEX'
        return response.get('data', {}).get('results', [])

    def find_phone(self, query):
        results = self.__search(query)
        return list(map(lambda result: CexPhoneMapper.map(result, query), results))

