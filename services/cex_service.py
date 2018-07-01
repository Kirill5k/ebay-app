from domain.phone import PhoneDetails
from domain.cex import CexPhone
from clients.cex.cex_client import CexClient
from typing import List
from utils.date import Date
from utils.common import for_each
from utils.logging import Logger


class CexService:
    logger = Logger.of('CexService')
    client = CexClient()

    @classmethod
    def find_match(cls, query: str) -> List[CexPhone]:
        phones = cls.__query_db(query)
        return phones if len(phones) > 0 else cls.__query_client(query)

    @classmethod
    def __query_db(cls, query):
        return CexPhone.objects(query__string=query, query__date__gte=Date().minus_days(7).as_date()).all()

    @classmethod
    def __query_client(cls, query):
        phones = cls.client.find_phone(query)
        for_each(cls.__save, phones)
        return phones

    @classmethod
    def __save(cls, phone):
        try:
            phone.save()
        except Exception as error:
            cls.logger.error(f'unable to save: {error}')
