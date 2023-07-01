ffmpeg -i audio-1.mp3 -filter:a "atempo=0.5" -ac 1 -f segment -segment_time 100 split_audio/out%03d.flac
