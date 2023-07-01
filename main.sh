#!/bin/bash

# remove all files from bucket
gsutil rm -r gs://yo-personal/speech-to-text/$1

# split audio into 100 second chunks
echo "Splitting audio into 100 second chunks..."
ffmpeg -i $1 -filter:a "atempo=0.5" -ac 1 -f segment -segment_time 100 split_audio/chunk%03d.flac # for analysis
ffmpeg -i $1 -filter:a "atempo=0.5" -ac 1 -f segment -segment_time 100 split_audio_mp3/chunk%03d.mp3 # for checking
echo "Done splitting audio into 100 second chunks!"

# upload to cloud storage
echo "Uploading to cloud storage..."
gsutil -m cp -r split_audio gs://yo-personal/speech-to-text/$1/
echo "Done uploading to cloud storage!"

# run speech-to-text on each chunk
echo "Running speech-to-text on each chunk..."
python -m convert_speech_to_text --file_name $1
echo "Done running speech-to-text on each chunk!"

# summarise
echo "\n[Summary]"
python -m summarise