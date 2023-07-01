from glob import glob
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

    with open(f"./transcripts/{file_name}.txt", "w") as transcript_file:
        for result in response.results:
            transcript_file.write(result.alternatives[0].transcript + "\n")


def list_blob_uris(file_name: str):
    storage_client = storage.Client()
    for blob in storage_client.list_blobs(BUCKET_NAME):
        if blob.name.startswith(f"speech-to-text/{file_name}/split_audio/") and blob.name.endswith(".flac"):
            yield blob.name

def upload_to_bucket(bucket_name: str, source_file_name: str, destination_blob_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def combine_transcripts():
    transcripts = glob("./transcripts/*.txt")
    transcripts.sort()
    with open("combined_transcript.txt", "w") as f:
        for transcript in transcripts:
            with open(transcript, "r") as t:
                transcript = t.read()
            f.write(transcript + "\n")
 
def main(file_name: str):    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for blob_name in list_blob_uris(file_name):
            uri = f"gs://{BUCKET_NAME}/{blob_name}"
            executor.submit(transcribe, uri)
    combine_transcripts()
    upload_to_bucket(BUCKET_NAME, "combined_transcript.txt", f"speech-to-text/{file_name}/combined_transcript.txt")
    print("Done!")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--file_name", type=str, help="URI of the audio file on GCS")
    args = parser.parse_args()
    main(args.file_name)
