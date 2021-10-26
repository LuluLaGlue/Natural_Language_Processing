from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from tensorflow import nn
import pathlib
import os

AUTOTUNE = tf.data.AUTOTUNE


def get_spectrogram(waveform):
    zero_padding = tf.zeros([16000] - tf.shape(waveform), dtype=tf.float32)

    waveform = tf.cast(waveform, tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)
    spectrogram = tf.signal.stft(equal_length,
                                 frame_length=255,
                                 frame_step=128)

    spectrogram = tf.abs(spectrogram)

    return spectrogram


def decode_audio(audio_binary):
    audio, _ = tf.audio.decode_wav(audio_binary)
    return tf.squeeze(audio, axis=-1)


def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2]


def get_waveform_and_label(file_path):
    label = get_label(file_path)
    audio_binary = tf.io.read_file(file_path)
    waveform = decode_audio(audio_binary)
    return waveform, label


def get_spectrogram_and_label_id(audio, label):
    spectrogram = get_spectrogram(audio)
    spectrogram = tf.expand_dims(spectrogram, -1)
    label_id = tf.argmax(label == commands)
    return spectrogram, label_id


def preprocess_dataset(files):
    files_ds = tf.data.Dataset.from_tensor_slices(files)
    output_ds = files_ds.map(get_waveform_and_label,
                             num_parallel_calls=AUTOTUNE)
    output_ds = output_ds.map(get_spectrogram_and_label_id,
                              num_parallel_calls=AUTOTUNE)
    return output_ds


data_dir = pathlib.Path('../data/mini_speech_commands')

commands = np.array(tf.io.gfile.listdir(str(data_dir)))
commands = commands[commands != 'README.md']

filenames = tf.io.gfile.glob(str(data_dir) + '/*/*')
filenames = tf.random.shuffle(filenames)
model = load_model("STT/Models/model_1")

for index, v in enumerate([0, 1, 2, 3, 4, 5]):
    test_audio = []
    test_labels = []
    test_files = [filenames[index]]
    # print(tf.strings.split(filenames[index], "/")[2])
    test_ds = preprocess_dataset(test_files)

    for audio, label in test_ds:
        test_audio.append(audio.numpy())
        test_labels.append(label.numpy())

    test_audio = np.array(test_audio)
    test_labels = np.array(test_labels)

    y_pred_1 = np.argmax(nn.softmax(model.predict(test_audio)), axis=1)

    print("pred: {} = {}".format(y_pred_1[0], commands[y_pred_1[0]]))
    print("label: {} = {}".format(test_labels[0], commands[test_labels[0]]))
