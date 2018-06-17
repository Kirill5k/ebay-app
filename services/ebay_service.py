from clients.ebay.ebay_client import EbayClient
from nlp.Seq2SeqPredictor import Seq2SeqPredictor
from nlp.embeddings import WordEmbeddings
from config import Config
from utils.logging import log, log_error
from domain.ebay import EbayPhone, PhoneDetails


class EbayService:
    ebay_client = EbayClient()
    predictor = Seq2SeqPredictor.from_file(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
    embeddings = WordEmbeddings.from_file(Config.get_filepath('word2vec'))

    @classmethod
    def get_latest_phones(cls):
        phones = cls.ebay_client.get_latest_phones()
        for phone in phones:
            cls.__update_details(phone)
        return phones

    @classmethod
    def __update_details(cls, phone: EbayPhone):
        try:
            details = cls.__get_details(phone.title)
            phone.details = details
            log(f'{phone.title} / {details}')
        except Exception as error:
            log_error(f'Error processing phone "{phone.title}": {error}')

    @classmethod
    def __get_details(cls, ebay_title: str) -> PhoneDetails:
        indexes = cls.embeddings.sentences_to_indices([ebay_title])
        prediction_ohs = cls.predictor.predict(indexes)[0]
        prediction = cls.embeddings.ohs_to_sentence(prediction_ohs)
        prediction = prediction.replace(' EMP', '')
        details = prediction.split(' - ')
        assert len(details) == 6, f'Unexpected prediction outcome: {prediction}'
        return PhoneDetails(brand=details[0], model=details[1], year=details[2], memory=details[3], color=details[4],network=details[5])
