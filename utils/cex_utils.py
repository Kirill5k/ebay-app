from statistics import mean
from domain.cex import CexPhone


def average_cash_price(phones: CexPhone):
    return mean(map(lambda phone: phone.price.cash, phones)) if (len(phones)) > 0 else 0