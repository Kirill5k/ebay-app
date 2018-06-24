from utils.logging import Logger
from keras.models import Model
from keras.layers import Dense, Input, Dropout, LSTM, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.initializers import glorot_uniform


class ModelPredictor:
    logger = Logger.of('ModelPredictor')

    def __init__(self, w2v_model, input_shape=(30,), output_size=4367):
        embeddings_layer = self.__embeddings_layer(w2v_model)
        self.model = self.__build_model(input_shape, embeddings_layer, output_size)

    @staticmethod
    def __build_model(input_shape, embeddings_layer, output_size):
        sentence_indices = Input(input_shape, dtype='int32')
        model = embeddings_layer(sentence_indices)
        model = LSTM(256, return_sequences=True)(model)
        model = Dropout(0.5)(model)
        model = LSTM(256, return_sequences=False)(model)
        model = Dropout(0.5)(model)
        model = Dense(512)(model)
        model = Dropout(0.3)(model)
        model = Dense(output_size)(model)
        model = Activation('softmax')(model)
        model = Model(inputs=sentence_indices, outputs=model)
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    @staticmethod
    def __embeddings_layer(w2v_model):
        # vocab_len = len(w2v_model.wv.vocab)
        # emb_dim = w2v_model.wv.vector_size
        # emb_matrix = w2v_model.wv.syn0
        # embedding_layer = Embedding(vocab_len, emb_dim, trainable=False)
        # embedding_layer.build((None,))
        # embedding_layer.set_weights([emb_matrix])
        # return embedding_layer
        return w2v_model.wv.get_keras_embedding()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs = 2000, batch_size = 32, shuffle=True)

    def test(self, X_test, y_test):
        loss, acc = self.model.evaluate(X_test, y_test)
        self.logger.info()
        self.logger.info(f'Test loss = {loss}')
        self.logger.info(f'Test accuracy = {acc}')