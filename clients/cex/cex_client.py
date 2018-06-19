from utils.http_utils import retry
from clients.cex.mapper.phone_mapper import CexPhoneMapper
import requests


class CexClient:
    @retry(times=5, wait=10)
    def __search(self, query):
        url = f'https://wss2.cex.uk.webuy.io/v3/boxes/predictivesearch?'
        params = {'q': query}
        result = requests.get(url=url,params=params)
        response = result.json().get('response', {'akc': 'Failure'})
        assert response['ack'] == 'Success', 'Failed to make get request to CEX'
        data = response.get('data')
        return data.get('results', []) if data is not None else []

    def find_phone(self, query):
        results = self.__search(query)
        return list(map(lambda result: CexPhoneMapper.map(result, query), results))

