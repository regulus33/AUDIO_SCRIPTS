import os
# from audio_scripts.ai_audio_chop import AudioProcessor
from audio_scripts.simple_audio_chop import chop

SCRIPT_DIR = '/Users/zacharyrowden/Desktop/AUDIO_SCRIPTS/'
INPUT_FILES_DIR = 'audio_files/'
audio_files_directory = SCRIPT_DIR + INPUT_FILES_DIR

# split_audio
file_path = audio_files_directory + 'RPReplay_Final1672014861.mp3'  # Replace with your file path
chop(file_path, 'mp3', '/Users/zacharyrowden/Desktop/AUDIO_SCRIPTS/audio_files/chunks')