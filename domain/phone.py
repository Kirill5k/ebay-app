from mongoengine import EmbeddedDocument, StringField


class PhoneDetails(EmbeddedDocument):
    brand = StringField(default='unknown')
    model = StringField(default='unknown')
    memory = StringField(default='unknown')
    network = StringField(default='unknown')
    color = StringField(default='unknown')
    year = StringField(default='unknown')

    def __str__(self):
        summary = f'{self.brand} {self.model} {self.memory} {self.year} {self.color} {self.network}'
        return summary.replace(' unknown', '').strip()