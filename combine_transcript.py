from glob import glob


def main():
    transcripts = glob("./transcript/*.txt")

    # sort transcripts by name
    transcripts.sort()

    with open("combined_transcript.txt", "w") as f:
        for i, transcript in enumerate(transcripts):
            with open(transcript, "r") as t:
                transcript = t.read()
            f.write(str(i) + ": " + transcript + "\n")

if __name__ == "__main__":
    main()
