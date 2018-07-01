from statistics import mean
from domain.cex import CexPhone
from typing import List


def average_cash_price(phones: List[CexPhone] = []):
    return mean(map(lambda phone: phone.price.cash, phones)) if len(phones) > 0 else 0
