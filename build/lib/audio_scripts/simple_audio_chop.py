import librosa
import librosa.display
import numpy as np
from pydub import AudioSegment
import os


def load_audio(file_path):
    """Load an audio file."""
    return librosa.load(file_path, sr=None)


def detect_onsets(y, sr):
    """Detect transients/onsets in the audio."""
    return librosa.onset.onset_detect(y=y, sr=sr, units='samples')


def split_audio_segment(audio, onsets, format='wav'):
    """Split audio at transients."""
    return [audio[max(0, onset - 1000):onset + 1000] for onset in onsets]


def save_chunks(chunks, format, directory=None):
    """Save audio chunks to files."""
    for i, chunk in enumerate(chunks):
        path = f"chunk_{i}.{format}"
        if directory:
            path = os.path.join(directory, path)
            os.makedirs(directory, exist_ok=True)
        chunk.export(path, format=format)


def chop(file_path, format_file, directory):
    """Split an audio file at transients/onsets and save the chunks."""
    y, sr = load_audio(file_path)
    onsets = detect_onsets(y, sr)
    audio = AudioSegment.from_file(file_path, format=format_file)
    chunks = split_audio_segment(audio, onsets, format_file)
    if directory:
        save_chunks(chunks, format_file, directory)
    # librosa.display.waveshow(y, sr=sr)
    return chunks
