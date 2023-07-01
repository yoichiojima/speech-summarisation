from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser
from google.cloud import speech, storage

BUCKET_NAME = "yo-personal"
LANGUAGE_CODE = "ja-JP"

def transcribe(uri: str):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code=LANGUAGE_CODE,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    file_name = uri.split('/')[-1].split('.')[0]

    print(f"Waiting for operation for audio {file_name} to complete...")
    response = operation.result(timeout=3600)

    with open(f"./transcript/{file_name}.txt", "w") as transcript_file:
        for result in response.results:
            transcript_file.write(result.alternatives[0].transcript + "\n")


def list_blob_uris(file_name: str):
    storage_client = storage.Client()
    for blob in storage_client.list_blobs(BUCKET_NAME):
        if blob.name.startswith(f"speech-to-text/{file_name}/split_audio/"):
            yield blob.name

def main(file_name: str):    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for blob_name in list_blob_uris(file_name):
            uri = f"gs://{BUCKET_NAME}/{blob_name}"
            executor.submit(transcribe, uri)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--file_name", type=str, help="URI of the audio file on GCS")
    args = parser.parse_args()
    main(args.file_name)
