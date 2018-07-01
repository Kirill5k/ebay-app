from nlp.embeddings import WordEmbeddings
from nlp.Seq2SeqPredictor import Seq2SeqPredictor
from nlp.training import DataSet
from utils.logging import Logger
import pandas as pd
from config import Config

logger = Logger.of('TextProcessing')
embeddings = WordEmbeddings.from_file(Config.get_filepath('word2vec'))

dataset = DataSet(embeddings, Config.get_filepath('train-data'), y_labels=['brand', 'model', 'memory', 'color', 'network'])
x_max_len, y_max_len, vocab_size = dataset.X_max_len, dataset.y_max_len, dataset.vocab_size
logger.info(f'max len: {x_max_len}/{y_max_len}, labels count {vocab_size}')
X_train, X_test, y_train, y_test = dataset.get_train_test_data(test_size=0.1)

# predictor = Seq2SeqPredictor.from_file(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
predictor = Seq2SeqPredictor.new(embeddings, (y_max_len, vocab_size))
predictor.summary()
predictor.train(X_train, y_train, epochs=40)
predictor.save(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
predictor.test(X_test, y_test)


test = X_test[0:4000]
expected = y_test[0:4000]
results = predictor.predict(test)

for (inp, exp, res) in zip(test, expected, results):
    r = embeddings.ohs_to_sentence(res)
    e = embeddings.ohs_to_sentence(exp)
    if r != e or 'unknown' in r:
        logger.info(f'Input: {embeddings.indexes_to_sentence(inp)}')
        logger.info(f'Result: {r}')
        logger.info(f'Expected: {e}')
        logger.info()


