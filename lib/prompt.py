class Prompt:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class Prompts:
    def __init__(self):
        self.prompts = []

    def append(self, prompt: Prompt):
        self.prompts.append(prompt)

    def get_prompts(self):
        return [i.to_dict() for i in self.prompts]
