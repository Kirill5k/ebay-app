from utils.logging import log
from keras.models import Sequential
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, Input, Dropout, LSTM
from keras.models import model_from_json


class Seq2SeqPredictor:
    def __init__(self, model):
        self.model = model
        self.__compile()
        log('Seq2SeqPredictor created')

    @staticmethod
    def new(word_embeddings, output_shape):
        log('creating new Seq2SeqPredictor model')
        model = Sequential()
        # model.add(Input(input_shape, dtype='int32'))
        model.add(word_embeddings.keras_embeddings_layer())
        model.add(LSTM(256))
        model.add(Dropout(0.5))
        model.add(RepeatVector(output_shape[0]))

        model.add(LSTM(256, return_sequences=True))
        model.add(Dropout(0.5))

        model.add(TimeDistributed(Dense(512)))
        model.add(Dropout(0.3))
        model.add(TimeDistributed(Dense(output_shape[1])))
        model.add(Activation('softmax'))

        return Seq2SeqPredictor(model)

    @staticmethod
    def from_file(model_file, weights_file):
        log(f'loading Seq2SeqPredictor model from {model_file} and weights from {weights_file}')
        with open(model_file, 'r') as model_file:
            model_json = model_file.read()
            model = model_from_json(model_json)
            model.load_weights(weights_file)
            return Seq2SeqPredictor(model)

    def __compile(self):
        log('compiling Seq2SeqPredictor model')
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def summary(self):
        self.model.summary()

    def train(self, X_train, y_train, epochs=50, batch_size=32, shuffle=True):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, shuffle=shuffle)

    def test(self, X_test, y_test):
        loss, acc = self.model.evaluate(X_test, y_test)
        log()
        log(f'test loss = {loss}')
        log(f'test accuracy = {acc}')

    def predict(self, X):
        return self.model.predict(X)

    def save(self, model_file, weights_file):
        log(f'saving model to file {model_file} and weights to file {weights_file}')
        model_json = self.model.to_json()
        with open(model_file, 'w') as file:
            file.write(model_json)
        self.model.save_weights(weights_file)