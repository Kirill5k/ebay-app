from nlp.embeddings import WordEmbeddings
from nlp.Seq2SeqPredictor import Seq2SeqPredictor
from nlp.training import DataSet
from utils.logging import log
import pandas as pd
from config import Config


embeddings = WordEmbeddings.from_file(Config.get_filepath('word2vec'))

dataset = DataSet(embeddings, Config.get_filepath('train-data'), y_labels=['brand', 'model', 'year', 'memory', 'color', 'network'])
x_max_len, y_max_len, vocab_size = dataset.X_max_len, dataset.y_max_len, dataset.vocab_size
log(f'max len: {x_max_len}/{y_max_len}, labels count {vocab_size}')
X_train, X_test, y_train, y_test = dataset.get_train_test_data(test_size=0.1)

predictor = Seq2SeqPredictor.from_file(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
# predictor = Seq2SeqPredictor.new(embeddings, (y_max_len, vocab_size))
predictor.summary()
predictor.train(X_train, y_train, epochs=5)
predictor.save(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
predictor.test(X_test, y_test)


test = X_test[0:500]
expected = y_test[0:500]
results = predictor.predict(test)

for (inp, exp, res) in zip(test, expected, results):
    log(f'Input: {embeddings.indexes_to_sentence(inp)}')
    log(f'Result: {embeddings.ohs_to_sentence(res)}')
    log(f'Expected: {embeddings.ohs_to_sentence(exp)}')
    log()


