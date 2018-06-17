from domain.ebay import EbayPhone, Seller


class EbayPhoneMapper:
    @staticmethod
    def map(response):
        id = response['itemId']
        title = response.get('title', '').lower().replace('*', ' ').replace('/', ' ').replace('+', ' plus ')
        price = float(response.get('price', {}).get('convertedFromValue', 0))
        seller = EbayPhoneMapper.__map_seller(response)
        condition = response['condition']
        url = EbayPhoneMapper.__map_url(response)
        images = EbayPhoneMapper.__map_images(response)
        return EbayPhone(id=id, title=title, price=price, images=images, seller=seller, condition=condition, url=url)

    @staticmethod
    def __map_seller(response):
        seller = response['seller']
        return Seller(name=seller['username'], feedback_score=seller['feedbackScore'], feedback_percentage=float(seller['feedbackPercentage']))

    @staticmethod
    def __map_url(response):
        url = response['itemWebUrl']
        return url.replace(".com/",".co.uk/")

    @staticmethod
    def __map_images(response):
        return [image['imageUrl'] for image in response.get('additionalImages', [])]