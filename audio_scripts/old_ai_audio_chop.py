import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import csv

# Load YAMNet model from TensorFlow Hub
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

# Function to convert MP3 to WAV and ensure the sample rate is 16 kHz
def process_audio_file(file_path):
    audio = AudioSegment.from_mp3(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path.replace('.mp3', '.wav'), format="wav")

    sample_rate, wav_data = wavfile.read(file_path.replace('.mp3', '.wav'))
    waveform = wav_data / np.iinfo(wav_data.dtype).max  # Normalize the waveform
    return waveform

# Helper function to read class names
def class_names_from_csv(class_map_csv_text):
    class_names = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row['display_name'])
    return class_names

# Directory containing MP3 files
directory = '/Users/zacharyrowden/Desktop/AUDIO_SCRIPTS/audio_files'  # Replace with your directory path

# Process each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        file_path = os.path.join(directory, filename)
        waveform = process_audio_file(file_path)

        # Run the model
        scores, embeddings, spectrogram = yamnet_model(waveform)
        class_scores = tf.reduce_mean(scores, axis=0)

        # Process the output
        top_class_indices = np.argsort(class_scores)[::-1][:3]  # Get top 3 classes
        class_map_path = yamnet_model.class_map_path().numpy()
        class_names = class_names_from_csv(class_map_path)

        print(f"Top class predictions for {filename}:")
        for i in top_class_indices:
            print(f"  {class_names[i]}, score: {class_scores[i]}")
