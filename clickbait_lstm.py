# -*- coding: utf-8 -*-
"""clickBait-LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C43FeMzeGL3z7CBIVLHFW4oZyVgJif0C
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd drive/MyDrive/Colab\ Notebooks/clickBait

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, GlobalMaxPooling1D, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

def runPredict(testText, testLabels, tokenizer, maxlen, model):
  token_text = pad_sequences(tokenizer.texts_to_sequences(testText), maxlen=maxlen)
  preds = [round(i[0]) for i in model.predict(token_text)]
  cm = confusion_matrix(testLabels, preds)

  tn, fp, fn, tp = cm.ravel()

  precision = tp/(tp+fp)
  recall = tp/(tp+fn)
  print("Eval on test set")
  print("Recall of the model is {:.2f}".format(recall))
  print("Precision of the model is {:.2f}".format(precision))

def buildAndRun(text, labels, testText, testLabels, needPlot = False):
  text_train, text_test, y_train, y_test = train_test_split(text, labels)
  print(text_train.shape, text_test.shape, y_train.shape, y_test.shape)


  vocab_size = 5000
  maxlen = 500
  embedding_size = 32
  epochs = 20


  tokenizer = Tokenizer(num_words=vocab_size)
  tokenizer.fit_on_texts(text)

  X_train = tokenizer.texts_to_sequences(text_train)
  x_test = tokenizer.texts_to_sequences(text_test)

  X_train = pad_sequences(X_train, maxlen=maxlen)
  x_test = pad_sequences(x_test, maxlen=maxlen)


  model = Sequential()
  model.add(Embedding(vocab_size, embedding_size, input_length=maxlen))
  model.add(Bidirectional(LSTM(32, return_sequences=True), input_shape=(maxlen, 32)))
  model.add(GlobalMaxPooling1D())
  model.add(Dropout(0.2))
  model.add(Dense(1, activation='sigmoid'))
  model.summary()

  callbacks = [
      EarlyStopping(
          monitor='val_accuracy',
          min_delta=1e-4,
          patience=3,
          verbose=1
      ),
      ModelCheckpoint(
          filepath='weights.h5',
          monitor='val_accuracy', 
          mode='max', 
          save_best_only=True,
          save_weights_only=True,
          verbose=1
      )
  ]

  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  history = model.fit(X_train, y_train, batch_size=512, validation_data=(x_test, y_test), epochs=epochs, callbacks=callbacks)


  #model.load_weights('weights.h5')
  #model.save('model')


  if needPlot:
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training acc')
    plt.plot(x, val_acc, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()


  preds = [round(i[0]) for i in model.predict(x_test)]
  cm = confusion_matrix(y_test, preds)
  if needPlot:
    plt.figure()
    plot_confusion_matrix(cm, figsize=(12,8), hide_ticks=True, cmap=plt.cm.Blues)
    plt.xticks(range(2), ['Not clickbait', 'Clickbait'], fontsize=16)
    plt.yticks(range(2), ['Not clickbait', 'Clickbait'], fontsize=16)
    plt.show()


  tn, fp, fn, tp = cm.ravel()

  precision = tp/(tp+fp)
  recall = tp/(tp+fn)

  print("Recall of the model is {:.2f}".format(recall))
  print("Precision of the model is {:.2f}".format(precision))
  #Do prediction on another dataset
  runPredict(testText, testLabels, tokenizer, maxlen, model)

"""#Dataset"""

DATA1_PATH = 'clickbait_data.csv'
DATA2_ClickBait_PATH = 'clickbait.txt'
DATA2_Genuine_PATH = 'genuine.txt'

def readTxt(filePath):
  with open(filePath, "r") as f:
    sentence = []
    line = f.readline()
    while line:
      sentence.append(line.rstrip('\n'))      
      line = f.readline()
    
    return sentence

clickBait = readTxt(DATA2_ClickBait_PATH)
nonClickBait = readTxt(DATA2_Genuine_PATH)

data = pd.read_csv(DATA1_PATH)
data
dataA_text = data['headline'].values
dataA_labels = data['clickbait'].values

import copy 
labelA = [1] * len(clickBait)
labelB = [0] * len(nonClickBait)

datasetB_X = clickBait + nonClickBait
datasetB_Y = labelA + labelB

dataB_text = np.array(datasetB_X,dtype = object)
dataB_labels = np.array(datasetB_Y)

print(len(clickBait), len(nonClickBait), len(datasetB_X))

"""#Train on A and predict B"""

buildAndRun(dataA_text, dataA_labels, dataB_text, dataB_labels)

"""#Train on B and predict A"""

buildAndRun(dataB_text, dataB_labels, dataA_text, dataA_labels)

dataAB_text = np.concatenate((dataA_text, dataB_text))
dataAB_labels = np.concatenate((dataA_labels, dataB_labels))

"""#Train on A+B and predict B"""

buildAndRun(dataAB_text, dataAB_labels, dataB_text, dataB_labels)

"""#Train on A+B and predict A

"""

buildAndRun(dataAB_text, dataAB_labels, dataA_text, dataA_labels)

"""#Train on A+B and predict A+B

"""

buildAndRun(dataAB_text, dataAB_labels, dataAB_text, dataAB_labels)