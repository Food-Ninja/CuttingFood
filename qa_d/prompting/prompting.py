import csv
import os

from gemma_prompter import GemmaPrompter
from llama_prompter import LlamaPrompter

prompters = [LlamaPrompter(), GemmaPrompter()]
system_msg = "Please answer the following question as briefly and concise as you can."
questions = []

data_path = os.path.join(os.path.dirname(__file__), "..", "qa.csv")
with open(data_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        questions.append(row[0])

result_path = os.path.join(os.path.dirname(__file__), "..", "results")
for prompter in prompters:
    prompt_res = []
    for q in questions:
        res = prompter.prompt_model(system_msg, q)
        prompt_res.append((q, res))
    with open(f"{result_path}/{prompter.model_name.lower()}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["question", "model_answer"])
        writer.writerows(prompt_res)
