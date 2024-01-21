import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

def split_audio(file_path, format='wav'):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)

    # Detect transients/onsets
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='samples')

    # Split audio at transients
    audio = AudioSegment.from_file(file_path, format=format)
    chunks = [audio[max(0, onset - 1000):onset + 1000] for onset in onsets]

    # Save chunks (optional)
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_{i}.{format}", format=format)

    # Plotting
    plt.figure(figsize=(15, 4))
    librosa.display.waveshow(y, sr=sr)
    for onset in onsets:
        plt.axvline(onset/sr, color='r')

    plt.title('Waveform with Transient Markers')
    plt.show()

    return chunks

