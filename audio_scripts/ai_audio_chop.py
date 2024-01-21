import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import csv


# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/hub/tutorials/yamnet.ipynb#scrollTo=VX8Vzs6EpwMo
class AudioProcessor:
    def __init__(self, directory):
        self.directory = directory
        self.yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

    def process_audio_file(self, file_path):
        # ffmpeg wrapper, here we just read audio
        audio = AudioSegment.from_mp3(file_path)
        # set 16k sample rate is needed for Yamnet to read properly
        audio = audio.set_frame_rate(16000).set_channels(1)
        # save as wav, which is needed for the read operation
        audio.export(file_path.replace('.mp3', '.wav'), format="wav")
        # get the audio data
        sample_rate, wav_data = wavfile.read(file_path.replace('.mp3', '.wav'))
        # normalize for some reason
        waveform = wav_data / np.iinfo(wav_data.dtype).max
        #
        return waveform

    def class_names_from_csv(self):
        class_names = []
        class_map_csv_text = self.yamnet_model.class_map_path().numpy()
        with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                class_names.append(row['display_name'])
        return class_names

    def analyze_directory(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".mp3"):
                file_path = os.path.join(self.directory, filename)
                waveform = self.process_audio_file(file_path)

                # Run the model
                scores, embeddings, spectrogram = self.yamnet_model(waveform)
                class_scores = tf.reduce_mean(scores, axis=0)

                # Process the output
                top_class_indices = np.argsort(class_scores)[::-1][:3]  # Get top 3 classes
                class_map_path = self.yamnet_model.class_map_path().numpy()
                class_names = self.class_names_from_csv()

                print(f"Top class predictions for {filename}:")
                for i in top_class_indices:
                    print(f"  {class_names[i]}, score: {class_scores[i]}")
