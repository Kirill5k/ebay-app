from clients.ebay.ebay_client import EbayClient
from nlp.Seq2SeqPredictor import Seq2SeqPredictor
from nlp.embeddings import WordEmbeddings
from config import Config
from utils.logging import log, log_error
from domain.ebay import EbayPhone
from domain.phone import PhoneDetails
from typing import List


class EbayService:
    client = EbayClient()
    predictor = Seq2SeqPredictor.from_file(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
    embeddings = WordEmbeddings.from_file(Config.get_filepath('word2vec'))

    @classmethod
    def get_latest_phones(cls) -> List[EbayPhone]:
        phones = cls.client.get_latest_phones()
        for phone in phones:
            cls.__update_details(phone)
            cls.__save(phone)
        return phones

    @classmethod
    def __update_details(cls, phone: EbayPhone):
        try:
            details = cls.__get_details(phone.title)
            phone.details = details
        except Exception as error:
            log_error(f'error processing phone "{phone.title}": {error}')
            phone.details = PhoneDetails()

    @classmethod
    def __get_details(cls, ebay_title: str) -> PhoneDetails:
        indexes = cls.embeddings.sentences_to_indices([ebay_title])
        prediction_ohs = cls.predictor.predict(indexes)[0]
        prediction = cls.embeddings.ohs_to_sentence(prediction_ohs)
        prediction = prediction.replace(' EMP', '')
        details = prediction.split(' - ')
        assert len(details) == 6, f'unexpected prediction outcome for {ebay_title}: {prediction}'
        return PhoneDetails(brand=details[0], model=details[1], memory=details[2], color=details[3], network=details[4], year=details[5])

    @classmethod
    def __save(cls, phone):
        try:
            phone.save()
        except Exception as error:
            log_error(f'unable to save phone: {error}')