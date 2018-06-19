from domain.cex import CexPhone, Price, Query


class CexPhoneMapper:
    @staticmethod
    def map(response: dict, query: str) -> CexPhone:
        name = response['boxName'].lower()
        condition = name[-1]
        price = CexPhoneMapper.__map_price(response)
        return CexPhone(name=name, price=price, query=Query(string=query), condition=condition)

    @staticmethod
    def __map_price(response: dict) -> Price:
        return Price(sell=response['sellPrice'], cash=response['cashPrice'], exchange=response['exchangePrice'])
