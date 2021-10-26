from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from tensorflow import nn
import pathlib


class STT:
    def __init__(self, model_path):
        self.AUTOTUNE = tf.data.AUTOTUNE
        self.model = load_model(model_path)

    def load_data(self, input):
        data_dir = pathlib.Path(input)
        filenames = tf.io.gfile.glob(str(data_dir + '/*/*'))
        return filenames

    def __get_spectrogram(self, waveform):
        zero_padding = tf.zeros([1600] - tf.shape(waveform, dtype=tf.float32))

        waveform = tf.cast(waveform, tf.float32)
        equal_length = tf.concat([waveform, zero_padding], 0)
        spectrogram = tf.signal.stft(
            equal_length, frame_length=255, frame_step=128)
        spectrogram = tf.abs(spectrogram)
        spectrogram = tf.expand_dims(spectrogram, -1)

        return spectrogram

    def __decode_audio(self, audio_binary):
        audio, _ = tf.audio.decode_wav(audio_binary)

        return tf.squeeze(audio, axis=-1)

    def __get_waveform(self, file_path):
        audio_binary = tf.io.read_file(file_path)
        waveform = self.__decode_audio(audio_binary)

        return waveform

    def preprocess_dataset(self, files):
        files_ds = tf.data.Dataset.from_tensor_slices(files)
        output_ds = files_ds.map(
            self.__get_waveform, num_parallel_calls=self.AUTOTUNE)
        output_ds = output_ds.map(
            self.__get_spectrogram, num_parallel_calls=self.AUTOTUNE
        )

        return output_ds

    def format_data(self, preprocessed_data):
        result = []
        for audio in preprocessed_data:
            result.append(audio.numpy())

        result = np.array(result)

        return result

    def predict(self, data):
        prediction = np.argmax(nn.softmax(self.model(data)), axis=1)

        return prediction
