from utils.http_utils import retry
from utils.logging import Logger
from clients.cex.mapper.phone_mapper import CexPhoneMapper
import requests


class CexClient:
    logger = Logger.of('CexClient')

    @retry(times=5, wait=10, default_response=[])
    def __search(self, query):
        url = f'https://wss2.cex.uk.webuy.io/v3/boxes/predictivesearch?'
        params = {'q': query}
        result = requests.get(url=url,params=params)
        response = result.json().get('response', {'akc': 'Failure'})
        assert response['ack'] == 'Success', 'Failed to make get request to CEX'
        self.logger.debug(f'cex response: {response}')
        data = response.get('data')
        results = data.get('results', []) if data is not None else []
        return results if results is not None else []

    def find_phone(self, query):
        self.logger.debug(f'cex query: {query}')
        results = self.__search(query)
        return list(map(lambda result: CexPhoneMapper.map(result, query), results))

