from argparse import ArgumentParser
from tqdm import tqdm
from google.cloud import speech
from concurrent.futures import ThreadPoolExecutor

def transcribe(i):
    client = speech.SpeechClient()
    index = str(i).zfill(3)

    uri = f"gs://yo-personal/speech-to-text/2023-06-28/split_audio/out{index}.flac"

    audio = speech.RecognitionAudio(uri=uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="ja-JP",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=3600)

    # Open a text file in write mode
    with open(f"./transcript/{index}.txt", "w") as transcript_file:
        for result in response.results:
            # Write each transcript to the text file
            transcript_file.write("Transcript: {}\n".format(result.alternatives[0].transcript))

def main(start: int, end: int):
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        list(tqdm(executor.map(transcribe, range(start, end + 1)), total=end-start+1))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1)
    args = parser.parse_args()
    main(args.start, args.end)

