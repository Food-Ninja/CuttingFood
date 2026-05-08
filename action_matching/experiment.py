import os
import random

from action_matching.prompting.openai_prompter import OpenAIPrompter

ACTIONS = ["cut", "carve", "pare", "saw", "dice", "chop", "cube", "mince", "slice", "sliver", "snip", "halve", "divide",
           "quarter", "julienne"]
random.shuffle(ACTIONS)

# prompters = [LlamaPrompter(), GemmaPrompter()]
prompters = [OpenAIPrompter()]

system_msg = "You are an expert in understanding task semantics and household actions. You are tasked with grouping a list of action verbs into groups based on their parameterisation in the domain of \"Cutting fruits and vegetables\". So two actions that have similar execution parameters should end up in the same group. For each group, you should choose one representative. Additionally, you have the option to exclude options that you do not deem suitable for the aforementioned task domain"
user_msg = f"List of actions: {ACTIONS}\nYour Grouping: "

data_path = os.path.join(os.path.dirname(__file__), "..", "action_matching/data/")
os.makedirs(data_path, exist_ok=True)

for p in prompters:
    grouping = p.prompt_model(system_msg, user_msg)
    with open(f"{data_path}/{p.model_name.lower()}.txt", "w", newline="", encoding="utf-8") as file:
        file.write(grouping)
