import os
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.utils import np_utils, plot_model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

def load_data(train, test):
  x_train = np.zeros((500, 100, 20))
  y_train = np.zeros((500,))
  
  x_test = np.zeros((100, 100, 20))
  y_test = np.zeros((100,))
  
  # x_train
  index = 0
  for root, dirs, files in os.walk(os.path.join(train, "text"), topdown=False):
    for file in files:
      x_train[index] = np.loadtxt(os.path.join(train, 'text', file), delimiter=',')
      index += 1
  
  # y_train
  index = 0
  for root, dirs, files in os.walk(os.path.join(train, "label"), topdown=False):
    for file in files:
      y_train[index, ] = open(os.path.join(train, 'label', file), 'r', encoding='utf-8').read()
      index += 1
  
  # x_test
  index = 0
  for root, dirs, files in os.walk(os.path.join(test, "text"), topdown=False):
    for file in files:
      x_test[index] = np.loadtxt(os.path.join(test, 'text', file), delimiter=',')
      index += 1
  
  # y_test
  index = 0
  for root, dirs, files in os.walk(os.path.join(test, "label"), topdown=False):
    for file in files:
      y_test[index, ] = open(os.path.join(test, 'label', file), 'r', encoding='utf-8').read()
      index += 1
  
  return (x_train, y_train), (x_test, y_test)

original_stdout = sys.stdout  

#Dataset
with open('model_result.txt', 'w') as f:
  sys.stdout = f 
  (X_train, Y_train), (X_test, Y_test) = load_data("train/", "test/")
  x_train = X_train.reshape(500, 1, 100, 20)/255
  x_test = X_test.reshape(100, 1, 100, 20)/255
  y_train = np_utils.to_categorical(Y_train)
  y_test = np_utils.to_categorical(Y_test)
  
  # Model Structure
  model = Sequential()
  model.add(Conv2D(filters=32, kernel_size=3, input_shape=(1, 100, 20), activation='relu', padding='same'))
  model.add(MaxPool2D(pool_size=2, data_format='channels_first'))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dense(6, activation='softmax'))
  print(model.summary())
  
  # Train
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  model.fit(x_train, y_train, epochs=10, batch_size=16, verbose=1)
  
  # Test
  loss, accuracy = model.evaluate(x_test, y_test)
  print('Test:')
  print('Loss: %s\nAccuracy: %s' % (loss, accuracy))
  
  # Save model
  model.save('./CNN_pssm.h5')
  
  # Load Model
  # model = load_model('./CNN_pssm.h5')
  sys.stdout = original_stdout 

# Display
def plot_img(n):
    plt.imshow(X_test[n], cmap='gray')
    plt.show()


def all_img_predict(model):
    print(model.summary())
    loss, accuracy = model.evaluate(x_test, y_test)
    print('Loss:', loss)
    print('Accuracy:', accuracy)
    predict = model.predict_classes(x_test)
    print(pd.crosstab(Y_test.reshape(-1), predict, rownames=['Label'], colnames=['predict']))


def one_img_predict(model, n):
    predict = model.predict_classes(x_test)
    print('Prediction:', predict[n])
    print('Answer:', Y_test[n])
    plot_img(n)
