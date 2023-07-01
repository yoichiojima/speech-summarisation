from lib.openai_wrapper import OpenAiWrapper
from lib.prompt import Prompt, Prompts

def summarise():
    role = (
        "the user is going to give you a transcript of a voice recording. "
        "that can be some kind of seminers or classes, or maybe just a random chat. "
        "you are going to summarise the transcript in japanese. "
        "the transcript is sometimes rough, but you are going to do your best."
    )

    p1 = Prompt(role = "system", content = role)

    with open("combined_transcript.txt", "r") as f:
        transcript = f.read()
    
    p2 = Prompt(role = "user", content = transcript)

    ps = Prompts()
    ps.append(p1)
    ps.append(p2)
    prompts = ps.get_prompts()

    gpt = OpenAiWrapper()
    gpt.complete_chat(prompts)
    first_message = gpt.get_first_message()

    print(first_message)

    with open("summary.txt", "w") as f:
        f.write(first_message)


if __name__ == "__main__":
    summarise()