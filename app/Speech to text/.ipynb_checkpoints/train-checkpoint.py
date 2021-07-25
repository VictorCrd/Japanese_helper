from constants import *
import joblib
from keras.optimizers import Adam
from model.tacotron_model import get_tacotron_model

import os
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"]="true"

import tensorflow as tf
print(tf.version.VERSION)
gpus = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)
#tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)

# import prepared data
decoder_input_training = joblib.load('data/decoder_input_training.pkl')
mel_spectro_training = joblib.load('data/mel_spectro_training.pkl')
spectro_training = joblib.load('data/spectro_training.pkl')

text_input_training = joblib.load('data/text_input_ml_training.pkl')
vocabulary = joblib.load('data/vocabulary.pkl')

model = get_tacotron_model(N_MEL, r, K1, K2, NB_CHARS_MAX,
                           EMBEDDING_SIZE, MAX_MEL_TIME_LENGTH,
                           MAX_MAG_TIME_LENGTH, N_FFT,
                           vocabulary)

opt = Adam()
model.compile(optimizer=opt,
              loss=['mean_absolute_error', 'mean_absolute_error'])

train_history = model.fit([text_input_training, decoder_input_training],
                          [mel_spectro_training, spectro_training],
                          epochs=NB_EPOCHS, batch_size=BATCH_SIZE,
                          verbose=1, validation_split=0.15)


joblib.dump(train_history.history, 'results/training_history.pkl')
model.save('results/model.h5')