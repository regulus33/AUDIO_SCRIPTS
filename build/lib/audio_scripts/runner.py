import os
from audio_scripts.ai_audio_chop import AudioProcessor
from audio_scripts.simple_audio_chop import split_audio

SCRIPT_DIR = '/Users/zacharyrowden/Desktop/AUDIO_SCRIPTS/'
INPUT_FILES_DIR = 'audio_files/'
audio_files_directory = SCRIPT_DIR + INPUT_FILES_DIR

# ai_audio_chop
# processor = AudioProcessor('/Users/zacharyrowden/Desktop/AUDIO_SCRIPTS/audio_files')
# processor.analyze_directory()

# split_audio
file_path = audio_files_directory + 'RPReplay_Final1672011390.mp3'  # Replace with your file path
split_audio(file_path)