from mongoengine import *
from datetime import datetime
from config import Config


connect(db=Config.mongo['db'], username=Config.mongo['username'], password=Config.mongo['password'], host=Config.mongo['host'])


class Seller(EmbeddedDocument):
    name = StringField()
    feedback_score = IntField()
    feedback_percentage = FloatField()


class PhoneDetails(EmbeddedDocument):
    brand = StringField(default='unknown')
    model = StringField(default='unknown')
    memory = StringField(default='unknown')
    network = StringField(default='unknown')
    color = StringField(default='unknown')
    year = StringField(default='unknown')

    def __str__(self):
        # Apple iPhone 8 Plus 64GB Space Grey, Unlocked B
        repr = f'{self.brand} {self.model} {self.memory} {self.year} {self.color} {self.network}'
        repr = repr.replace('unknown', '').strip()
        return repr if len(repr) > 0 else 'unknown/unrecognized'


class EbayPhone(Document):
    id = StringField(required=True, primary_key=True)
    title = StringField()
    price = FloatField()
    images = ListField(URLField())
    details = EmbeddedDocumentField(PhoneDetails)
    seller = EmbeddedDocumentField(Seller)
    condition = StringField()
    url = URLField(unique=True)
    date_posted = DateTimeField(default=datetime.utcnow)
    network = StringField()
    meta = {'collection': 'ebay-listings'}
