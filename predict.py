#importing necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
import numpy as np
import streamlit as st

#defining project title
st.title("Automatic Text Predictor")

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

#generating next words given a seed
def next_word(seed):
  seed_text = seed
  next_words = 1
  for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = model.predict_classes(token_list, verbose=0)
    output_word = ""
    for word, index in tokenizer.word_index.items():
      if index == predicted:
        output_word = word
        break
    seed_text += " " + output_word
  st.write(seed_text)

#getting the output/predicted text  
next_word(st.text_input('Enter seed sentence','I want to meet'))
