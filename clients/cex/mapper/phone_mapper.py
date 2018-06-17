from domain.cex import CexPhone, Price, Query


class CexPhoneMapper:
    @staticmethod
    def map(response: dict, query: str) -> CexPhone:
        price = CexPhoneMapper.__map_price(response)
        return CexPhone(name=response['boxName'], price=price, query=Query(string=query))

    @staticmethod
    def __map_price(response: dict) -> Price:
        return Price(sell=response['sellPrice'], cash=response['cashPrice'], exchange=['exchangePrice'])