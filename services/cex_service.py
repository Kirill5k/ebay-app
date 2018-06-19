from domain.phone import PhoneDetails
from domain.cex import CexPhone
from clients.cex.cex_client import CexClient
from typing import List
from utils.date_utils import Date


class CexService:
    client = CexClient()

    @classmethod
    def find_match(cls, details: PhoneDetails) -> List[CexPhone]:
        query = str(details)
        if 'unknown' not in query:
            phones = CexPhone.objects(query__string=query, query__date__gte=Date().minus_days(7).as_date()).all()
            return phones if len(phones) > 0 else cls.client.find_phone(query)
        else:
            return []
