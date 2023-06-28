from argparse import ArgumentParser
from google.cloud import speech


def main():
    client = speech.SpeechClient()

    with open("audio-1.mp3", "rb") as audio_file:
        input_audio = audio_file.read()

    audio = speech.RecognitionAudio(content=input_audio)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code="ja-JP",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=3600)

    # Open a text file in write mode
    with open("transcript-1.txt", "a") as transcript_file:
        for result in response.results:
            # Write each transcript to the text file
            transcript_file.write("Transcript: {}\n".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    main()
