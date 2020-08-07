#importing necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
import numpy as np

#dataset preprocessing
file = open("Goodwill.txt").read() #opeining the dataset and reading from it

tokenizer = Tokenizer() #tokenizing the dataset
data = file.lower().split("\n") #converting dataset to lowercase

#removing whitespaces from the dataset
corpus = []
for line in data:
    a = line.strip()
    corpus.append(a)

#generating tokens for each sentence in the data
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1
print(tokenizer.word_index)
print(total_words)

#creating labels for each sentence in dataset
input_sequences = []
for line in corpus:
	token_list = tokenizer.texts_to_sequences([line])[0]
	for i in range(1, len(token_list)):
		n_gram_sequence = token_list[:i+1]
		input_sequences.append(n_gram_sequence)

# pad sequences 
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# create predictors and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

#builiding the sequential model
model = Sequential([
                    Embedding(total_words, 100, input_length = max_sequence_len-1),
                    Bidirectional(LSTM(150)),
                    Dense(total_words, activation = 'softmax')
])

#compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#training the mdoel on the dataset
history = model.fit(xs, ys, epochs=30, verbose=1)

#save the model with weights in HDF5 format

model.save('textPredictorModel.h5')

