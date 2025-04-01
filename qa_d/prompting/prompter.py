class Prompter:
    def __init__(self, model: str, temp=0.0, max_new_tokens=200):
        self.model_name = model
        self.temperature = temp
        self.max_new_tokens = max_new_tokens

    def prompt_model(self, system_msg: str, question: str) -> str:
        pass
