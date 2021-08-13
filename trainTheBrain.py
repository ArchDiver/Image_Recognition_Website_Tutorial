import gc
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout
import tensorflow as tf
from tensorflow.keras import backend as K

TRAIN_DATA_DIR = 'train'
VALIDATION_DATA_DIR = 'validation'
NB_TRAIN_SAMPLES = 20
NB_VALIDATION_SAMPLES = 20
EPOCHS = 50
BATCH = 5

def build_model():
  if K.image_data_format() == 'channels_first':
    imput_shape = (3, IMG_WIDTH, IMG_HEIGHT)
  else:
    imput_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
  
  model = Sequential()
  model.add(Conv2D(32, (3,3), imput_shape=imput_shape))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))

  model.add(Conv2D(32, (3,3), imput_shape=imput_shape))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))

  model.add(Conv2D(64, (3,3), imput_shape=imput_shape))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))

  model.add(Flatten())
  model.add(Dense(64))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(1))
  model.add(Activation('sigmoid'))

  model.compile(loss = 'binary_crossentropy',
                  optimize='resprop',
                  metrics=['accuracy'])

def train_model():
  # This adds extra versions of the photos to improve the training
  train_datagen = ImageDataGenerator(
          rescale = 1 / 255,
          shear_range = 0.2,
  )


def main():
  myModel = none
  K.clear_session()
  gc.collect()
  myModel = build_Model()
  myModel = train_model(myModel)
  save_model(myModel)



main()