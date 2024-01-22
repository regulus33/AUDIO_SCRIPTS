# Import necessary libraries
import os  # Provides functions to interact with the operating system
from argparse import ArgumentParser
import re
import tensorflow as tf  # TensorFlow, a machine learning library
import tensorflow_hub as hub  # TensorFlow Hub, for loading pre-trained models
import numpy as np  # NumPy, for numerical operations
from pydub import AudioSegment  # PyDub, for audio file manipulation
from scipy.io import wavfile  # SciPy module for reading and writing .wav files
import csv  # Module for handling CSV files
import shutil
import pdb


# Define a constant for the file extension we're working with
FILE_EXTENSION = 'mp3'
MODEL_EXTENSION = 'wav'


def scrub_arg(input_string):
    return input_string.replace("'", '')


# Define a class to process audio files
class SmartSoundDirectoryMaker:
    def __init__(self, input_dir, output_dir):
        self.in_dir = input_dir  # Store the directory of audio files
        self.output_dir = output_dir
        # Load the YAMNet model from TensorFlow Hub
        self.yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

    def _replace_last_char(self, s, old, new):
        # Find the last occurrence of the character
        index = s.rfind(old)

        # Check if the character is in the string
        if index != -1:
            # Replace the character
            s = s[:index] + new + s[index + 1:]
        return s

    def _get_audio_data(self, file_path):
        if FILE_EXTENSION != 'mp3':
            raise Exception("Only mp3 files are supported! Convert to mp3s first.")
        # Read the audio file using PyDub
        audio = AudioSegment.from_mp3(file_path)
        # Convert the audio sample rate to 16kHz and set to mono (1 channel)
        audio = audio.set_frame_rate(16000).set_channels(1)
        # Export the audio in WAV format (needed for further processing)
        audio.export(file_path.replace(FILE_EXTENSION, MODEL_EXTENSION), format=MODEL_EXTENSION)
        # Read the exported WAV file
        sample_rate, wav_data = wavfile.read(file_path.replace('.' + FILE_EXTENSION, '.' + MODEL_EXTENSION))
        # Normalize the audio data
        waveform = wav_data / np.iinfo(wav_data.dtype).max
        # Return the processed waveform data
        return waveform

    def _class_names_from_csv(self):
        class_names = []
        # Retrieve the class map file path from the YAMNet model
        class_map_csv_text = self.yamnet_model.class_map_path().numpy()
        # Open and read the CSV file
        with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Append each class name to the list
                class_names.append(row['display_name'])
        # Return the list of class names
        return class_names

    import re

    def _replace_non_alphanumeric(self, s):
        return re.sub(r'\W', '_', s)

    def _create_dir_from_top_classes(self, top_classes):
        dir_name = ''
        for klass in top_classes:
            dir_name += str(klass) + '_'
        dir_name = self._replace_last_char(dir_name, '_', '')
        dir_name = self._replace_non_alphanumeric(dir_name)
        path = self.output_dir + '/' + dir_name + '/'
        return path


    def analyze_directory(self):
        # Iterate over all files in the directory
        for filename in os.listdir(self.in_dir):
            # Check if the file is an MP3
            if filename.endswith(".mp3"):
                # Construct the full path of the file
                file_path = os.path.join(self.in_dir, filename)
                # Process the audio file to get waveform data
                waveform = self._get_audio_data(file_path)

                # Run the YAMNet model on the waveform data
                scores, embeddings, spectrogram = self.yamnet_model(waveform)
                # Average the scores over time
                class_scores = tf.reduce_mean(scores, axis=0)

                # Get the indices of the top 3 class predictions
                top_class_indexes = np.argsort(class_scores)[::-1][:3]
                # Retrieve the class map path
                class_map_path = self.yamnet_model.class_map_path().numpy()
                class_names = self._class_names_from_csv()
                top_classes = []
                for index in top_class_indexes:
                    top_classes.append(class_names[index])

                dir = self._create_dir_from_top_classes(top_classes)

                print(f"new dir for {filename}:")
                print(dir)

                if not os.path.exists(dir):
                    os.makedirs(dir)

                dir_path = dir + filename
                shutil.copy(file_path, dir_path)


parser = ArgumentParser()
parser.add_argument('--indir', type=str, required=True, help="Directory with input files")
parser.add_argument('--outdir', type=str, required=True, help="Directory with output files")

args = parser.parse_args()

indir = scrub_arg(args.indir)
outdir = scrub_arg(args.outdir)
# pdb.set_trace()
smart_sound_directory_maker = SmartSoundDirectoryMaker(indir, outdir)
smart_sound_directory_maker.analyze_directory()
