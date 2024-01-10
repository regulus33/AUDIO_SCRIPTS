import os
import argparse
from pydub import AudioSegment, silence

def chop_audio(file_path, output_dir):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)

    # Detect non-silent parts of the audio
    non_silence = silence.detect_nonsilent(
        audio, min_silence_len=1000, silence_thresh=-32
    )

    # Process each non-silent segment
    for i, (start, end) in enumerate(non_silence):
        segment = audio[start:end]
        segment.export(f"{output_dir}/segment_{i}_{os.path.basename(file_path)}", format="mp3")

def process_directory(directory):
    # Create output directory if not exists
    output_dir = os.path.join(directory, "chopped")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            chop_audio(file_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chop audio files into segments")
    parser.add_argument("directory", type=str, help="Directory containing MP3 files to process")
    args = parser.parse_args()
    process_directory(args.directory)
